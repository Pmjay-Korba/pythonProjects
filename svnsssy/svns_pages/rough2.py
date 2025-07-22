import openpyxl
from playwright.sync_api import sync_playwright, Page, TimeoutError

from ehospital_proper.colour_print_ehosp import ColourPrint
from svnsssy.svns_pages import xpaths_svsn as xpaths


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
    employees_data_dict = {k:v for k,v in employees_data_dict.items() if k is not None}

    print(employees_data_dict)
    return employees_data_dict

def retrieve_incentive_data_from_dk(page:Page, employees_data_emp_ip:str)->list[str]:
    """
    retrieve the all data of employee detail
    :param employees_data_emp_ip: dict of emp name and id
    :return: all data from dk site
    """
    if page.url != xpaths.incentive_detail_website_url:
        page.goto(xpaths.incentive_detail_website_url)
    page.wait_for_selector(xpaths.emp_code_entry_field).fill(employees_data_emp_ip)
    page.on('response', lambda response: wait_for_ajax(response,xpaths.check_url))
    page.locator(xpaths.search_button).click()

    total_amount_pending = page.locator('//*[@id="ctl00_ContentPlaceHolder1_Label4"]').text_content()
    total_paid_cases = page.locator('//*[@id="ctl00_ContentPlaceHolder1_Label14"]').text_content()
    total_paid_amount = page.locator('//*[@id="ctl00_ContentPlaceHolder1_Label5"]').text_content()
    # try:
    number_of_cases_pending = page.locator('//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[2]/td[3]').text_content()
    # except NoSuchElementException:
    #     number_of_cases_pending = 0
    print(employees_data_emp_ip, number_of_cases_pending, '\t', total_amount_pending, '\t', total_paid_cases, '\t', total_paid_amount)

    # return code, number_of_cases_pending, total_amount_pending.text, total_paid_cases.text, total_paid_amount.text

# except TimeoutException:
# print(f"\033[93mTime Out\033[0m")
# raise TimeoutException


def wait_for_ajax(response, check_url):
    if check_url not in response.url:
        res = response.status
        # data = response.text()
        # print(f'response-{res}, data-{data}')
        # print(f'response code - {res}')

    # print(response)
    # try:
    #     if check_url in response.url
    # except Exception as e:
    #     ColourPrint.print_bg_red("Exception")
    #     print(e)
    #     ColourPrint.print_bg_red("Exception")

def ayushman_app(desired_title_of_page):

    with sync_playwright() as p:
        # Connect to the running Chrome instance on the debugging port
        browser = p.chromium.connect_over_cdp('http://localhost:9222')

        # Get the active browser context and page (tab)
        context = browser.contexts[0]  # Assuming you want the first context


        for page in context.pages:
            try:
                page_title = page.title()
                print(f"Checking page title: {page_title}")
                print("Current URL: ", page.url)

                if page_title.strip() == desired_title_of_page:
                    # if page_title.strip().lower() == target_title.strip().lower():
                    ColourPrint.print_yellow(f"Found matching page: {page_title}")
                    page.set_default_timeout(20000)
                    # retrieve_incentive_data_from_dk(page,'N55171003')

                    # getting all names and ids
                    all_name_and_id_dict = get_emp_data_from_excel(
                        r"G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto_ver_3.xlsx",
                        'Sheet3')
                    for each_name, each_id in all_name_and_id_dict.items():  # retrieve_incentive_data_from_dk(page,'N55171003')
                        retrieve_incentive_data_from_dk(page, employees_data_emp_ip=each_id)
                        print()

            except Exception as e:
                ColourPrint.print_bg_red('Error Start Below')
                print(f"Error accessing a page: {e}")
                ColourPrint.print_bg_red('Error End Above')



