import asyncio
import json
import math
import os
import time
from datetime import datetime, timedelta

from TMS_new.async_tms_new.b_new_async import both_delete
from b_new_async import type_list_generate, load_excel_sheet_and_return_list, compare_excel_and_json, getting_query_and_discharge_details
import openpyxl
import select_ors
from dkbssy.utils.colour_prints import ColourPrint
from playwright.async_api import async_playwright, Page, TimeoutError
from tms_playwright.discharge_to_be_done.detail_list_getter_all import is_file_older_than_2_hours, save_to_json, \
    read_from_json, save_to_json
from select_ors import JSON_FILE_PATH, EXCEL_FILE_PATH

async def spreadsheet_download_as_excel_and_load_openpyxl_wb(page, sheet_url):
    # Navigate to the Google Sheets URL
    await page.goto(sheet_url)
    # Click on "File" -> "Download" -> "Microsoft Excel (.xlsx)"
    await page.click("text=File")
    await asyncio.sleep(0.5)
    await page.click("text=Download")
    await asyncio.sleep(0.5)
    await page.click("text=Microsoft Excel (.xlsx)")
    # Expect the download to start and capture the download event
    async with page.expect_download() as download_info:
        pass  # The download should automatically start after clicking

    # Get the download object
    download = await download_info.value  # Waits until the download is complete
    # Get the suggested filename (e.g., "Sheet1.xlsx")
    filename = download.suggested_filename
    print(filename)
    # Save the file to your desired folder with the same name
    filepath = f"..\\async_tms_new\\download\\{filename}"
    await download.save_as(filepath)

    return openpyxl.load_workbook(filepath)


def import_json(JSON_FILE_PATH):
    # json_file_path = f"..\\async_tms_new\\download\\file_json.json"
    older_than_2_hours = is_file_older_than_2_hours(JSON_FILE_PATH)
    # ColourPrint.print_yellow('Older! Need download? ', older_than_2_hours)
    if not older_than_2_hours:
        # File is less than 2 hours old, read from the file
        pre_auth_query_list_generated, claim_query_list_generated, under_treatment_list_generated = read_from_json(JSON_FILE_PATH)
        return pre_auth_query_list_generated, claim_query_list_generated, under_treatment_list_generated
    else:
        return False


async def check_count_of_tab(context):
    count_of_pages = len(context.pages)
    if count_of_pages < 2:
        raise ValueError('Count of browser tab is les than two. Duplicate it and than restart')


async def check_connected_pages(browser, play):
    # Wait until at least one context with one page is available
    for _ in range(10):  # Try for up to 10 * 0.5s = 5 seconds
        if browser.contexts:
            context = browser.contexts[0]
            if context.pages:
                page = context.pages[0]
                return context, page
        await asyncio.sleep(0.5)

    print("❌ No active page found. Please make sure a tab is open.")
    await browser.close()
    await play.stop()
    return None

async def check_page_title_same(context, title_of_page, tab_count=2):
    ColourPrint.print_green('Opened pages count', len(context.pages))
    matched_page = []
    for page in context.pages:
        page_title = await page.title()
        print('Title of page: ', page_title.strip())
        if page_title.strip() == title_of_page.strip():
            matched_page.append(page)
    if not len(matched_page) >= tab_count:
        raise ValueError(f"Tab count is less than the desired {tab_count}. Actual count of open page is {len(matched_page)}")
    return matched_page




async def main():
    play = await async_playwright().start()
    browser = await play.chromium.connect_over_cdp('http://localhost:9222')

    # 'already exister below so not await'
    # context = browser.contexts[0]
    # page = context.pages[0]
    # page.set_default_timeout(5000)

    context, page = await check_connected_pages(browser=browser, play=play)
    page.set_default_timeout(5000)


    cdp_chrome_title = await page.title()
    print(f"✅ Found CDP Chrome page title: {cdp_chrome_title}")

    'download the spreadsheet'
    spread_page2 = await context.new_page()
    # work_book = await spreadsheet_download_as_excel_and_load_openpyxl_wb(page=spread_page2,sheet_url='https://docs.google.com/spreadsheets/d/1vhjV0rcODJ4lGYJBHENMnHFvqHgK25dQRt9SVpr_9N4/edit?gid=0#gid=0')
    await spread_page2.close()
    # print(work_book)

    # 'temp save will return the lists if less than 2 hours old or return False if older'
    # temp_saved_json = import_json()
    # if not temp_saved_json:
    #     ColourPrint.print_pink('Older than 2 hours')

    'Check the count of browser tab'
    await check_count_of_tab(context=context)

    'check the same tab opened or not'
    ColourPrint.print_green('-'*50)
    page_tab_count = 3
    matching_pages = await check_page_title_same(context=context, tab_count=page_tab_count, title_of_page='PMJAY - Provider' )
    ColourPrint.print_green('-'*50)
    # print(matching_pages)

    page, page2, page3, page4 = matching_pages


    'temp save will return the lists if less than 2 hours old or return False if older'
    temp_saved_json = import_json(JSON_FILE_PATH=JSON_FILE_PATH)
    ColourPrint.print_pink('Json response:', temp_saved_json)
    if not temp_saved_json:
        ColourPrint.print_pink('Older than 2 hours')
        pre_auth_query_list_generated, claim_query_list_generated, under_treatment_list_generated = await asyncio.gather(
            type_list_generate(page=page,
                               case_type_button=select_ors.PreauthorizationQueriedOnly,
                               current_status="Preauthorization Queried",
                               patient_status_field_xpath=select_ors.PreauthorizationQueried_With
            ),
            type_list_generate(page=page2,
                               case_type_button=select_ors.ClaimsQueriedOnly,
                               current_status="Claims Queried",
                               patient_status_field_xpath=select_ors.ClaimsQueried_With
            ),
            type_list_generate(page=page3,
                               case_type_button=select_ors.underTreatmentOnly,
                               current_status='Under Treatment',
                               patient_status_field_xpath=select_ors.underTreatmentWith_
            )
        )
        save_to_json(pre_auth_query_list_generated,claim_query_list_generated,under_treatment_list_generated,f"..\\async_tms_new\\download\\file_json.json")
        ColourPrint.print_green('JSON SAVED')
    else:
        pre_auth_query_list_generated, claim_query_list_generated, under_treatment_list_generated =  temp_saved_json

    'joining the both query'
    both_query_list = pre_auth_query_list_generated + claim_query_list_generated

    'getting the discharge sheet datas an comparing'
    discharge_row_datas = load_excel_sheet_and_return_list(EXCEL_FILE_PATH=EXCEL_FILE_PATH, excel_sheet_name='Pend Dischg2')
    add_discharge, delete_discharge = compare_excel_and_json(excel_sheet_data_list=discharge_row_datas, json_retrieved_list=under_treatment_list_generated)
    print('mmmmmmmm 1')

    'getting the query sheet datas an comparing'
    query_row_data = load_excel_sheet_and_return_list(EXCEL_FILE_PATH=EXCEL_FILE_PATH, excel_sheet_name='QUERY2')
    add_query, delete_query =compare_excel_and_json(excel_sheet_data_list=query_row_data, json_retrieved_list=both_query_list)
    print('mmmmmm 2 ')

    "for deleting both query and discharge"
    # workbook_after_both_deletion = both_delete(discharge_delete_list=delete_discharge, query_delete_list= delete_query,excel_file_path=EXCEL_FILE_PATH, discharge_sheet_name="Pend Dischg2", query_sheet_name="QUERY2")
    print('mmmm 3')

    "divided lists"
    len_discharge = len(add_discharge)
    add_discharge1, add_discharge2 = add_discharge[:math.ceil(len_discharge/2)], add_discharge[math.ceil(len_discharge/2):]

    len_query = len(add_query)
    add_query1, add_query2 = add_query[:math.ceil(len_query/2)], add_query[math.ceil(len_query/2):]
    "adding the additions"
    query_scrape_data_1, query_scrape_data_2, discharge_scrape_data_1, discharge_scrape_data_2 =  await asyncio.gather(
        getting_query_and_discharge_details(page=page3, case_numbers_list=add_query1),
        getting_query_and_discharge_details(page=page2, case_numbers_list=add_query2),
        getting_query_and_discharge_details(page=page, case_numbers_list=add_discharge1),
        getting_query_and_discharge_details(page=page4,case_numbers_list=add_discharge2),
    )

    query_all_data = add_query1 + add_query2
    discharge_all_data = discharge_scrape_data_1 + discharge_scrape_data_2

    await play.stop()





if __name__ == '__main__':
    asyncio.run(main())