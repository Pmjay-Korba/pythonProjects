import asyncio
import json
import time
import random
from playwright.async_api import async_playwright, Page, TimeoutError, expect

from EHOSP.tk_ehosp.alert_boxes import error_tk_box, tk_ask_yes_no, tk_ask_input, select_ward
from TMS_Process.process.claim_clearer import is_home_page, select_ALL_and_search
from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
from dkbssy.utils.colour_prints import ColourPrint, message_box
from TMS_Process.process.file_folder_searcher import search_file_all_drives, ProjectPaths
from TMS_Process.process.pdf_creator import generate_pdfs_from_txt_list, delete_pdf, custom_size_pdf_from_txt_list


def load_last_saved(CURRENT_SAVE):
    """Load last saved registration number from JSON file."""
    if CURRENT_SAVE.exists():
        with open(CURRENT_SAVE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("query_clear")
    return None


def update_last_saved(CURRENT_SAVE, registration_no: str):
    """Update JSON file with the latest saved registration number."""
    with open(CURRENT_SAVE, "w", encoding="utf-8") as f:
        json.dump({"query_clear": registration_no}, f, indent=4)

async def _main(reg_multiline_str, cdp_port=9222):

    # print(pdf_1mb,pdf_2mb)
    CURRENT_SAVE = ProjectPaths.DOWNLOAD_DIR/"current_saves.json"

    last_saved = load_last_saved(CURRENT_SAVE=CURRENT_SAVE)
    print(last_saved)



    async with async_playwright() as p:

        browser = await p.chromium.connect_over_cdp(f"http://localhost:{cdp_port}")
        context = browser.contexts[0]
        all_pages = context.pages

        pages_indexes = await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='PMJAY - Provider',
                                                                              cdp_port=cdp_port)
        page_index = pages_indexes[0]  # selecting the first index of matching page

        page = all_pages[page_index]  # selecting the first PAGE of matching page
        page.set_default_timeout(20000)



        start_index = 0
        multi_lined_list:list = reg_multiline_str.split()

        "Commented as saving is causing problem in testing"
        # # checking if the last save is in list
        # if last_saved and last_saved in multi_lined_list:
        #     start_index = multi_lined_list.index(last_saved)+1
        #     print("Start index: ",start_index)


        for registration_no in multi_lined_list[start_index:]:
            if registration_no.strip() == "":
                print("Blank")
                continue
            time.sleep(5)
            ColourPrint.print_green(message_box(registration_no))


            await is_home_page(page=page)

            await select_ALL_and_search(page=page, registration_no=registration_no)

            'Looking if queried or resolved'
            caseview = await page.locator("//li[@class='ES8GosCR9dsXoNoSy9So he8vrs1JR2h4h_PgLoHc ']").text_content()
            if 'caseview' in caseview.strip().lower() :
                ColourPrint.print_blue(f'Skipped: {registration_no}')
                continue  # skipping non - queried

            if caseview.strip().lower().startswith('pre') and 'que' in caseview.strip().lower():
                pdf_1mb = _create_custom_pdf(registration_no=registration_no)
                await pre_auth_query_clearer(page=page, pdf_1mb=pdf_1mb)
                delete_pdf(pdf_1mb)


            if caseview.strip().lower().startswith('claim'):

                pdf_1mb, pdf_2mb = _create_files_pdfs(registration_no=registration_no)
                await claim_query_clearer(page=page, registration_no=registration_no, pdf_1mb=pdf_1mb, pdf_2mb=pdf_2mb)

                delete_pdf(pdf_1mb)
                delete_pdf(pdf_2mb)

            # if caseview.strip().lower().startswith('under'):
            #     pdf_1mb = _create_custom_pdf(registration_no=registration_no)
            #     await enhancement(page=page, pdf_1=pdf_1mb)
            #     delete_pdf(pdf_1mb)

            # ✅ update progress after each successful run
            update_last_saved(registration_no=registration_no, CURRENT_SAVE=CURRENT_SAVE)

def _create_files_pdfs(registration_no):
    ColourPrint.print_yellow(message_box('Please wait. Scanning drives...'))
    text_file_path = search_file_all_drives(filename=registration_no)
    print(json.dumps(text_file_path, indent=2))
    pdf_1mb, pdf_2mb = generate_pdfs_from_txt_list(text_file_path)
    return pdf_1mb, pdf_2mb

def _create_custom_pdf(registration_no):
    ColourPrint.print_yellow(message_box('Please wait. Scanning drives...'))
    text_file_path = search_file_all_drives(filename=registration_no)
    print(json.dumps(text_file_path, indent=2))
    pdf_1mb = custom_size_pdf_from_txt_list(txt_file_paths=text_file_path, max_size_mb=0.95)
    return pdf_1mb

async def claim_query_clearer(page, pdf_1mb, pdf_2mb, registration_no=None):

    await page.locator("//span[normalize-space()='Query Response']").click()  # clicking the query bar
    remarks = ['uploaded', 'File uploaded', 'Files done uploading', 'UPLOAD', 'upload', 'FILES UPLOAD', 'DONE']
    remark = random.choice(remarks)
    # print(remark)
    "searching the file"

    await page.set_input_files("//input[@id='SupportingDoc2']", pdf_2mb)

    if pdf_1mb:
        await page.set_input_files('//*[@id="SupportingDoc1"]', pdf_1mb)

    await page.locator("//input[@id='Remarks']").fill(remark)

    await page.locator("//button[normalize-space()='SAVE']").click()

    await page.wait_for_selector("//span[normalize-space()='Query Response saved successfully.']")


    await page.locator("//button[normalize-space()='SUBMIT CLAIM']").click()

    await page.locator("//button[normalize-space()='YES']").click()

async  def pre_auth_query_clearer(page, pdf_1mb, pdf_2mb=None):
    await page.locator("//div[contains(text(),'Investigations')]/parent::div/following-sibling::h2/button").click()
    await page.locator("//button[normalize-space()='Add Other Documents']").click()
    # await page.locator("//input[@id='otherInvest']").fill(remark)  # instead Null is autofill and uses as selector
    await page.set_input_files("//input[@type='file']", pdf_1mb)
    await page.locator("//button[contains(@data-toggle,'collapse')][normalize-space()='ADD']").click()
    await page.wait_for_selector("//p[normalize-space()='Null']")
    await page.locator("//button[normalize-space()='VALIDATE & PREVIEW']").click()
    await page.locator("//button[normalize-space()='INITIATE RESUBMISSION']").click()
    await page.locator("//button[normalize-space()='YES']").click()

async def pre_auth_filler(page:Page):
    await page.locator("//h4[normalize-space()='Medical Information']/parent::button").click()
    await page.locator("//span[normalize-space()='General Findings']/parent::button").click()
    temp = random.choice([97,98,99])
    await page.locator("//input[@id='Temperature']").fill(temp)
    pulse = random.choice([60,65,70,75,80])
    await page.locator("//input[@id='PulseRatePerMinute']").fill(pulse)
    height = random.choice([140,145,150,155])
    await page.locator("//input[@id='Height']").fill(height)
    weight = random.choice([45,50,55,60,65,70])
    await page.locator("//input[@id='Weight']").fill(weight)

    await page.locator('(//input[@id="Cyanosis"]/following-sibling::span[@class="X822VFjKSr1jqv5N60Yx"])[2]').click()
    await page.locator('(//input[@id="Pallor"]/following-sibling::span[@class="X822VFjKSr1jqv5N60Yx"])[2]').click()
    await page.locator('(//input[@id="Malnutrition"]/following-sibling::span[@class="X822VFjKSr1jqv5N60Yx"])[2]').click()
    await page.locator('(//input[@id="OedemaInFeet"]/following-sibling::span[@class="X822VFjKSr1jqv5N60Yx"])[2]').click()

async def enhancement(page:Page, pdf_1):
    # verify_under_treatment =
    await page.locator("//button[normalize-space()='Initiate Enhancement']").click()
    await page.locator("//button[normalize-space()='YES']").click()
    depart = await page.locator("//th[normalize-space()='Speciality']/ancestor::table/tbody//tr[1]/td[2]").text_content()
    # show more
    await page.locator("//th[normalize-space()='Speciality']/ancestor::table/tbody//tr[1]/td[3]//span").click()
    diagnosis = await page.locator("//th[normalize-space()='Speciality']/ancestor::table/tbody//tr[1]/td[3]/p").text_content()
    if diagnosis.endswith("Show Less"):
        diagnosis = diagnosis.removesuffix("Show Less")

    print(depart, diagnosis)



    #
    await page.locator("(//label[normalize-space()='Speciality:']/ancestor::div[normalize-space(@class)='row']//input[@type='text' and contains(@id,'react-select')])[1]").fill(depart)
    # await page.locator("//input[@id='react-select-36-input']").fill(depart)
    await page.keyboard.press(key='Enter')
    # await asyncio.sleep(1)

    " added this here so that option populates gets time"
    days_enhanced_str = await page.locator("//th[normalize-space()='No. of Days/Units']//ancestor::table/tbody//tr/td[5]").all_text_contents()
    days_enhanced_int = [int(i) for i in days_enhanced_str]
    total_enhanced = sum(days_enhanced_int)
    answer = tk_ask_yes_no(
        question=f'The total enhanced already taken is: {total_enhanced} days.\nDo You want to take more enhancement.')  # returns True False
    if answer:
        "if yes diagnosis is filled"
        dd = page.locator("(//label[normalize-space()='Speciality:']/ancestor::div[normalize-space(@class)='row']//input[@type='text' and contains(@id,'react-select')])[2]")
        await dd.wait_for(state="visible")
        await dd.fill(diagnosis)
        await page.keyboard.press(key='Enter')

        "asking the ward type"
        ward_type = select_ward()

        "selecting the type of ward"
        ward_stay =page.locator("(//label[normalize-space()='Speciality:']/ancestor::div[normalize-space(@class)='row']//input[@type='text' and contains(@id,'react-select')])[3]")
        await ward_stay.wait_for(state="visible")
        await ward_stay.fill(ward_type)
        await page.keyboard.press(key='Enter')

        user_input_days = tk_ask_input(question="How many days you want to take enhancement.\nType in below for desired days.\nPRESSING Enter without typing number of days\nwill automatically take 3 days", default="3")
        if user_input_days is None:
            error_tk_box(error_message='User Cancelled', error_title='Error')
            raise ValueError('User cancelled the user input prompt')

        await page.locator("//input[@id='noofdays']").fill(user_input_days)


        reason_enhance = random.choice(['Additional facts were diagnosed during treatment.',
                          'Details submitted during pre-auth was not correct.',
                          'Others',
                          'Treatment plan changed during hospitalization.',
                          'Treatment plan is optimized for better outcome.'
                          ])

        reason_web = page.locator("(//label[normalize-space()='Speciality:']/ancestor::div[normalize-space(@class)='row']//input[@type='text' and contains(@id,'react-select')])[4]")
        await reason_web.wait_for(state="visible")
        await reason_web.fill(reason_enhance)
        await page.keyboard.press(key='Enter')

        await page.set_input_files("//input[@type='file']", pdf_1)
        await page.locator("//div[div[label[normalize-space()='Enhancement Reason:']]]//img[@class and not(@width)]").click()
        await page.locator("//div[contains(text(),'Investigations')]/parent::div//parent::div//button[@type]").click()
        await page.locator("//button[normalize-space()='Add Bed Side Photo']").click()
        await page.set_input_files("//label[normalize-space()='Upload Attachment']/following-sibling::div//input", pdf_1)
        await page.locator("//button[contains(@data-toggle,'collapse')][normalize-space()='ADD']").click()

        




    #




def main(reg_multiline_str):
    asyncio.run(_main(reg_multiline_str))





if __name__ =="__main__":
    # main("1009299836")
    main()