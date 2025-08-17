import asyncio
import json

import gspread
from playwright.async_api import async_playwright
from TMS_Process.process.claim_clearer import is_home_page, select_ALL_and_search
from TMS_Process.process.tks import initial_setup
from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
from playwright.async_api import async_playwright, Page, TimeoutError, expect
from TMS_Process.process.enhance_2 import headers_for_tms, validate_registration_no
from TMS_new.play_request.req_2 import AsyncTms
from dkbssy.utils.colour_prints import ColourPrint


def col_letter_to_index(letter):
    """Convert column letter(s) like 'A', 'B', 'AA' to number."""
    letter = letter.upper()
    result = 0
    for char in letter:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result

class GSheetHandle:
    def __init__(self, g_workbook_id, auth_file_path):
        self.g_workbook_id = g_workbook_id
        self.auth_file_path = auth_file_path

        # Authenticate using service account file
        gc = gspread.service_account(self.auth_file_path)
        # Open the gsheet
        self.workbook = gc.open_by_key(self.g_workbook_id)


    def g_single_col_data(self, worksheet_name, col_index_start_at_1)->list:
        """
        Used for getting the single column data
        :param worksheet_name: worksheet name of workbook initialised at start
        :param col_index_start_at_1: Index - NON-ZERO
        :return: list of column data
        """
        worksheet = self.workbook.worksheet(worksheet_name)
        col_data = worksheet.col_values(col_index_start_at_1)
        return col_data


    def get_enhance_req_or_not(self, column_alpha):
        column_index_int = col_letter_to_index(column_alpha)
        req_or_not_col_data = self.g_single_col_data(worksheet_name='ENSAN',col_index_start_at_1=column_index_int)
        print(req_or_not_col_data)  # ['REMARK', 'NOT REQUIRED', 'NOT REQUIRED', 'YES', 'NOT REQUIRED', 'COMPLETED']
        # for i, j in enumerate(req_or_not_col_data):
        #     filter_yes_indexes = [req_or_not_col_data.index()]
        d = [i for i, j in enumerate(req_or_not_col_data) if j=='YES']
        print(d)
        return d

    def get_all_sheet_data(self, sheet_name)-> list[dict[str, int | float | str]]:
        sheet = self.workbook.worksheet(sheet_name)
        sh_data=sheet.get_all_records()
        # print(sh_data)
        return  sh_data

    def enhance_required(self,sheet_name):
        """
        Include the "Remark"="YES" data and blank remark with registration number must be present. Ignores non "YES".
        :param sheet_name: Enhancement sheet
        :return: list of YES and BLANK REMARK
        """
        full_data = self.get_all_sheet_data(sheet_name=sheet_name)
        filtered_yes_blank = [x for x in full_data if ((x.get('REMARK') =="YES" or x.get('REMARK')=="") and str(x.get('REGISTRATION NO')).strip() != "")]
        print(json.dumps(filtered_yes_blank,indent=2))
        validate_registration_no(filtered_yes_blank)


        return filtered_yes_blank


    async def _start_tms(self, filtered_yes_list, set_timeout=10000, cdp_port=9222):
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(f"http://localhost:{cdp_port}")
            context = browser.contexts[0]
            all_pages = context.pages
            pages_indexes = await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='PMJAY - Provider', cdp_port=cdp_port)
            page_index = pages_indexes[0]  # selecting the first index of matching page
            page = all_pages[page_index]  # selecting the first PAGE of matching page
            page.set_default_timeout(set_timeout)

            "REQUEST INTERACTION"
            regis_no_list_of_yes_blank = self.regis_no_of_filtered_yes_blank_enhance(filtered_yes_list=filtered_yes_list)
            # print(regis_no_only_list_of_yes)

            "preparing headers"
            # get session storage
            session_storage = await AsyncTms().get_session_storage(page)
            print('Session Storage: ', json.dumps(session_storage, indent=2))
            headers = headers_for_tms(session_storage=session_storage)
            print('headers', headers)

            "retrieving the datas from TMS the other fields of spreadsheet enhancement"
            datas_are_list = await AsyncTms().process_all(both_query_list=regis_no_list_of_yes_blank, context=context, headers=headers)
            ColourPrint.print_yellow(datas_are_list)

            "UI INTERACTIONS"
            # checking is home page
            for dic_data in filtered_yes_list:  #[{'REGISTRATION NO': 1012089745, 'CARD': '', 'NAME': '', 'ADMISSION DATE': '', 'Total Blocking days': '', 'ENHANCE STATUS': '', 'LAST ENHAN TAKEN DATE': '', 'REMARK': 'YES', 'LOCATION': ''},
                # {'REGISTRATION NO': 1012089747, 'CARD': '', 'NAME': '', 'ADMISSION DATE': '', 'Total Blocking days': '', 'ENHANCE STATUS': '', 'LAST ENHAN TAKEN DATE': '', 'REMARK': 'YES', 'LOCATION': ''}]

                await is_home_page(page=page)
                await select_ALL_and_search(page=page, registration_no=str(dic_data['REGISTRATION NO']))
                await self.initiate_enhance(page=page)

    def regis_no_of_filtered_yes_blank_enhance(self, filtered_yes_list):
        reg_no_list = [x['REGISTRATION NO'] for x in filtered_yes_list]
        return reg_no_list

    async def initiate_enhance(self, page:Page):
        await page.locator("//button[text()='Initiate Enhancement']").click()
        await page.locator("//button[text()='YES']").click()


    def async_run_by_sync(self, filtered_yes_list):
        return asyncio.run(self._start_tms(filtered_yes_list))

def main():
    """Checking the base folder of OPD IPD"""
    # initial_setup()

    wb_id ='1vhjV0rcODJ4lGYJBHENMnHFvqHgK25dQRt9SVpr_9N4'

    "update manually in pc"
    auth_file_name = r"./downloads/sodium-cat-452017-h0-9d08be057d0e.json"
    sheet_name = 'ENSAN'
    "update manually in pc above"

    wb = GSheetHandle(g_workbook_id=wb_id, auth_file_path=auth_file_name)
    wb.get_all_sheet_data(sheet_name=sheet_name)

    enhance_required_list = wb.enhance_required(sheet_name=sheet_name)

    # updating workbook




    wb.async_run_by_sync(enhance_required_list)



if __name__ == '__main__':
    main()