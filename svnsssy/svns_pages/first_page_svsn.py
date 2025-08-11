import datetime
import sqlite3
import openpyxl
from playwright.sync_api import sync_playwright, Page, TimeoutError

from dkbssy.utils.colour_prints import ColourPrint
from svnsssy.svns_pages import xpaths_svsn as xpaths


class AyushmanApp:
    # def __init__(self):
    # self.playwright = sync_playwright().start()
    # self.browser = self.playwright.chromium.connect_over_cdp('http://localhost:9222')
    # self.context = self.browser.contexts[0]
    # self.page = self.context.new_page()
    # self.url = url
    # self.page_title = page_title

    def get_desired_page(self, target_title):
        playwright = sync_playwright().start()
        browser = playwright.chromium.connect_over_cdp('http://localhost:9222')
        # context = browser.contexts
        # print('Context length', len(context))
        # print(context)
        if not browser.contexts:
            print("No active contexts found.")
            playwright.stop()
            return

        context = browser.contexts[0]

        # Ensure there's at least one active page
        if context.pages:
            pages = context.pages
        else:
            print("No existing pages detected. Creating a new tab...")
            page = context.new_page()
            pages = [page]

        # Search for the page by title
        matched_page = None
        for page in pages:
            title = page.title()
            print(f"Checking Page: {title} | URL: {page.url}")

            if target_title.lower() in title.lower():  # Case-insensitive search
                matched_page = page
                break

        if matched_page:
            page = matched_page
            ColourPrint.print_yellow(f"Matched Page Found: {page.title()} ({page.url})")
            print("Now working with this page...")
            page.set_default_timeout(30000)
            # page.goto()
            return page

    @staticmethod
    def get_emp_data_from_excel(main_excel_path: str, sheet_name) -> dict:
        """ main_excel_path = incentive_auto_version_3 path.xlsx
        return {employee name(s): employee id(s)} dict()
        """
        # print(0000000,main_excel_path)
        if not main_excel_path.endswith('.xlsx'):
            main_excel_path += '.xlsx'
            print(main_excel_path)
        # print(11111111, main_excel_path)
        workbook = openpyxl.load_workbook(main_excel_path)
        worksheet = workbook[sheet_name]

        employees_data = worksheet.iter_rows(min_row=2, values_only=True)
        employees_data_dict = dict()
        # print(list(employees_data)[0])
        for each_emp_data in employees_data:
            emp_name = each_emp_data[1]
            emp_emp_id = each_emp_data[2]
            employees_data_dict[emp_name] = emp_emp_id
        workbook.close()
        employees_data_dict = {k: v for k, v in employees_data_dict.items() if k is not None}
        print(employees_data_dict)
        return employees_data_dict

    def wait_for_ajax(self, response, check_url):
        if check_url not in response.url:
            res = response.status

    def retrieve_incentive_data_from_dk(self, page: Page, employees_data_emp_ip: str) -> dict:
        """
        retrieve the all data of employee detail
        :param employees_data_emp_ip: dict of emp name and id
        :return: all data from dk site
        """
        if page.url != xpaths.incentive_detail_website_url:
            page.goto(xpaths.incentive_detail_website_url)
        try:
            current_date_time = datetime.datetime.now()
            current_date_time = current_date_time.strftime('%Y-%m-%d %H:%M:%S')
            page.wait_for_selector(xpaths.emp_code_entry_field).fill(employees_data_emp_ip)
            page.on('response', lambda response: self.wait_for_ajax(response, xpaths.check_url))
            page.locator(xpaths.search_button).click()

            total_amount_pending = page.locator('//*[@id="ctl00_ContentPlaceHolder1_Label4"]').text_content()
            total_paid_cases = page.locator('//*[@id="ctl00_ContentPlaceHolder1_Label14"]').text_content()
            total_paid_amount = page.locator('//*[@id="ctl00_ContentPlaceHolder1_Label5"]').text_content()
            # try:
            number_of_cases_pending = page.locator(
                '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[2]/td[3]').text_content()
        except TimeoutError:
            number_of_cases_pending = 0
        print(employees_data_emp_ip, number_of_cases_pending, '\t', total_amount_pending, '\t', total_paid_cases, '\t',
              total_paid_amount)
        keys_d = ['id_emp', 'unpaid_cases', 'unpaid_amount', 'paid_cases', 'paid_amount', "date_time_updated"]
        values_d = [employees_data_emp_ip, number_of_cases_pending, total_amount_pending, total_paid_cases, total_paid_amount, current_date_time]

        d = {}
        for keys, values in zip(keys_d, values_d):
            d[keys]=values
        return d

    @staticmethod
    def temp_inc_data_sql(data_list_of_all:list[dict]):
        # [{'id_emp': 'J55172798', 'unpaid_cases': '9142', 'unpaid_amount': '483044', 'paid_cases': '469', 'paid_amount': '11779', 'date_time_updated': datetime.datetime(2025, 2, 16, 14, 49, 20, 920975), 'name_emp': 'Mr. Kiran Kumar Sahu'},
        # {'id_emp': 'J55173309', 'unpaid_cases': '9139', 'unpaid_amount': '482117', 'paid_cases': '470', 'paid_amount': '11915', 'date_time_updated': datetime.datetime(2025, 2, 16, 14, 49, 26, 286095), 'name_emp': 'SUMITRA KURREY'}]



        conn = sqlite3.connect('temp_updated_db.db')
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temp_emp_data (
                table_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_emp TEXT,
                id_emp TEXT UNIQUE, 
                unpaid_cases TEXT,
                unpaid_amount TEXT,
                paid_cases TEXT,
                paid_amount TEXT,
                date_time_updated TEXT
            )
        ''')
        # retrieving the saved data to check the time updated
        cursor.execute('''
            SELECT * FROM temp_emp_data         
        ''')



        # Inserting the data
        cursor.executemany('''
            INSERT INTO temp_emp_data(
                name_emp,
                id_emp, 
                unpaid_cases,
                unpaid_amount,
                paid_cases,
                paid_amount,
                date_time_updated
                )
                
                VALUES (
                :name_emp,
                :id_emp, 
                :unpaid_cases,
                :unpaid_amount,
                :paid_cases,
                :paid_amount,
                :date_time_updated
                )
                
            ''', data_list_of_all)



        conn.commit()
        conn.close()


