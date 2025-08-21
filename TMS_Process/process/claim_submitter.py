import asyncio
import time
from playwright.async_api import async_playwright, Page, TimeoutError, expect
from TMS_Process.process.claim_clearer import is_home_page, select_ALL_and_search
from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
from TMS_new.async_tms_new import select_ors
from dkbssy.utils.colour_prints import ColourPrint
from tms_playwright.page_objs_tms.tms_xpaths import files_to_upload_dict


async def main(registration_no_list, cdp_port=9222):
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

        for registration_no in registration_no_list:
            print(registration_no)
            await is_home_page(page=page)

            await select_ALL_and_search(page=page, registration_no=registration_no)

            await claim_submitter(page=page)

async def claim_submitter(page):
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
    print(await( await(page.wait_for_selector("//div[@class='weiskrL_wfv7iVk5WPKd modal-body']//div[@class='tGmaR1iE3EpIOpxAsaaA']")).text_content()))


if __name__ =="__main__":
    reg = """1011752226
1011763908
1011765957
1011766328
1011782643
1011782732
1011784431
1011784715
1011784986
1011787078
1011791286
1011792116
1011796787
1011797394
1011800067
1011801426
1011808332
1011815594
1011841030
1011843037
1011855029
1011857132
1011863198
1011864536
1011867434
1011873912
1011874392
1011875882
1011879674
1011882392
1011882598
1011902901
1011913801
1011916911
1011928874
1011931086
1011931191
1011935482
1011936685
1011936979
1011950014
1011951097
1011952755
1011954416
1011969772
1011971994
1011979441
1011980646
1011983714
1011998526
1012003368
1012007505
1012015955
1012027496
1012061916
1012063811
1012101500
1012105785
1012182865
1012205772
1012269629
1012270029
1012270508
1012271152
1012282410
1012297826
1012298346
1012312964
1012313192
1012313677
1012315082
1012319420
1012397842
1009935314
1011131136
1011231010
1011651449
1011936600
1012238815
1011369815
1010394687
1012339995
1012371685
1012400267
1012438472
1012441280
1012307674""".split('\n')
    asyncio.run(main(registration_no_list=reg))
