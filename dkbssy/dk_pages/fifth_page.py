import asyncio

from bs4 import BeautifulSoup

from dkbssy.dk_pages.dk_login_page import Page
from playwright.async_api import async_playwright, Page as PagePlay


class FifthPage(Page):
    case_number_xpath = '//*[@id="ctl00_ContentPlaceHolder1_caseNoReqText"]'
    status_xpath = '//*[@id="ctl00_ContentPlaceHolder1_caseStatusText"]'
    procedure_xpath = '//*[@id="ctl00_ContentPlaceHolder1_procName"]'
    last_updated_xpath = '//*[@id="ctl00_ContentPlaceHolder1_caseLastUpdateDate"]'

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def modified_url(self, case_number):
        return f'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleViewDME.aspx?ci={case_number}'

    def get_data(self, case_number):
        # print(self.modified_url(case_number))
        self.driver.get(self.modified_url(case_number))
        # wait for table loading
        self.find_wait_by('//*[@id="incentiveTableData"]/tr[1]/td[1]')
        case_number_text = self.find_wait_by(self.case_number_xpath).text
        status_text = self.find_wait_by(self.status_xpath).text
        last_updated_text = self.find_wait_by(self.last_updated_xpath).text
        procedure_text = self.find_wait_by(self.procedure_xpath).text
        # wait for table loading
        self.find_wait_by('//*[@id="incentiveTableData"]/tr[1]/td[1]')
        # get table data
        table_data_tbody = self.find_wait_by('//*[@id="incentiveTableData"]').text
        rows = table_data_tbody.split('\n')
        # print('-----tbody-------')
        # print(repr(table_data_tbody))
        print(table_data_tbody)
        print('========')
        return case_number_text, status_text, last_updated_text, procedure_text, table_data_tbody

    def bs4_parser(self, html_string):
        # html_string = '''<tr><td>1</td><td>अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल  सलाहकार  </td><td>Professor(DME)</td>...<td></td></tr>'''  # your full inner_html here

        soup = BeautifulSoup(html_string, "html.parser")

        table_data = []

        for row in soup.find_all("tr"):
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            table_data.append(cells)

        # Example output
        # for row in table_data:
        #     print('bs4-->>', row) # or print(row) as list
        return table_data


    def amount_id_extract(self, case_number):
        """selenium approach"""
        # case_number_text, status_text, last_updated_text, procedure_text, table_data_tbody = self.get_data(case_number)  # selenium approach
        # print(table_data_tbody)

        "playwright approach"
        case_number_text, status_text, last_updated_text, procedure_text, table_data_tbody = self.get_data_async_main(case_number)
        # print('by playwright')

        data_of_line = []
        table_by_lines = self.bs4_parser(html_string=table_data_tbody)
        # print('table by line', table_by_lines)

        category = None

        for i in table_by_lines:
            # print(i) # ['1', 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल  सलाहकार', 'Professor(DME)', 'Dr. Gopal Singh Kanwer', '0058020401008356', 'PUNB0617300', '11170010478', '3.16', '', '', '', '']
            name_amount_list = i[1].split()
            # print('----', name_amount_list)
            if name_amount_list[0] == 'अधिष्ठाता':
                category = 1
            elif name_amount_list[0] == 'पैथोलॉजी' and name_amount_list[8] == 'फैकल्टी':
                # print('path f')
                category = 2
            elif name_amount_list[0] == 'पैथोलॉजी' and name_amount_list[8] == '(टेक्निशियन':
                category = 3
                # print('path t')
            elif name_amount_list[0] == 'सभी' and name_amount_list[1] == 'फिजिशियन':
                category = 4
                # print('phys')
            elif name_amount_list[0] == 'सभी' and name_amount_list[1] == 'सीनियर':
                category = 5
                # print('seni')
            elif name_amount_list[0] == 'एनेस्थीसिया':
                category = 6
            elif name_amount_list[0] == 'नर्सिंग':
                category = 7
            elif name_amount_list[0] == 'चतुर्थ':
                category = 8
            elif name_amount_list[0] == 'डाटा':
                category = 9
            amount = i[7]
            emp_id = i[6]
            data_of_line.append([category, emp_id, amount])
            # print('::::', data_of_line)
            # print(case_number_text, status_text, last_updated_text, procedure_text, data_of_line)
        return case_number_text, status_text, last_updated_text, procedure_text, data_of_line

    def get_data_async_main(self, case_number):
        return asyncio.run(self._get_data_async(case_number))

    async def _get_data_async(self, case_number):
        new_url = self.modified_url(case_number)
        play = await async_playwright().start()
        browser = await play.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0]
        page.set_default_timeout(300000)
        # print('playerithjjjjj')
        await page.goto(new_url)
        # Wait for any redirection and DOM loading
        await page.wait_for_load_state("networkidle")

        await page.wait_for_selector('//*[@id="incentiveTableData"]/tr[1]/td[1]')

        case_number_text = await page.locator(self.case_number_xpath).text_content()
        status_text = await page.locator(self.status_xpath).text_content()
        last_updated_text = await page.locator(self.last_updated_xpath).text_content()
        procedure_text = await page.locator(self.procedure_xpath).text_content()

        # wait for table loading
        await page.wait_for_selector('//*[@id="incentiveTableData"]/tr[1]/td[1]')

        # get table data
        # table_data_tbody = await page.locator('//*[@id="incentiveTableData"]').text_content()
        table_data_tbody = await page.locator('//*[@id="incentiveTableData"]').inner_html()
        rows = table_data_tbody.split('\n')

        # print('tsblr', table_data_tbody)
        # print(type(table_data_tbody))

        await play.stop()
        return case_number_text, status_text, last_updated_text, procedure_text, table_data_tbody
#
# async def get_multiple_async(number_of_page, case_number_list):
#     play = await async_playwright().start()
#     browser = await play.chromium.connect_over_cdp('http://localhost:9222')
#     context = browser.contexts[0]
#     pages = [context.new_page() for i in number_of_page]



    # await play.stop()

if __name__ == '__main__':
    # FifthPage(None, None).get_data_async_main('CASE/PS6/HOSP22G146659/CK7323887')
    FifthPage(None, None).amount_id_extract('CASE/PS6/HOSP22G146659/CK7323887')