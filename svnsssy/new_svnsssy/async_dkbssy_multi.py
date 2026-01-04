import asyncio
import time

from playwright.async_api import async_playwright

from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
from dkbssy.dk_pages.sixth_page import batch_divide
from dkbssy.utils import name_for_date_check_gmc
from dkbssy.utils.colour_prints import ColourPrint, message_box
from dkbssy.utils.excel_utils import ExcelMethods
from dkbssy.utils.sqlite_updation_long import process_all_cases_to_db_3
from svnsssy.new_svnsssy.amount_update_request import main_aiohttp_optimized
from svnsssy.new_svnsssy.async_dkbssy import split_multiline_to_list, retrieve_case_number, select_department_and_dates, \
    stuck_display_multi, check_already_initiated, scrape_incentive_case_details, radio_click, \
    get_cat_and_names_for_entry, \
    entry_proper, Status, StatusText, original_site_query_modify, _scrape_amount, process_scraped_data, \
    indent_json_print, check_box_and_submit, stuck_list, TempIncentiveSave, update_sql_in_auto_2


async def handle_dialog(dialog):
    print(f"Dialog appeared with message: {dialog.message}")
    await dialog.accept()


async def _main(all_incentive_multiline, set_timeout_is, num_of_pages_to_create = 2):
    page_indexes = await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='Shaheed Veer Narayan Singh Ayushman Swasthya Yojna')
    # print(is_chrome_dev_open)

    # only for checking the approver site open
    # await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='Shaheed Veer Narayan Singh Ayushman Swasthya Yojna', cdp_port=9223)

    "completing the 'fullWebComplete' to database if last cases the error in completing"
    temp_inc_save = TempIncentiveSave()
    cache_data = temp_inc_save.get_temp_json_data()
    if cache_data:
        process_all_cases_to_db_3(cache_data)


    # num_of_pages_to_create = 2

    # from_date = '01-08-2022'
    from_date = '2022-08-01'
    # to_date = '31-12-2023'
    to_date = '2023-12-31'

    # check upload file -> skipping in new modified
    # checked_file_path = check_file_path(attach_file_path=attach_upload_file_path)
    print()

    # splits to individual data line
    incentive_cases_list = split_multiline_to_list(all_incentive_multiline=all_incentive_multiline)
    # indent_json_print(incentive_cases_list)

    # function ran
    name_for_date_check_gmc.checker_with_dict_output(incentive_cases_list)


    master_of_sub_incentive_list = batch_divide(num_of_pages_to_create, incentive_cases_list)

    # print(master_of_sub_list)


    async with async_playwright() as p:
        cdp_for_main = 9222
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{cdp_for_main}")
        context = browser.contexts[0]
        all_pages = context.pages

        page_index = page_indexes[0]  # selecting the first index of matching page
        page = all_pages[page_index]  # selecting the first PAGE of matching page

        page.set_default_timeout(set_timeout_is)
        page.set_default_navigation_timeout(set_timeout_is)


        # ⚡ Attach dialog handler exactly once
        # page.on("dialog", handle_dialog)

        depart_choice = ExcelMethods().entry_department()

        """SELECTING THE DATE AND DEPARTMENT AND SEARCHING THE ALL CASE DATA TO MATCH THE STUCK LISTS REMOVAL
            DOING THE ABOVE IN MAIN PAGE --> Mainly removing the queried done and marked reinitated"""
        await select_department_and_dates_and_stuck_remover(page=page, depart_name=depart_choice, from_date=from_date,
                                                            to_date=to_date)

        "alerting the message those which are not queried and cleared"
        stuck_display_multi()


        all_data_of_all_batches = await entry_proper_multi_batch(all_batch_list=master_of_sub_incentive_list,context=context, num_of_pages_to_create=num_of_pages_to_create,
                                       depart_choice=depart_choice,from_date=from_date, to_date=to_date, set_timeout = set_timeout_is)
        indent_json_print(all_data_of_all_batches)

        flatten_list = flatten_3level_to_2level(all_data_of_all_batches)
        indent_json_print(flatten_list)

        "saving in temporary file"
        temp_inc_save.save_temp_before_db(flatten_list)

        "adding to DB3"
        process_all_cases_to_db_3(flatten_list)
        ColourPrint.print_green('Completed DB done')

        "updating the status json"
        for data in flatten_list:
            incentive_case_number = data[0]
            Status().set_status(case_number=incentive_case_number, status_text=StatusText.EXCEL_DB_SAVED)
        'cleaned the temp file'
        temp_inc_save.clean_temp_file()
        ColourPrint.print_green(message_box('All saved'))

        "Updating the incentive auto 2 from db3"
        update_sql_in_auto_2()

        "updating auto2 globally"
        await main_aiohttp_optimized()


def flatten_3level_to_2level(_3level_list):
    _2level_list = [inner_list for group_list in _3level_list for inner_list in group_list]
    return _2level_list

async def select_department_and_dates_and_stuck_remover(page, depart_name, from_date, to_date):
    second_page_url = "https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduledme.aspx"
    speciality_DD_xpath = '//*[@id="ctl00_ContentPlaceHolder1_speciality"]'
    from_date_xpath = '//*[@id="ctl00_ContentPlaceHolder1_fdate"]'
    to_date_xpath = '//*[@id="ctl00_ContentPlaceHolder1_tdate"]'
    search_button_xpath = '//*[@id="ctl00_ContentPlaceHolder1_SearchCases"]'

    # page.set_default_timeout(300000)

    await page.goto(second_page_url)
    await page.select_option(speciality_DD_xpath, depart_name)
    await page.locator(from_date_xpath).fill(from_date)
    await page.locator(to_date_xpath).fill(to_date)
    # Correct usage of expect_response
    async with page.expect_response(
            lambda response: 'incentivemoduledme.aspx' in response.url and response.status == 200) as resp_info:
        await page.locator(search_button_xpath).click()

    response = await resp_info.value
    data = await response.text()  # or await response.json() if JSON

    'getting the incomplete data from json'
    incomplete = stuck_list()

    for case_number in incomplete:
        if f'{case_number}</a>' in data:
            Status().delete_status(case_number=case_number)



async def entry_proper_one_batch(incentive_cases_list_one_batch, page, batch_id, depart_choice,from_date,to_date):
    # getting each incentive case number

    """Alerting the incomplete incentives"""
    # stuck_display_multi()

    one_batch_collected_data_for_db = []
    for idx, case_number_with_data in enumerate(incentive_cases_list_one_batch, start=1):
        case_number = retrieve_case_number(case_number_with_data)
        try:
            # case_number = retrieve_case_number(case_number_with_data)
            # await asyncio.sleep(1)
            ColourPrint.print_pink(f"[Batch {batch_id}] Case Number {idx} Is:", case_number)

            "QUERY MODIFY IF STUCK AND NOT SHOWING IN BOTH SITES"
            ColourPrint.print_turquoise("Query Modify")
            # query_modify = f'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApViewDME.aspx?ci={case_numberw}&{amount}'
            query_modify = f'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApViewDME.aspx?ci={case_number}'
            ColourPrint.print_blue(f"[Batch {batch_id}]", query_modify)

            # "CHECKING THE MANUAL QUERY WAS CLEARED METHOD INSIDE THE SELECT DEPARTMENT"
            await select_department_and_dates_and_stuck_remover(page=page, depart_name=depart_choice, from_date=from_date, to_date=to_date)


            await check_already_initiated(page, case_number)  # return true

            main_master_c_num_with_name_amt_cat_e_code = []
            details_list = list(await scrape_incentive_case_details(page=page))
            # print(details_list)
            main_master_c_num_with_name_amt_cat_e_code.extend(details_list)  # adding the case details in the main master

            await radio_click(page=page)
            # await selection_of_category()
            final_cat_and_names = get_cat_and_names_for_entry()
            # print(f'{final_cat_and_names=}')

            """Entry is doing here"""
            await entry_proper(page, final_cat_and_names)
            Status().set_status(case_number=case_number, status_text=StatusText.INITIATED_DONE)

            await check_box_and_submit(page=page)

            "APPROVER SITE WORKS"
            await approver_raise_query_multi(case_number=case_number)

            "Original Site"
            await original_site_query_modify(page=page, case_number=case_number)

            "getting the amounts to be used in db"
            incentive_received_data = await _scrape_amount(page=page, case_number=case_number)
            #  [('SURINDAR LAL CHANDRA', 'डाटा एंट्री ऑपरेटर', 'DME55173655', '22.1'), ('Yamini Verma', 'डाटा एंट्री ऑपरेटर', 'DME55173200', '22.1'), ('KUMARI JYOTI LAHRE', 'डाटा एंट्री ऑपरेटर', 'DME55173036', '22.1'), ('SUMITRA KURREY', 'डाटा एंट्री ऑपरेटर', 'J55173309', '22.1'), ('Mr. Kiran Kumar Sahu', 'डाटा एंट्री ऑपरेटर', 'J55172798', '22.1'), ('K. Damodar', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020110', '1.54'), ('L.Kondiya', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020107', '1.54'), ('Bal Chainya', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020105', '1.54'), ('Smt. Shushila Bai', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020103', '1.54'), ('Ankaiya', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020093', '1.54'), ('Smt. Achamma Bai', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020090', '1.54'), ('Smt. Chandrika Bai', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020088', '1.54'), ('Mongra Tandon', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '04170150044', '1.54'), ('reman singh kanwar', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '07170250453', '1.54'), ('Mithlesh Kumar Markam', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '07170250399', '1.54'), ('V. Kondiya', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020092', '1.54'), ('Panch Ram Nirmalkar', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020091', '1.54'), ('Shri Shyam Das Mahant', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020087', '1.54'), ('Shri Amar Das', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020086', '1.54'), ('Shri Shiv Kumar Sarthi', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020084', '1.54'), ('Shri Krishna Kumar Tripathi', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020082', '1.54'), ('mohendra kumar janardan', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '04170150084', '1.54'), ('RAVINDRA KUMAR PANDEY', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '04170150035', '1.54'), ('Shri S.N.Shriwas', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020100', '1.54'), ('Shri Sunil Kumar Channe', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020099', '1.54'), ('Shri H.P.Tiwari', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020098', '1.54'), ('Shri C.P. Chandra', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020097', '1.54'), ('S SHANKAR RAO', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020189', '1.54'), ('PUSHPENDRA KUMAR', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020184', '1.54'), ('Smt.Lata Chandra', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020137', '1.54'), ('Shri Maheshwar Prasad Tandon', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020131', '1.54'), ('Anand Singh Rathiya', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517857', '1.54'), ('Smt. Sant Ram Kashyap', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020095', '1.54'), ('Komal Dewangan', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517589', '1.54'), ('PRATIBHA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517615', '1.54'), ('BAJANTI', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517614', '1.54'), ('SUNITA RATHORE', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517613', '1.54'), ('AAKANKSHA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517610', '1.54'), ('Mrs. ANAMIKA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517055', '1.54'), ('Mrs. BASANTI RATHIYA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517028', '1.54'), ('KU. PRIYA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517136', '1.54'), ('MAHENDRA KUMAR', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N55171003', '1.54'), ('Mr. BALDEV SINGH', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517085', '1.54'), ('Mr .AVINASH KUMAR BANJARE', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517084', '1.54'), ('Mr. MONESHWAR CHANDRA RATHIYA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517083', '1.54'), ('KUMARI SHREMATI', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517056', '1.54'), ('RAMANAND', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517042', '1.54'), ('RAJESH', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517032', '1.54'), ('Narendra Kumar Kanwar', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '04170140534', '2.95'), ('Manish Singh', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170011626', '2.95'), ('Jyoti Porte', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517990', '2.95'), ('Bhanu Priya Chauhan', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517989', '2.95'), ('KIRAN CHANDRA', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517979', '2.95'), ('TULSI YADAV', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '0617009003', '2.95'), ('NEELIMA NISHAD', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170050074', '2.95'), ('ASHA KINDO', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '03170050126', '2.95'), ('Anita Yadav', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '22170040038', '2.95'), ('Smt. Bhavana Bansiyar', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '15170200090', '2.95'), ('Ku. Har Bai Khunte', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '14170011702', '2.95'), ('vinita tigga', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '12170050188', '2.95'), ('KU. ANJANA KUJUR', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '11170260055', '2.95'), ('SAROJ RATHOR', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '09170160077', '2.95'), ('Neelam Kanwar', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '08170040064', '2.95'), ('Smt.Nirmala Miri', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '07170250081', '2.95'), ('SMT NAMITA PATEL', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020176', '2.95'), ('ku Kiran Sahu', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020161', '2.95'), ('Ku.Marget Bishwash', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020153', '2.95'), ('Ku.Jyoti Gual', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020143', '2.95'), ('Smt Bharti Markam', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020142', '2.95'), ('Ku. Sandhya Nair', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020124', '2.95'), ('PREETI SONWANI', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170011771', '2.95'), ('MANJULATA KANWAR', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '04170150162', '2.95'), ('SUSHILATA RATHIYA', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '04170140436', '2.95'), ('DIPTI LAKRA', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '04170140331', '2.95'), ('Smt.DIVYA ALKA TOPPO', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '04170060068', '2.95'), ('Sanjaya Kumar Tiwari', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517515', '2.95'), ('PAWAN KUMAR PATEL', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517809', '2.95'), ('VANDANA SAMUEL', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020614', '2.95'), ('CHANDRAKANTA SHRIVASTAV', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020507', '2.95'), ('PUSHPA BAG', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020500', '2.95'), ('Deepa sahu', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020472', '2.95'), ('Priti Masih Upma Kumar', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '15170200071', '2.95'), ('SMT. PHULKUMARI TOPPO', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020668', '2.95'), ('Smt. Sarika Tirpude Ramteke', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020665', '2.95'), ('PRIYA VERMA', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020641', '2.95'), ('Victoria Gardia', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170010273', '2.95'), ('Smt.Seema Rani Lajras', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020063', '2.95'), ('Rajni Kiran Kispotta', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '11170010433', '2.95'), ('Sanjay Das Manikpuri', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517599', '2.95'), ('Neelu Chaudhary', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517492', '2.95'), ('Radhe Shyam Kashyap', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'AI55170022', '2.95'), ('Amarjeet Kour', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '19170040056', '2.95'), ('Smt. Varnita Zilkar', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '15170200084', '2.95'), ('Dr. Priyanka Ekka', 'सभी फिजिशियन / सर्जन', '05530010030', '198.9'), ('Dr Ankita Kapoor', 'सभी फिजिशियन / सर्जन', '05530010028', '198.9'), ('DR ARUNIKA SISODIYA', 'सभी फिजिशियन / सर्जन', '05170020182', '198.9'), ('Dr. V.Agrawal', 'सभी फिजिशियन / सर्जन', '05170020043', '198.9'), ('Dr.Sumit Gupta', 'सभी फिजिशियन / सर्जन', '05170020187', '198.9'), ('MAHENDRA KUMAR', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '05170011797', '2.49'), ('dinesh kumar patel', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '09530010377', '2.49'), ('Smt.Bhagwati Koshle', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '09170010257', '2.49'), ('ARUN KUMAR KANWAR', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '07170021387', '2.49'), ('SMT DURGESHWARI KARSH', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '06170050083', '2.49'), ('SHIVSHANKAR SINGH KANWAR', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '05170060099', '2.49'), ('Shri C.L. Dixena', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '05170020117', '2.49'), ('Shri Sushil kumar miri', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '03170010366', '2.49'), ('Santosh Kumar Singh', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', 'AI55170030', '2.49'), ('Smt. Reena Verma', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', 'AI55170024', '2.49'), ('Smt. Pinky Singh', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '06170100054', '2.49'), ('Shri Dildar Sahish', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '05170020054', '2.49'), ('Haricharan Jangde', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '05170010396', '2.49'), ('Pratima Sahu', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', 'N5517593', '2.49'), ('Geeta patel', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', 'J55172863', '2.49'), ('ACHCHHE KUMAR PATLEY', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '04170150173', '2.49'), ('Dr. manoj Kumar', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010029', '15.47'), ('Dr. Sumit Gupta', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', 'DME55173185', '15.47'), ('Dr. Ashutosh Kumar', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', 'DME55173188', '15.47'), ('Shende Pranali kisandas', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', 'DME55172441', '15.47'), ('Vibha Tandon', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010013', '15.47'), ('HANISH KUMAR CHOWDA', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '04170140518', '15.47'), ('Reena Nayak', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', 'DME55172439', '15.47'), ('Dr. Veenapani Mire', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010079', '15.47'), ('Rajesh Kumar', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010065', '15.47'), ('Dushyant Chandra', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010031', '15.47'), ('Dr. Deepa Janghel', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010026', '15.47'), ('Dr. Awadh Sahu', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', 'DME55173201', '15.47'), ('DR RAKESH KUMAR AGRAWAL', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05170040053', '15.47'), ('GHANSHYAM SINGH JATRA', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05170011289', '15.47'), ('AVINASH MESHRAM', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '66170010023', '3.16'), ('RAVIKANT JATWAR', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '04170140099', '3.16'), ('Dr. Rakesh Kumar Verma', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '02530010055', '3.16'), ('Dr. Aditya Siodiya', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '09530010327', '3.16'), ('DR.ANMOL MADHUR MINZ', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '04170140656', '3.16'), ('Dr. Durga Shankar Patel', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '66170010344', '3.16'), ('Dr. Gopal Singh Kanwer', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '11170010478', '3.16')]

            processed_inc_names = process_scraped_data(incentive_received_data)
            print()
            print('printing processes incentive received data')
            # print(processed_inc_names)

            main_master_c_num_with_name_amt_cat_e_code.extend(processed_inc_names)
            # print(main_master_c_num_with_name_amt_cat_e_code) # ['CASE/PS6/HOSP22G146659/CB7008568', '2210', 'Ophthalmology', 'SICS with non-foldable IOL', '2023-10-07', 'Lal Khan', ('Dr. Gopal Singh Kanwer', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '11170010478', '3.16'), ('Dr. Durga Shankar Patel', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '66170010344', '3.16'), ('DR.ANMOL MADHUR MINZ', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '04170140656', '3.16'), ('Dr. Aditya Siodiya', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '09530010327', '3.16'), ('Dr. Rakesh Kumar Verma', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '02530010055', '3.16'), ('RAVIKANT JATWAR', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '04170140099', '3.16'), ('AVINASH MESHRAM', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल सलाहकार', '66170010023', '3.16'), ('GHANSHYAM SINGH JATRA', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05170011289', '15.47'), ('DR RAKESH KUMAR AGRAWAL', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05170040053', '15.47'), ('Dr. Awadh Sahu', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', 'DME55173201', '15.47'), ('Dr. Deepa Janghel', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010026', '15.47'), ('Dushyant Chandra', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010031', '15.47'), ('Rajesh Kumar', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010065', '15.47'), ('Dr. Veenapani Mire', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010079', '15.47'), ('Reena Nayak', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', 'DME55172439', '15.47'), ('HANISH KUMAR CHOWDA', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '04170140518', '15.47'), ('Vibha Tandon', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010013', '15.47'), ('Shende Pranali kisandas', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', 'DME55172441', '15.47'), ('Dr. Ashutosh Kumar', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', 'DME55173188', '15.47'), ('Dr. Sumit Gupta', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', 'DME55173185', '15.47'), ('Dr. manoj Kumar', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )', '05530010029', '15.47'), ('ACHCHHE KUMAR PATLEY', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '04170150173', '2.49'), ('Geeta patel', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', 'J55172863', '2.49'), ('Pratima Sahu', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', 'N5517593', '2.49'), ('Haricharan Jangde', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '05170010396', '2.49'), ('Shri Dildar Sahish', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '05170020054', '2.49'), ('Smt. Pinky Singh', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '06170100054', '2.49'), ('Smt. Reena Verma', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', 'AI55170024', '2.49'), ('Santosh Kumar Singh', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', 'AI55170030', '2.49'), ('Shri Sushil kumar miri', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '03170010366', '2.49'), ('Shri C.L. Dixena', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '05170020117', '2.49'), ('SHIVSHANKAR SINGH KANWAR', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '05170060099', '2.49'), ('SMT DURGESHWARI KARSH', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '06170050083', '2.49'), ('ARUN KUMAR KANWAR', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '07170021387', '2.49'), ('Smt.Bhagwati Koshle', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '09170010257', '2.49'), ('dinesh kumar patel', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '09530010377', '2.49'), ('MAHENDRA KUMAR', 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )', '05170011797', '2.49'), ('Dr.Sumit Gupta', 'सभी फिजिशियन / सर्जन', '05170020187', '198.9'), ('Dr. V.Agrawal', 'सभी फिजिशियन / सर्जन', '05170020043', '198.9'), ('DR ARUNIKA SISODIYA', 'सभी फिजिशियन / सर्जन', '05170020182', '198.9'), ('Dr Ankita Kapoor', 'सभी फिजिशियन / सर्जन', '05530010028', '198.9'), ('Dr. Priyanka Ekka', 'सभी फिजिशियन / सर्जन', '05530010030', '198.9'), ('Smt. Varnita Zilkar', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '15170200084', '2.95'), ('Amarjeet Kour', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '19170040056', '2.95'), ('Radhe Shyam Kashyap', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'AI55170022', '2.95'), ('Neelu Chaudhary', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517492', '2.95'), ('Sanjay Das Manikpuri', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517599', '2.95'), ('Rajni Kiran Kispotta', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '11170010433', '2.95'), ('Smt.Seema Rani Lajras', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020063', '2.95'), ('Victoria Gardia', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170010273', '2.95'), ('PRIYA VERMA', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020641', '2.95'), ('Smt. Sarika Tirpude Ramteke', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020665', '2.95'), ('SMT. PHULKUMARI TOPPO', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020668', '2.95'), ('Priti Masih Upma Kumar', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '15170200071', '2.95'), ('Deepa sahu', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020472', '2.95'), ('PUSHPA BAG', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020500', '2.95'), ('CHANDRAKANTA SHRIVASTAV', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020507', '2.95'), ('VANDANA SAMUEL', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '66170020614', '2.95'), ('PAWAN KUMAR PATEL', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517809', '2.95'), ('Sanjaya Kumar Tiwari', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517515', '2.95'), ('Smt.DIVYA ALKA TOPPO', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '04170060068', '2.95'), ('DIPTI LAKRA', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '04170140331', '2.95'), ('SUSHILATA RATHIYA', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '04170140436', '2.95'), ('MANJULATA KANWAR', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '04170150162', '2.95'), ('PREETI SONWANI', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170011771', '2.95'), ('Ku. Sandhya Nair', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020124', '2.95'), ('Smt Bharti Markam', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020142', '2.95'), ('Ku.Jyoti Gual', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020143', '2.95'), ('Ku.Marget Bishwash', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020153', '2.95'), ('ku Kiran Sahu', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020161', '2.95'), ('SMT NAMITA PATEL', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170020176', '2.95'), ('Smt.Nirmala Miri', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '07170250081', '2.95'), ('Neelam Kanwar', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '08170040064', '2.95'), ('SAROJ RATHOR', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '09170160077', '2.95'), ('KU. ANJANA KUJUR', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '11170260055', '2.95'), ('vinita tigga', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '12170050188', '2.95'), ('Ku. Har Bai Khunte', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '14170011702', '2.95'), ('Smt. Bhavana Bansiyar', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '15170200090', '2.95'), ('Anita Yadav', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '22170040038', '2.95'), ('ASHA KINDO', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '03170050126', '2.95'), ('NEELIMA NISHAD', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170050074', '2.95'), ('TULSI YADAV', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '0617009003', '2.95'), ('KIRAN CHANDRA', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517979', '2.95'), ('Bhanu Priya Chauhan', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517989', '2.95'), ('Jyoti Porte', 'नर्सिंग एवं पैरामेडिकल स्टाफ', 'N5517990', '2.95'), ('Manish Singh', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '05170011626', '2.95'), ('Narendra Kumar Kanwar', 'नर्सिंग एवं पैरामेडिकल स्टाफ', '04170140534', '2.95'), ('RAJESH', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517032', '1.54'), ('RAMANAND', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517042', '1.54'), ('KUMARI SHREMATI', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517056', '1.54'), ('Mr. MONESHWAR CHANDRA RATHIYA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517083', '1.54'), ('Mr .AVINASH KUMAR BANJARE', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517084', '1.54'), ('Mr. BALDEV SINGH', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517085', '1.54'), ('MAHENDRA KUMAR', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N55171003', '1.54'), ('KU. PRIYA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517136', '1.54'), ('Mrs. BASANTI RATHIYA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517028', '1.54'), ('Mrs. ANAMIKA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517055', '1.54'), ('AAKANKSHA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517610', '1.54'), ('SUNITA RATHORE', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517613', '1.54'), ('BAJANTI', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517614', '1.54'), ('PRATIBHA', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517615', '1.54'), ('Komal Dewangan', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517589', '1.54'), ('Smt. Sant Ram Kashyap', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020095', '1.54'), ('Anand Singh Rathiya', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', 'N5517857', '1.54'), ('Shri Maheshwar Prasad Tandon', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020131', '1.54'), ('Smt.Lata Chandra', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020137', '1.54'), ('PUSHPENDRA KUMAR', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020184', '1.54'), ('S SHANKAR RAO', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020189', '1.54'), ('Shri C.P. Chandra', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020097', '1.54'), ('Shri H.P.Tiwari', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020098', '1.54'), ('Shri Sunil Kumar Channe', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020099', '1.54'), ('Shri S.N.Shriwas', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020100', '1.54'), ('RAVINDRA KUMAR PANDEY', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '04170150035', '1.54'), ('mohendra kumar janardan', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '04170150084', '1.54'), ('Shri Krishna Kumar Tripathi', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020082', '1.54'), ('Shri Shiv Kumar Sarthi', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020084', '1.54'), ('Shri Amar Das', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020086', '1.54'), ('Shri Shyam Das Mahant', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020087', '1.54'), ('Panch Ram Nirmalkar', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020091', '1.54'), ('V. Kondiya', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020092', '1.54'), ('Mithlesh Kumar Markam', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '07170250399', '1.54'), ('reman singh kanwar', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '07170250453', '1.54'), ('Mongra Tandon', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '04170150044', '1.54'), ('Smt. Chandrika Bai', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020088', '1.54'), ('Smt. Achamma Bai', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020090', '1.54'), ('Ankaiya', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020093', '1.54'), ('Smt. Shushila Bai', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020103', '1.54'), ('Bal Chainya', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020105', '1.54'), ('L.Kondiya', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020107', '1.54'), ('K. Damodar', 'चतुर्थ वर्ग एवं सफाई कर्मचारी', '05170020110', '1.54'), ('Mr. Kiran Kumar Sahu', 'डाटा एंट्री ऑपरेटर', 'J55172798', '22.1'), ('SUMITRA KURREY', 'डाटा एंट्री ऑपरेटर', 'J55173309', '22.1'), ('KUMARI JYOTI LAHRE', 'डाटा एंट्री ऑपरेटर', 'DME55173036', '22.1'), ('Yamini Verma', 'डाटा एंट्री ऑपरेटर', 'DME55173200', '22.1'), ('SURINDAR LAL CHANDRA', 'डाटा एंट्री ऑपरेटर', 'DME55173655', '22.1')]
            'The above main_master_c_num_with_name_amt_cat_e_code will be sent for saving in excel and db after processing'
            'DISPLAY THE NAMES AND AMOUNT'
            indent_json_print(main_master_c_num_with_name_amt_cat_e_code)

            'Excel save'
            ExcelMethods().excel_save_new(final_lol=main_master_c_num_with_name_amt_cat_e_code)

            'adding to list for db'
            one_batch_collected_data_for_db.append(main_master_c_num_with_name_amt_cat_e_code)

        except Exception as e:
            ColourPrint.print_bg_red(f"[Batch {batch_id}] ERROR in case {case_number}: {e}")
            continue  # optional continue statement

    return one_batch_collected_data_for_db


async def safe_batch_wrapper(one_batch_list, page, batch_id, depart_choice, from_date, to_date):
    try:
        return await entry_proper_one_batch(
            incentive_cases_list_one_batch=one_batch_list,
            page=page,
            batch_id=batch_id,
            depart_choice=depart_choice,
            from_date=from_date,
            to_date=to_date
        )
    except Exception as e:
        ColourPrint.print_bg_red(f"FATAL ERROR in Batch {batch_id}: {e}")
        return []  # batch returns empty but does not stop program



async def entry_proper_multi_batch(all_batch_list, context, num_of_pages_to_create, depart_choice,from_date, to_date, set_timeout):
    pages_created = []
    for _ in range(num_of_pages_to_create):
        new_page = await context.new_page()
        new_page.on("dialog", handle_dialog)  # <-- must do this!
        new_page.set_default_timeout(set_timeout)
        new_page.set_default_navigation_timeout(set_timeout)
        pages_created.append(new_page)


    tasks = []
    # batch_id = 1
    for i, one_batch_list in enumerate(all_batch_list):
        page = pages_created[i % num_of_pages_to_create]
        task = asyncio.create_task(safe_batch_wrapper(one_batch_list=one_batch_list, page=page,
                                                          batch_id= i+1, depart_choice=depart_choice,
                                                          from_date=from_date, to_date=to_date))


        tasks.append(task)

    all_batch_data = await asyncio.gather(*tasks, return_exceptions=True)

    [await page.close() for page in pages_created]

    # ColourPrint.print_blue(all_batch_list)
    return all_batch_data

async def approver_raise_query_multi(case_number, set_timeout_is=120_000, port =9223):
    ColourPrint.print_green("Inside Async")
    approver_page_indexes = await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='Shaheed Veer Narayan Singh Ayushman Swasthya Yojna', cdp_port=port)
    async with async_playwright() as p:
        cdp_for_main = port
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{cdp_for_main}")
        context = browser.contexts[0]
        all_pages = context.pages

        page_index = approver_page_indexes[0]  # selecting the first index of matching page
        # page = all_pages[page_index]  # selecting the first PAGE of matching page

        page = await context.new_page()

        page.set_default_timeout(set_timeout_is)
        page.set_default_navigation_timeout(set_timeout_is)

        url = f"https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApViewDME.aspx?ci={case_number}"
        await page.goto(url)

        Status().set_status(case_number=case_number, status_text=StatusText.INITIATE_BUT_QUERY_PAGE_NOT_LOADED)

        await page.select_option('#ctl00_ContentPlaceHolder1_StatusTxt', '3')
        await page.locator('#ctl00_ContentPlaceHolder1_queryText').fill('REINITIATE')
        # time.sleep(5)
        await page.locator("//input[@id='ctl00_ContentPlaceHolder1_statusSubmit']").click()
        # time.sleep(5)
        Status().set_status(case_number=case_number, status_text=StatusText.QUERY_CLEAR_CLICKED_BUT_TIMEOUT)
        # await page.locator("//button[normalize-space()='OK']").is_visible()
        await page.locator("//button[normalize-space()='OK']").click()
        ColourPrint.print_green('Async done')

        Status().set_status(case_number=case_number, status_text=StatusText.QUERIED_CLEAR_COMPLETED)

        await page.close()


def main(all_incentive_multiline, set_timeout_is=120000):
    t1 =time.perf_counter()
    asyncio.run(_main(all_incentive_multiline, set_timeout_is, num_of_pages_to_create=3))
    t2 = time.perf_counter()
    print(t2-t1)