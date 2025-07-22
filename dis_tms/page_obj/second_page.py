import random

from dis_tms.page_obj.first_page import Page
from selenium.common.exceptions import TimeoutException

from dis_tms.utils import utilities
from dkbssy.utils.colour_prints import ColourPrint


class SecondPage(Page):
    _down_arrow_xp = '//span[contains(@style,"display:inline")]'
    _logout_button_xp = '//a[normalize-space()="Log Out" and not(contains(@style, "color"))]'
    _pre_authorisation = '//span[normalize-space()="Preauthorization"]'
    _discharge_xp = '//span[normalize-space()="Cases for Surgery/Discharge"]'
    _search_box_xp = '//input[@name="caseNo"]'
    _search_button_xp = '//button[normalize-space()="Search"]'
    _search_case_num_xp = '//*[@id="no-more-tables"]/table/tbody/tr/td[2]/b/u/a'
    _doctor_type_xp = '//select[@id="surDocType"]'
    _ip_date_xp = '//b[text()="IP Registered Date: "]/parent::label/parent::div'

    _doctor_type_dd_xp, _doctor_type_wait_xp, _doctor_type_value = ('//*[@id="surDocType"]',
                                                                    '//*[@id="surDocType"]/option', "O")
    _doctor_name_dd_xp, _doctor_name_wait_xp, _doctor_name_value = ('//*[@id="surgeonName"]',
                                                                    '//select[@id="surgeonName"]/option[3]',
                                                                    utilities.doctor_name())
    _treatment_date_xp = '//input[@id="surgstartdt"]'
    _save_treatment_date_xp = '//button[@id="dateUpdate"]'
    AFTER_TREATMENT_SAVE_MODAL_BODY_TEXT = 'Do you want to save Treatment start/ Surgery dates?'
    # _modal_body_text_xpath = ('//button[text()="OK"]/ancestor::div[@class="modal-content"]/descendant::div['
    #                           '@class="bootbox-body"]')
    _SAVE_SUCCESSFULLY_TEXT = 'Saved Successfully'
    _radio_discharge_xp = '//*[@id="discharge"]'
    _discharge_date_xp = '//input[@id="disDate"]'
    _follow_up_xp = '//input[@id="nxtFollUpDt"]'
    _special_xp, _special_wait_xp, _special_value = '//*[@id="specCase"]', '//*[@id="specCase"]/option[3]', 'NO'
    _procedure_consent_xp = '//*[@id="procedureConsentYes"]'
    _disclaimer_xp = '//*[@id="disDisClaimer"]'
    _attachment_button_xp = '//*[@id="btnattach"]'

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def logout(self):
        self.find_wait_by_clickable(self._down_arrow_xp).click()
        self.find_wait_by_clickable(self._logout_button_xp).click()

    def pre_auth(self, case_number):
        self.find_wait_by_clickable(self._pre_authorisation).click()
        self.find_wait_by_clickable(self._discharge_xp).click()
        self.switch_frames("middleFrame")
        self.find_wait_by_presence(self._search_box_xp).send_keys(case_number)
        self.find_wait_by_clickable(self._search_button_xp).click()
        try:
            self.find_wait_by_visible(self._search_case_num_xp).click()
        except TimeoutException:
            print()
            ColourPrint.print_pink("ALREADY DONE")
            print()

    def get_ip_date(self):
        ip_date = self.find_wait_by_presence(self._ip_date_xp).text
        # print(repr(ip_date))  # = 'IP Registered Date:\n10/06/2024'
        ColourPrint.print_yellow(ip_date)
        return ip_date.split("\n")[1]

    def date_entry(self, xpath, date_value):
        # self.find_wait_by_clickable(xpath=xpath).send_keys(date_value)
        element = self.find_wait_by_presence(xpath=xpath)
        script = f"arguments[0].value = '{date_value}'; arguments[0].dispatchEvent(new Event('change'));"
        self.driver.execute_script(script, element)

    def second_page_main(self, case_number, _discharge_date):
        self.pre_auth(case_number)

        # getting ip date
        ip_date = self.get_ip_date()
        # converting to datetime
        ip_date_str_datetime = utilities.date_insert(ip_date)

        # second_page_obj.logout()
        self.switch_frames('bottomFrame')
        self.drop_down_load_and_select(self._doctor_type_dd_xp, self._doctor_type_wait_xp, self._doctor_type_value)
        self.drop_down_load_and_select(self._doctor_name_dd_xp, self._doctor_name_wait_xp, self._doctor_name_value)
        # enter treatment/surgery date
        self.date_entry(self._treatment_date_xp, ip_date_str_datetime)
        # save button click
        self.button_click(self._save_treatment_date_xp)
        save_treatment_modal_clicking = self.modal_box(self.AFTER_TREATMENT_SAVE_MODAL_BODY_TEXT,
                                                       self._modal_body_text_xpath)
        xx = self.find_wait_by_visible('//div[contains(@class,"bootbox") and contains(@class,"show")]/descendant::div[@class="bootbox-body"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", xx)
        save_treatment_modal_clicking.click()
        try:
            save_success_modal_clicking = self.modal_box(self._SAVE_SUCCESSFULLY_TEXT)
            save_success_modal_clicking.click()
        except TimeoutException:
            ColourPrint.print_yellow('Timeout - No Saved Pop-up')
            pass
        self.radio_click(self._radio_discharge_xp)

        # discharge date # converting to datetime
        discharge_date_str_datetime = utilities.date_insert(_discharge_date)
        # adding discharge time
        dis_hour = random.choice(['13', '14', '15', '16', '17', '18', '19', '20'])
        dis_minute = random.choice(['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'])
        discharge_date_and_time = discharge_date_str_datetime + " " + dis_hour + ":" + dis_minute

        # enter discharge date
        self.date_entry(self._discharge_date_xp, discharge_date_and_time)
        # enter follow-up date
        follow_up_str_datetime = utilities.date_insert(_discharge_date, follow_up_days=5)
        self.date_entry(self._follow_up_xp, follow_up_str_datetime)
        self.drop_down_load_and_select(self._special_xp, self._special_wait_xp, self._special_value)
        self.radio_click(self._procedure_consent_xp)
        self.button_click(self._disclaimer_xp)
        self.button_click(self._attachment_button_xp)
