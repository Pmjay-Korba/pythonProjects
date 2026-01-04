"""

first step is to open the Supply order page then select 'All Order' of the year which you want to get data than start the programme
like '2023-24' and 'All'

"""

import asyncio
from playwright.async_api import async_playwright, Page
from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
from bs4 import BeautifulSoup
import pandas as pd

from dkbssy.utils.colour_prints import ColourPrint


async def _main( set_timeout_is):
    page_indexes = await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='Supply Orders')
    # print(is_chrome_dev_open)

    # only for checking the approver site open
    # await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='Shaheed Veer Narayan Singh Ayushman Swasthya Yojna', cdp_port=9223)
    html = None
    async with async_playwright() as p:
        cdp_for_main = 9222
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{cdp_for_main}")
        context = browser.contexts[0]
        all_pages = context.pages

        page_index = page_indexes[0]  # selecting the first index of matching page
        page = all_pages[page_index]  # selecting the first PAGE of matching page

        page.set_default_timeout(set_timeout_is)
        page.set_default_navigation_timeout(set_timeout_is)
        html = await page.content()
    # print(html)

    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a", href=lambda h: h and "LPSupplyPosition.aspx" in h)

    results = []
    for a in anchors:
        href = a.get("href")
        text = a.get_text(strip=True)
        results.append({"text": text, "href": href})


    # for j in results:
    #     print(j)


    # return results
    urls = []
    for i in results:
        j = i['href'].split(",")[4]
        j = (j.replace('"', '')).replace(" ", "")
        url = f'https://dpdmis.in/faconline/LocalPurchases/{j}'
        urls.append(url)

    return urls


# --- Your XPaths ---
SUPPLY_ORDER_NUMBER = "//span[@title='Supply order number']"
EACH_ROW = "//th[text()='Sl. No.']/parent::tr/parent::tbody//tr[contains(@class,'gridView') and not(@class='gridViewHeader')]"
EACH_ROW_CODE = "//td[2]//tbody//tbody//td/a"
EACH_ROW_NAME = "//td[2]//tbody//tbody//td/label[@for='lblItemName']/a"
each_row_quantity = "//td[3]/span"

async def scrape_data(page:Page, url):
    each_order_data = []
    await page.goto(url)
    number = await page.locator(SUPPLY_ORDER_NUMBER).text_content()
    each_rox = await page.locator(EACH_ROW).all()
    # each_order_data["order_number"] = number
    # drugs_lists =[]
    for e in each_rox:
        sub_drug_lists ={}
        code = await e.locator("xpath=" + EACH_ROW_CODE).first.text_content()
        name = await e.locator("xpath=" + EACH_ROW_NAME).text_content()
        qty = await e.locator("xpath=" + each_row_quantity).text_content()

        # print(number, code, name, qty)
        sub_drug_lists['order_number'] = number
        sub_drug_lists['drug_code'] = code
        sub_drug_lists['drug_name'] = name
        sub_drug_lists['drug_quantity'] = qty

        each_order_data.extend([sub_drug_lists])

    print(each_order_data)
    print()
    return each_order_data



async def main_2(url_list):
    page_indexes = await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='Supply Orders')
    # print(is_chrome_dev_open)

    # only for checking the approver site open
    # await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='Shaheed Veer Narayan Singh Ayushman Swasthya Yojna', cdp_port=9223)
    async with async_playwright() as p:
        cdp_for_main = 9222
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{cdp_for_main}")
        context = browser.contexts[0]
        all_pages = context.pages

        page_index = page_indexes[0]  # selecting the first index of matching page
        page = all_pages[page_index]  # selecting the first PAGE of matching page

        # page.set_default_timeout(set_timeout_is)
        # page.set_default_navigation_timeout(set_timeout_is)

        page = await context.new_page()

        master_list =[]
        ColourPrint.print_yellow('len url', len(url_list))
        for n, url in enumerate(url_list, start=1):
            print(n, url)
            each_orders_is = await scrape_data(page, url)
            master_list.extend(each_orders_is)

        print(master_list)

        # Convert to DataFrame
        df = pd.DataFrame(master_list)

        # Save to Excel
        df.to_excel("supply_orders.xlsx", index=False)


# Example (run inside async environment)

# url_list = ['']
url_lists = asyncio.run(_main(20000))
asyncio.run(main_2(url_lists))
# print(u)
