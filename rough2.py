import asyncio

from playwright.async_api import async_playwright

from TMS_Process.process.claim_clearer_RF import is_home_page
from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC


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

        await page.get_by_placeholder("Search").fill("1006464009")
        await page.get_by_placeholder("Search").locator('..').locator('span').click()


if __name__ == "__main__":
    asyncio.run(main())