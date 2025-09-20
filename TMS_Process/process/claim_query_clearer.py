import asyncio
import json
import time
import random
import os
import subprocess
from playwright.async_api import async_playwright, Page, TimeoutError, expect
from EHOSP.tk_ehosp.alert_boxes import error_tk_box, tk_ask_yes_no, tk_ask_input, select_ward
from TMS_Process.process.claim_clearer_RF import is_home_page, select_ALL_and_search
from TMS_Process.process.discharge_process import discharge_main
from TMS_Process.process.enhancement import enhancement, enhancement_type_2
from TMS_Process.process.tks import initial_setup_for_base_folder
from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
from dkbssy.utils.colour_prints import ColourPrint, message_box
from TMS_Process.process.file_folder_searcher import search_file_all_drives_base, ProjectPaths
from TMS_Process.process.pdf_creator import generate_pdfs_from_txt_list, delete_pdf, custom_size_pdf_from_txt_list, \
    save_pdf_backup


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
    """setting up base folder"""
    BASE_FOLDER = initial_setup_for_base_folder()

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
        page.set_default_timeout(120000)


        # start_index = 0
        multi_lined_list:list = reg_multiline_str.split()

        # "Commented as saving is causing problem in testing"
        # # checking if the last save is in list
        # if last_saved and last_saved in multi_lined_list:
        #     start_index = multi_lined_list.index(last_saved)+1
        #     print("Start index: ",start_index)


        for registration_no in multi_lined_list:
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

            if caseview.strip().lower().startswith('under'):

                'checking for the discharge button presence'
                await page.wait_for_selector("//button[normalize-space()='Initiate Resubmission']")
                'checking for the presence of Initiate button'
                parent_of_discharge_node_texts = await page.locator("//button[normalize-space()='Initiate Resubmission']/parent::div").text_content()
                print(parent_of_discharge_node_texts)

                print('Initiate Enhancement'.lower() in parent_of_discharge_node_texts.lower())

                text_file_search_path = search_file_all_drives_base(filename=registration_no)
                # Open Explorer at that folder
                subprocess.Popen(f'explorer "{os.path.dirname(text_file_search_path[0])}"')

                'blocking so that files can be checked and if necessary discharge can be manually downloaded from nextgen. So this download will be included in pdf creation'
                'Right now yes or no both proceed the same'
                answer_about_files_complete = tk_ask_yes_no(question='Check the folder has all necessary files.\nPress "YES" to continue')
                # if answer_about_files_complete

                pdf_1mb = _create_custom_pdf(registration_no=registration_no)


                if 'Initiate Enhancement'.lower() in parent_of_discharge_node_texts.lower():

                    "clicking finance to se number of days enhancement done"
                    await page.locator("//button[normalize-space()='Finance']").click()

                    days_enhanced_str = await page.locator("//th[normalize-space()='Quantity']//ancestor::table/tbody//tr/td[6]").all_text_contents()
                    days_enhanced_int = [int(i) for i in days_enhanced_str]
                    total_enhanced = sum(days_enhanced_int)
                    answer = tk_ask_yes_no(
                        question=f'The total enhanced already taken is: {total_enhanced} days.\nDo You want to take more enhancement.\n\nIf clicked "NO" it will proceed.')  # returns True False
                    if answer:
                        # await enhancement(page=page, pdf_1=pdf_1mb)
                        await enhancement_type_2(page=page, pdf_1mb=pdf_1mb)
                    else:  # for the no further enhancement required
                        await discharge_main(page=page, pdf_1mb=pdf_1mb)

                else:  # for those whom the enhancement is not required
                    "testing the discharge"
                    await discharge_main(page=page, pdf_1mb=pdf_1mb)

                delete_pdf(pdf_1mb)

            # else:
            #     answer = tk_ask_yes_no(question=f'The {registration_no} is not in "Preauth query", or "Claim query, or "Under treatment".\nDo you want to proceed to next case.')
            #     if not answer:
            #         error_tk_box(error_message='User Stopped', error_title='Error')
            #         raise ValueError('User Stopped. The user input  was cancelled')


            # ✅ update progress after each successful run
            update_last_saved(registration_no=registration_no, CURRENT_SAVE=CURRENT_SAVE)

            # await asyncio.sleep(5)

def _create_files_pdfs(registration_no):
    ColourPrint.print_yellow(message_box('Please wait. Scanning drives...'))
    text_file_path = search_file_all_drives_base(filename=registration_no)
    print(json.dumps(text_file_path, indent=2))
    if not text_file_path:
        err_msg = f'The txt file is not present in the folder for registration no {registration_no}.'
        error_tk_box(error_message=err_msg)
        raise FileNotFoundError(err_msg)
    pdf_1mb, pdf_2mb = generate_pdfs_from_txt_list(text_file_path)
    return pdf_1mb, pdf_2mb

def _create_custom_pdf(registration_no):
    ColourPrint.print_yellow(message_box('Please wait. Scanning drives...'))
    text_file_path = search_file_all_drives_base(filename=registration_no)
    print(json.dumps(text_file_path, indent=2))
    if not text_file_path:
        err_msg = f'The txt file is not present in the folder for registration no {registration_no}.'
        error_tk_box(error_message=err_msg)
        raise FileNotFoundError(err_msg)
    pdf_1mb = save_pdf_backup(txt_file_paths=text_file_path, max_size_mb=0.95)
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
    await page.locator("//h4[text()='Treatment']").click()
    await page.locator("//div[contains(text(),'Investigations')]/parent::div/following-sibling::h2/button").click()
    await page.locator("//button[normalize-space()='Add Other Documents']").click()
    # await page.locator("//input[@id='otherInvest']").fill(remark)  # instead Null is autofill and uses as selector
    await page.locator("//button[contains(@data-toggle,'collapse')][normalize-space()='ADD']").click()
    await page.wait_for_selector("//p[normalize-space()='Null']")
    await page.set_input_files("//input[@type='file']", pdf_1mb)
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

    #




def main(reg_multiline_str):
    asyncio.run(_main(reg_multiline_str))





if __name__ =="__main__":
    # main("1009299836")
    main()