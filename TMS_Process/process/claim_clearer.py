"""# only for RF query now"""


import asyncio

from playwright.async_api import async_playwright, Page, TimeoutError, expect
from urllib3.util.wait import wait_for_socket

from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
from TMS_new.async_tms_new import select_ors
from dkbssy.utils.colour_prints import ColourPrint
from tms_playwright.page_objs_tms.tms_xpaths import files_to_upload_dict


async def main(registration_no, cdp_port):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{cdp_port}")
        context = browser.contexts[0]
        all_pages = context.pages

        pages_indexes = await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='PMJAY - Provider',
                                                                              cdp_port=cdp_port)
        page_index = pages_indexes[0]  # selecting the first index of matching page

        page = all_pages[page_index]  # selecting the first PAGE of matching page
        page.set_default_timeout(10000)

        # checking is home page
        await is_home_page(page=page)

        await select_ALL_and_search(page=page, registration_no=registration_no)

        # only for RF qquery now
        await query_process(page=page)


async def is_home_page(page:Page):
    body_texts = await page.locator("//body").text_content()
    if "Your Hospital Dashboard" not in body_texts:
        await page.locator(select_ors.homeSVG).click()
        await expect(page.locator(select_ors.yourHospitalDashboard)).to_be_visible(timeout=60000)
        try:
            await (await page.wait_for_selector(select_ors.searchBox, timeout=2000)).fill('test')
            total_amount = (await (await page.wait_for_selector("//h1[@class=' MMPSPNfakB2FCrcdJFVH V0N_rBD9HSG_V8DXM7fh']//span[@class='BUnqLA8pVHiNDXGN4301']")).text_content())
            print(total_amount)
            # await asyncio.sleep(2)

        except TimeoutError:
            await page.reload()
            await asyncio.sleep(2)
            print('Reloaded')


async def select_ALL_and_search(page:Page, registration_no):
    await page.locator(select_ors.patientStatusInput).type('ALL')
    await page.keyboard.press("Enter")
    # typing the case number
    await page.locator(select_ors.searchBox).fill(registration_no)  # search box = //input[@placeholder='Search']
    # clicking the search icon
    await expect(page.locator(select_ors.searchIcon)).to_be_enabled()
    await page.locator(select_ors.searchIcon).click()
    await page.locator(select_ors.searchIcon).click()
    await page.locator(select_ors.searchIcon).click()

    while True:
        try:
            # await page.wait_for_selector("//p[contains(text(),'Registration ID:')]", timeout=2000)  # all ids labels
            await page.wait_for_selector(f"//strong[contains(text(),'{registration_no}')]", timeout=2000)  # all ids labels
            # print('cccccccccccccccccccccc')
            break
        except TimeoutError:
            ColourPrint.print_yellow("Timeout error -->")
            await page.locator(select_ors.searchIcon).click()

    searched_reg_no_xp = f"// strong[normalize-space()='{registration_no}']/parent::p/parent::div/following-sibling::div//*[name()='svg']"
    # await page.locator(select_ors.searchIcon).click()
    await page.locator(searched_reg_no_xp).click()

async def query_process(page:Page):
    await page.locator("//span[normalize-space()='Query Response']").click()  # clicking the query bar
    response_text = 'RF query not applicable from. Hospital end. Kindly provide necessary details if so. Thanks.'
    files_to_upload_xp = "//input[@id='SupportingDoc2']"
    file_path = r"C:\Users\HP\Downloads\RF.pdf"
    await page.set_input_files(files_to_upload_xp, file_path)
    await page.locator("//input[@id='Remarks']").fill(response_text)
    await page.locator("//button[normalize-space()='SAVE']").click()
    await page.wait_for_selector("//span[normalize-space()='Query Response saved successfully.']")
    await page.locator("//button[normalize-space()='SUBMIT CLAIM']").click()
    await page.locator("//button[normalize-space()='YES']").click()
    await asyncio.sleep(3)



if __name__ == '__main__':
    l = """1007009307
    1008506061
    1008648428
    1006910087
    1008660745
    1006962218
    1003407721""".split('\n')
    for i in l:
        asyncio.run(main(registration_no=f'{i.strip()}', cdp_port=9222))