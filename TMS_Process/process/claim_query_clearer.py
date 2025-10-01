import asyncio
import json
import sys
import time
import random
import os
import subprocess
from playwright.async_api import async_playwright, Page, TimeoutError, expect

from EHOSP.ehospital_proper.inject_custom_form_html import modal_info_button, modal_folder_button
from EHOSP.tk_ehosp.alert_boxes import error_tk_box, tk_ask_yes_no, tk_ask_input, select_ward
from TMS_Process.process.claim_clearer_RF import is_home_page, select_ALL_and_search
from TMS_Process.process.discharge_process import discharge_main
from TMS_Process.process.enhancement import enhancement, enhancement_type_2
from TMS_Process.process.pdf_creator_threaded import generate_fixed_pdfs_threaded
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

async def _main(reg_multiline_str, set_timeout_is, cdp_port=9222):
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
        page.set_default_timeout(set_timeout_is)


        # start_index = 0
        multi_lined_list:list = reg_multiline_str.split()

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
                query_question_is = (await get_query_question(page=page)).strip('Show Less')
                await modal_info_button(message=query_question_is, page=page)

                'open folder'
                await display_modal_show_folder(page=page, registration_no=registration_no)

                pre_auth_query_answer = tk_ask_yes_no(question="Do you want to process the preauth query?")
                if pre_auth_query_answer:
                    # opening folder and display the continue modal

                    pdf_1, pdf_2, pdf_3 = _create_custom_pdf_new(registration_no=registration_no)
                    await pre_auth_query_clearer(page=page, pdf_list=[pdf_1, pdf_2, pdf_3])

                    delete_pdf(pdf_1)
                    delete_pdf(pdf_2)
                    delete_pdf(pdf_3)


            if caseview.strip().lower().startswith('claim'):
                query_question_is = (await get_query_question(page=page)).strip('Show Less')
                await modal_info_button(message=query_question_is, page=page)

                # opening folder and display the continue modal
                await display_modal_show_folder(page=page, registration_no=registration_no)

                claim_query_answer = tk_ask_yes_no(question="Do you want to process the claim query?")

                # sys.exit()

                if claim_query_answer:
                    pdf_1mb, pdf_2mb = _create_files_pdfs(registration_no=registration_no)
                    await claim_query_clearer(page=page, registration_no=registration_no, pdf_1mb=pdf_1mb, pdf_2mb=pdf_2mb)

                    delete_pdf(pdf_1mb)
                    delete_pdf(pdf_2mb)
                # else:

            if caseview.strip().lower().startswith('under'):

                'checking for the discharge button presence'
                await page.wait_for_selector("//button[normalize-space()='Initiate Resubmission']")
                'checking for the presence of Initiate button'
                parent_of_discharge_node_texts = await page.locator("//button[normalize-space()='Initiate Resubmission']/parent::div").text_content()
                print(parent_of_discharge_node_texts)

                print('Initiate Enhancement'.lower() in parent_of_discharge_node_texts.lower())

                # "Display modal"
                await display_modal_show_folder(page=page, registration_no=registration_no)


                if 'Initiate Enhancement'.lower() in parent_of_discharge_node_texts.lower():

                    "clicking finance to se number of days enhancement done"
                    await page.locator("//button[normalize-space()='Finance']").click()

                    days_enhanced_str = await page.locator("//th[normalize-space()='Quantity']//ancestor::table/tbody//tr/td[6]").all_text_contents()
                    days_enhanced_int = [int(i) for i in days_enhanced_str]
                    total_enhanced = sum(days_enhanced_int)
                    answer = tk_ask_yes_no(question=f'The total enhanced already taken is: {total_enhanced} days.\nDo You want to take more enhancement.\n\nIf clicked "NO" it will proceed.')  # returns True False
                    if answer:
                        # await enhancement(page=page, pdf_1=pdf_1mb)
                        pdf_1, pdf_2, pdf_3 = _create_custom_pdf_new(registration_no=registration_no)
                        await enhancement_type_2(page=page, pdfs_list=[pdf_1, pdf_2, pdf_3])
                        delete_pdf(pdf_1)
                        delete_pdf(pdf_2)
                        delete_pdf(pdf_3)

                    else:
                        answer2  = tk_ask_yes_no( question='Do you want to DISCHARGE or PROCEED TO NEXT CASE NUMBER\n\n"YES" : Process discharge\n"NO" : Proceed to next Case.No.')  # returns True False
                        if answer2:  # means continue discharge else proceed to next reg.no.
                            pdf_1, pdf_2, pdf_3 = _create_custom_pdf_new(registration_no=registration_no)
                            pdf_4 = pdf_1
                            await discharge_main(page=page, pdfs_list=[pdf_1, pdf_2, pdf_3, pdf_4])
                            delete_pdf(pdf_1)
                            delete_pdf(pdf_2)
                            delete_pdf(pdf_3)
                            delete_pdf(pdf_4)
                        else:  # for the no further enhancement required
                            print('Continuing')
                else:  # for those whom the enhancement is not required
                    "testing the discharge"
                    pdf_1, pdf_2, pdf_3 = _create_custom_pdf_new(registration_no=registration_no)
                    pdf_4 = pdf_1
                    await discharge_main(page=page, pdfs_list=[pdf_1, pdf_2, pdf_3, pdf_4])
                    delete_pdf(pdf_1)
                    delete_pdf(pdf_2)
                    delete_pdf(pdf_3)
                    delete_pdf(pdf_4)

                # At the end, check if Explorer is still running
                # if win_fol_displayed.poll() is None:  # None = still running
                #     print("Explorer still open → closing it")
                #     win_fol_displayed.terminate()  # or proc.kill()
                # else:
                #     print("Explorer already closed by user")

                # delete_pdf(pdf_1mb)

            # else:
            #     answer = tk_ask_yes_no(question=f'The {registration_no} is not in "Preauth query", or "Claim query, or "Under treatment".\nDo you want to proceed to next case.')
            #     if not answer:
            #         error_tk_box(error_message='User Stopped', error_title='Error')
            #         raise ValueError('User Stopped. The user input  was cancelled')


            # ✅ update progress after each successful run
            update_last_saved(registration_no=registration_no, CURRENT_SAVE=CURRENT_SAVE)

            # await asyncio.sleep(5)

async def display_modal_show_folder(page, registration_no):
    try:
        text_file_search_path = search_file_all_drives_base(filename=registration_no)[0]
    except IndexError as e:
        err_msg = f'The txt file is not present in the folder for registration no {registration_no}.'
        error_tk_box(error_message=err_msg)
        raise IndexError(err_msg)

    await modal_folder_button(page=page,
                              message="Check the images are complete in folder. <br>To see images click 'Open Folder'<br>After checking, click 'Continue'.",
                              file_path=text_file_search_path
                              )

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

def _create_custom_pdf_rough(registration_no):
    ColourPrint.print_yellow(message_box('Please wait. Scanning drives...'))
    text_file_path = search_file_all_drives_base(filename=registration_no)
    print(json.dumps(text_file_path, indent=2))
    if not text_file_path:
        err_msg = f'The txt file is not present in the folder for registration no {registration_no}.'
        error_tk_box(error_message=err_msg)
        raise FileNotFoundError(err_msg)
    pdf_1mb = save_pdf_backup(txt_file_paths=text_file_path, max_size_mb=0.95)
    return pdf_1mb


def _create_custom_pdf_new(registration_no):
    ColourPrint.print_yellow(message_box('Please wait. Scanning drives...'))
    text_file_path = search_file_all_drives_base(filename=registration_no)
    text_file_path = text_file_path[0]
    print(json.dumps(text_file_path, indent=2))
    if not text_file_path:
        err_msg = f'The txt file is not present in the folder for registration no {registration_no}.'
        error_tk_box(error_message=err_msg)
        raise FileNotFoundError(err_msg)
    pdf_1, pdf_2, pdf_3 = generate_fixed_pdfs_threaded(txt_file_path=text_file_path)
    return pdf_1,pdf_2,pdf_3

async def click_first_until_second_present(page, first_locator, second_locator, max_retries=5, wait_time=1.0):
    """
    Clicks the first button until the second button appears.
    Retries up to max_retries with a wait_time between attempts.
    """
    for attempt in range(1, max_retries + 1):
        try:
            # Check if second element is present
            second_visible = await page.locator(second_locator).count() > 0
            if second_visible:
                print(f"✅ Second element is present, stopping retries.")
                return True

            # Wait for first element to be ready
            await page.wait_for_selector(first_locator, timeout=2000)
            await page.locator(first_locator).click()
            print(f"✅ Clicked first locator (attempt {attempt})")

            # Small wait to allow second element to appear
            await asyncio.sleep(wait_time)

        except TimeoutError:
            print(f"⚠️ Attempt {attempt}: first element not ready, retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)

    # Final check if second element is present
    if await page.locator(second_locator).count() > 0:
        print("✅ Second element appeared after retries.")
        return True
    else:
        print(f"❌ Failed: second element never appeared after {max_retries} attempts.")
        return False

async def claim_query_clearer(page, pdf_1mb, pdf_2mb, registration_no=None):

    await page.locator("//span[normalize-space()='Query Response']").click()  # clicking the query bar
    remarks = ['uploaded', 'File uploaded', 'Files done uploading', 'UPLOAD', 'upload', 'FILES UPLOAD', 'DONE']
    remark = random.choice(remarks)
    # print(remark)
    "searching the file"

    await page.set_input_files("//input[@id='SupportingDoc2']", pdf_2mb)
    await asyncio.sleep(1)

    if pdf_1mb:
        # print(';pdf1mb' , pdf_1mb)
        await page.set_input_files('//*[@id="SupportingDoc1"]', pdf_1mb)
        await asyncio.sleep(1)

    await page.locator("//input[@id='Remarks']").fill(remark)

    await page.locator("//button[normalize-space()='SAVE']").click()

    await page.wait_for_selector("//span[normalize-space()='Query Response saved successfully.']")


    await page.locator("//button[normalize-space()='SUBMIT CLAIM']").click()

    await page.locator("//button[normalize-space()='YES']").click()


async def get_query_question(page:Page) -> str:
    see_query_question = None
    try:
        await page.locator("//button[normalize-space()='Case log']").click()
        await (await page.wait_for_selector(
            "//*[name()='circle' and @id='bg-icon']/ancestor::something/parent::div/parent::div/parent::div/div[2]/div[last()]/div[2]/div[3]//span[contains(text(),'...Show More')]",
            timeout=3000)).click()
        last_query_question_xp = "//*[name()='circle' and @id='bg-icon']/ancestor::something/parent::div/parent::div/parent::div/div[2]/div[last()]/div[2]/div[3]"
        see_query_question = await page.locator(last_query_question_xp).text_content()
        # close cross button
        await page.locator("//*[name()='path' and @id='cross-icon']").click()

    except TimeoutError:
        print('Checking Chats')
        'opening chat icon'
        await page.locator("(//img[@data-tip='Chat'])[last()]").click()
        # getting question - last question
        see_query_question = await page.locator("(//div[@class=' mt-1 GoMHIRgbsMpPdNHZPHNf']/span)[last()]").text_content()
        # close button
        await page.locator("(//div[contains(@class,'react-draggable')]//img)[2]").click()

    return see_query_question

async  def pre_auth_query_clearer(page, pdf_list):
    pdf_1, pdf_2, pdf_3 = pdf_list
    await page.locator("//h4[text()='Treatment']").click()
    await page.locator("//div[contains(text(),'Investigations')]/parent::div/following-sibling::h2/button").click()
    for pdf in pdf_list:
        await click_first_until_second_present(page=page,first_locator="//button[normalize-space()='Add Other Documents']",
                                               second_locator="//button[contains(@data-toggle,'collapse')][normalize-space()='ADD']")
        # await page.locator("//input[@id='otherInvest']").fill(remark)  # instead Null is autofill and uses as selector
        await page.locator("//button[contains(@data-toggle,'collapse')][normalize-space()='ADD']").click()
        await page.wait_for_selector("(//p[normalize-space()='Null'])[last()]")
        await page.set_input_files("//input[@type='file']", pdf)
        await asyncio.sleep(1)
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




def main(reg_multiline_str, set_timeout_is):
    asyncio.run(_main(reg_multiline_str, set_timeout_is=set_timeout_is))





if __name__ =="__main__":
    # main("1009299836")
    main()