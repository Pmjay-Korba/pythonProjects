import asyncio

from playwright.async_api import async_playwright, Page, TimeoutError,  Error as PlaywrightError

from EHOSP.ehospital_proper.colour_print_ehosp import ColourPrint
from EHOSP.tk_ehosp.alert_boxes import error_tk_box


async def _get_desired_page_indexes_in_cdp_async(user_title_of_page, cdp_port):
    """

    :param user_title_of_page: User defined page
    :param cdp_port: Port no. {9222}
    :return: list of index of page opened
    """
    title_of_error = "BrowserDev Error"
    browser_type_is = "BrowserDev"
    if int(cdp_port) == 9223:
        browser_type_is = "EdgeDev"
    elif int(cdp_port) == 9222:
        browser_type_is = "ChromeDev"
    try:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(f'http://localhost:{cdp_port}')
            context = browser.contexts[0]
            if not context:
                error_tk_box(error_title=title_of_error, error_message='No browser tab is opened')
                raise
            pages = context.pages
            print("Count of Pages", len(pages))

            # adding the same page indexes
            same_page_opened = []
            ColourPrint.print_blue(f"User defined page for {browser_type_is}:", user_title_of_page)
            for idx, page in enumerate(pages):
                # print()
                try:
                    title_extracted =await asyncio.wait_for(page.title(), timeout=5)
                    print(f'Page no.{idx} ->', title_extracted)
                    if title_extracted.strip() == user_title_of_page.strip():
                        same_page_opened.append(idx)

                except Exception:
                    print('time out in the function _get_desired_page')


            # raising error box if no title
            if not same_page_opened:
                err_msg = f'No tab opened with page title: "{user_title_of_page}" in {browser_type_is}. Try after Opening and Login'
                error_tk_box(error_title=title_of_error, error_message=err_msg)
                raise NameError(err_msg)

            # print('End')
            print('Same Page Indices = ', same_page_opened)
            return same_page_opened


    except PlaywrightError as e:
        if  "ECONNREFUSED" in str(e):
            err_msg = f'{browser_type_is} is not running.\n\nOpen {browser_type_is} and login in {user_title_of_page} than retry'
            error_tk_box(error_title=title_of_error, error_message=err_msg)
            raise ConnectionError(err_msg)

def get_desired_page_indexes_in_cdp_async_for_SYNC(user_title_of_page, cdp_port=9222) -> list:
    return asyncio.run(_get_desired_page_indexes_in_cdp_async(user_title_of_page=user_title_of_page, cdp_port=cdp_port))

async def get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page, cdp_port=9222) -> list:
   return await _get_desired_page_indexes_in_cdp_async(user_title_of_page=user_title_of_page, cdp_port=cdp_port)


# if __name__ == "__main__":
#     asyncio.run(get_desired_page_indexes_in_cdp_async_for_ASYNC('Shaheed Veer Narayan Singh Ayushman Swasthya Yojna'))
