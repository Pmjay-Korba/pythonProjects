import asyncio
import time
from playwright.async_api import async_playwright, Page, TimeoutError, expect
from TMS_Process.process.claim_clearer import is_home_page, select_ALL_and_search
from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
from TMS_new.async_tms_new import select_ors
from dkbssy.utils.colour_prints import ColourPrint
from tms_playwright.page_objs_tms.tms_xpaths import files_to_upload_dict


async def main(cdp_port=9222):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{cdp_port}")
        context = browser.contexts[0]
        all_pages = context.pages

        pages_indexes = await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='PMJAY - Provider',
                                                                              cdp_port=cdp_port)
        page_index = pages_indexes[0]  # selecting the first index of matching page

        page = all_pages[page_index]  # selecting the first PAGE of matching page
        page.set_default_timeout(10000)


        await asyncio.sleep(10)

        # for registration_no in registration_no_list:
        #     print(registration_no)
        await is_home_page(page=page)

        # await select_ALL_and_search(page=page, registration_no=registration_no)
        await page.locator("//div[@class=' xB2wY4KO4UlXm9Li88Da P3Oql_qNUCLDWHYyNbII']").click()
        # counts = int(await page.locator("//h1[@class=' xB2wY4KO4UlXm9Li88Da V0N_rBD9HSG_V8DXM7fh']").text_content())
        # for _ in range(counts):
        while True:
            await claim_submitter(page=page)

async def claim_submitter(page):
    # print(await( await(page.wait_for_selector("//div[@class='weiskrL_wfv7iVk5WPKd modal-body']//div[@class='tGmaR1iE3EpIOpxAsaaA']")).text_content()))

    # async with page.expect_response("https://apisprod.nha.gov.in/pmjay/provider/nproviderdashboard/V3/beneficiary/list") as response_info:
    #     pass
    # val = await response_info.value
    # print(val)

    await page.locator("(//something)[1]").click()

    await page.locator("//input[@id='Hospital Bill Number']").fill(" ")
    # time.sleep(2)
    await page.locator("//button[normalize-space()='SAVE']").click()
    await page.wait_for_selector("//span[normalize-space()='Hospital Bill Details saved successfully.']")
    # time.sleep(2)
    await page.locator("//span[contains(@class,'qNscgo05cXwFxxXbkhOu')]").click()
    # time.sleep(2)
    await page.locator("//button[normalize-space()='Preview & Claim']").click()
    # time.sleep(2)
    await page.locator("//button[normalize-space()='SUBMIT CLAIM']").click()
    # time.sleep(2)
    await page.locator("//button[normalize-space()='YES']").click()
    # time.sleep(2)



if __name__ =="__main__":
    asyncio.run(main())
