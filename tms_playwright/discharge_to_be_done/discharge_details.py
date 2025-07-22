import datetime
import openpyxl
from playwright.sync_api import sync_playwright, TimeoutError, Page, expect
import time
from dis_tms.utils import utilities
from dkbssy.utils.colour_prints import ColourPrint
from tms_playwright.page_objs_tms import tms_xpaths


class DischargeGetParameters:
    def modal_ok_box(self,
                     page,
                     partial_body_text,
                     modal_body_xpath=tms_xpaths.modal_body_xpath,
                     modal_ok_xpath=tms_xpaths.modal_ok_xpath):
        modal_body_web = page.wait_for_selector(modal_body_xpath)
        web_modal_body_text = modal_body_web.inner_text()
        if partial_body_text in web_modal_body_text:
            modal_ok_button = page.wait_for_selector(modal_ok_xpath)
            modal_ok_button.click()
            ColourPrint.print_green(web_modal_body_text, "-> Done Till Here")
        else:
            ColourPrint.print_bg_red(f'No button containing "{partial_body_text}"')
            return

    def login(self, user_id, page):
        page.goto(tms_xpaths.first_page_url_xpath)
        username = page.wait_for_selector(tms_xpaths.username_xpath)
        username.fill(user_id)
        proceed_button = page.wait_for_selector(tms_xpaths.proceed_button_xpath)
        proceed_button.click()
        self.modal_ok_box(page, tms_xpaths.AFTER_PROCEED_MODAL_BODY_TEXT)
        password = page.wait_for_selector(tms_xpaths.password_xp)
        password.type(tms_xpaths.password_value)
        captcha = page.wait_for_selector(tms_xpaths.captcha_xp)
        captcha.click()
        time.sleep(10)
        login_checkbox_button = page.wait_for_selector(tms_xpaths.login_checkbox)
        login_checkbox_button.click()
        login_button = page.wait_for_selector(tms_xpaths.login_button_xp)
        login_button.click()
        page.wait_for_load_state()

    def detail_entry_page(self, page: Page, case_number):
        middle_frame_element = page.wait_for_selector(tms_xpaths.middle_frame_xp)
        middle_frame_content = middle_frame_element.content_frame()
        case_number_input = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_case_number_field_xp)
        case_number_input.fill(case_number)
        down_arrow = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_type_down_arrow_xp)
        down_arrow.click()
        input_box = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_input_box)
        input_box.fill('All')
        page.keyboard.press("Enter")
        search_button = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_search_button_xp)
        search_button.click()

    def retrieve_data(self, page: Page, case_number):
        middle_frame_element = page.wait_for_selector(tms_xpaths.middle_frame_xp)
        middle_frame_content = middle_frame_element.content_frame()
        try:
            middle_frame_content.wait_for_selector(tms_xpaths.dis_details_wait_for_table_xp)
            card = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_card_xp).text_content()
            status = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_status_xp).text_content()
            name = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_name_xp).text_content()
            depart = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_depart_xp).text_content()
            procedure = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_procedure_xp).text_content()
            # date = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_date_xp).text_content().split("/")
            # date = datetime.date(year=int(date[2]), month=int(date[1]), day=int(date[0]))
            # print("Date Is", date)

            date = middle_frame_content.wait_for_selector(tms_xpaths.dis_details_date_xp).text_content()
            # print("Date Is", date)
            return card, name, case_number, date, depart, procedure, status

        except TimeoutError:
            no_record = middle_frame_content.wait_for_selector(tms_xpaths.dis_detail_not_found).text_content()
            if no_record == "No Records Found":
                print("NO RECORD", case_number)

    def query_question_data(self, page: Page) -> str:
        middle_frame_element = page.wait_for_selector(tms_xpaths.middle_frame_xp)
        middle_frame_content = middle_frame_element.content_frame()
        searched_case_number = middle_frame_content.wait_for_selector(tms_xpaths.claim_query_searched_case_number_xp)
        searched_case_number.click()

        bottom_frame_element = middle_frame_content.wait_for_selector(tms_xpaths.bottom_frame_xp)
        bottom_frame_content = bottom_frame_element.content_frame()
        query_question = bottom_frame_content.wait_for_selector(tms_xpaths.claim_query_table_query_question_xp)
        query_required = query_question.inner_text()
        return query_required

    def split_case_numbers(self, case_numbers: str) -> list:
        case_numbers = case_numbers.split('\n')
        filtered_case_numbers = []
        for c in case_numbers:
            if c == "":
                pass
            else:
                filtered_case_numbers.append(c)
        return filtered_case_numbers

    def excel_save(self, list_to_save, raw_file_path):  # r'H:\My Drive\GdrivePC\Hospital\RSBY\New\discharge1.xlsx'
        wb = openpyxl.load_workbook(raw_file_path)
        ws = wb['Sheet1']
        ws.append(list_to_save)
        wb.save(raw_file_path)
        wb.close()

    def main_discharge_detail_tms(self, user_id, case_numbers, raw_excel_file_path, is_query_question_required=False):
        """is_query_question_required: will go next page to retrieve the query /objections raised"""
        case_numbers = self.split_case_numbers(case_numbers)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, args=['--start-maximized'])
            page = browser.new_page(no_viewport=True)
            page.set_default_timeout(20000)
            self.login(user_id, page)

            for case_number in case_numbers:
                if not is_query_question_required:
                    print(case_numbers.index(case_number), case_number)
                    # detail page
                    self.detail_entry_page(page, case_number)
                    data = self.retrieve_data(page, case_number)
                    print(data)
                    self.excel_save(data, raw_excel_file_path)
                else:
                    print(case_numbers.index(case_number), case_number)
                    # detail page
                    self.detail_entry_page(page, case_number)
                    data = self.retrieve_data(page, case_number)  # returns tuple
                    # print(data)
                    question = self.query_question_data(page)
                    data = list(data)
                    data.append(question)
                    print(data)
                    self.excel_save(data, raw_excel_file_path)
                    case_search_left_panel = page.wait_for_selector(tms_xpaths.claim_query_cases_search_tab_xp)
                    case_search_left_panel.click()

            down_logout_arrow = page.wait_for_selector(tms_xpaths.down_arrow_xp)
            down_logout_arrow.click()
            logout_button = page.wait_for_selector(tms_xpaths.logout_button_xp)
            logout_button.click()

# if __name__ == "main":
#     DischargeGetParameters().main_discharge_detail_tms(case_numbers, list_to_save, raw_excel_file_path)
