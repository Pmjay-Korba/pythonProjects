import asyncio
import json
import time
import random
from playwright.async_api import async_playwright, Page, TimeoutError, expect
from TMS_Process.process.claim_clearer import is_home_page, select_ALL_and_search
from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
from TMS_new.async_tms_new import select_ors
from dkbssy.utils.colour_prints import ColourPrint, message_box
from tms_playwright.page_objs_tms.tms_xpaths import files_to_upload_dict
from TMS_Process.process.file_folder_searcher import search_file_all_drives, ProjectPaths
from TMS_Process.process.pdf_creator import generate_pdfs_from_txt_list, delete_pdf


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
        # checking if the last save is in list
        if last_saved and last_saved in multi_lined_list:
            start_index = multi_lined_list.index(last_saved)+1
            print("Start index: ",start_index)


        for registration_no in multi_lined_list[start_index:]:
            if registration_no.strip() == "":
                print("Blank")
                continue
            time.sleep(5)
            ColourPrint.print_green(message_box(registration_no))

            pdf_1mb, pdf_2mb = _create_files_pdfs(registration_no=registration_no)

            await is_home_page(page=page)
            await select_ALL_and_search(page=page, registration_no=registration_no)

            'Looking if queried or resolved'
            caseview = await page.locator("//li[@class='ES8GosCR9dsXoNoSy9So he8vrs1JR2h4h_PgLoHc ']").text_content()
            if 'caseview' in caseview.strip().lower() :
                ColourPrint.print_blue(f'Skipped: {registration_no}')
                continue  # skipping non - queried

            await claim_query_clearer(page=page, registration_no=registration_no, pdf_1mb=pdf_1mb, pdf_2mb=pdf_2mb)

            delete_pdf(pdf_1mb)
            delete_pdf(pdf_2mb)


            # ✅ update progress after each successful run
            update_last_saved(registration_no=registration_no, CURRENT_SAVE=CURRENT_SAVE)

def _create_files_pdfs(registration_no):
    ColourPrint.print_yellow(message_box('Please wait. Scanning drives...'))
    text_file_path = search_file_all_drives(filename=registration_no)
    print(json.dumps(text_file_path, indent=2))
    pdf_1mb, pdf_2mb = generate_pdfs_from_txt_list(text_file_path)
    return pdf_1mb, pdf_2mb

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


def main(reg_multiline_str):
    # l = reg_multiline_str.split()
    # for j in l :
    #     if j.strip() == "":
    #         print("Blank")
    #         continue
    #     time.sleep(2)
    #     ColourPrint.print_green(message_box(j))
        asyncio.run(_main(reg_multiline_str))
    # input_reg = str(input('ENTER REG NO: '))
    # asyncio.run(_main(reg_no))



if __name__ =="__main__":
    # main("1009299836")
    main()