import asyncio

from playwright.async_api import async_playwright, Page, TimeoutError, expect
from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
import select_ors
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
        await expect(page.locator(select_ors.yourHospitalDashboard)).to_be_visible()
        try:
            await (await page.wait_for_selector(select_ors.searchBox, timeout=2000)).fill('test')
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
    await page.locator(select_ors.searchIcon).click()
    await expect(page.locator(select_ors.searchIcon)).to_be_enabled()

    while True:
        try:
            await page.wait_for_selector("//p[contains(text(),'Registration ID:')]", timeout=2000)  # all ids labels
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
    file_path = r"C:\Users\HP\Desktop\RF.pdf"
    await page.set_input_files(files_to_upload_xp, file_path)
    await page.locator("//input[@id='Remarks']").fill(response_text)
    await page.locator("//button[normalize-space()='SAVE']").click()
    await page.wait_for_selector("//span[normalize-space()='Query Response saved successfully.']")
    await page.locator("//button[normalize-space()='SUBMIT CLAIM']").click()
    await page.locator("//button[normalize-space()='YES']").click()
    await asyncio.sleep(3)



if __name__ == '__main__':
    l = """1006721522
    1007022008
    """.split('\n')
    for i in l:
        asyncio.run(main(registration_no=f'{i.strip()}', cdp_port=9222))