import time
import openpyxl
import pandas as pd
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from dkbssy.dk_pages.dk_login_page import Page
from dkbssy.utils.colour_prints import ColourPrint
from selenium.webdriver.support import expected_conditions as EC
from dkbssy.utils.incen_percent import inc_percent_amt_calc
from dkbssy.utils.excel_utils import ExcelMethods


class ThirdPage(Page):
    _radio_name_xpath = '//*[@id="ctl00_ContentPlaceHolder1_RadioButtonList1_0"]'
    _web_category_xpath = '//*[@id="ctl00_ContentPlaceHolder1_empCategory"]'
    _waiting_for_category_xpath = '//*[@id="ctl00_ContentPlaceHolder1_empCategory"]/option[10]'
    _web_emp_name_xpath = '//*[@id="ctl00_ContentPlaceHolder1_empName"]'
    _waiting_for_emp_name_xpath = '//*[@id="ctl00_ContentPlaceHolder1_empName"]/option[7]'
    _add_staff_button_xpath = '//input[@value="Add Staff"]'
    _submit_button_xpath = '//*[@id="ctl00_ContentPlaceHolder1_button_submit"]'
    _attachment_file_xpath = '//*[@id="ctl00_ContentPlaceHolder1_FileUpload1"]'

    _category_all_value_pair = {
        'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल  सलाहकार  ': '1',
        'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )': '2',
        'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )': '3',
        'सभी फिजिशियन / सर्जन ': '4', 'सभी सीनियर एवं जूनियर रेसिडेंट ': '5',
        'एनेस्थीसिया': '6', 'नर्सिंग एवं पैरामेडिकल स्टाफ ': '7', 'चतुर्थ वर्ग एवं सफाई कर्मचारी': '8',
        'डाटा एंट्री ऑपरेटर': '9'
    }

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def case_details(self):
        case_number = self.find_wait_by('//*[@id="ctl00_ContentPlaceHolder1_caseno"]').text
        depart_name_web = self.find_wait_by('//*[@id="ctl00_ContentPlaceHolder1_dis_main_name"]').text
        incentive_amount = self.find_wait_by('//*[@id="ctl00_ContentPlaceHolder1_settledamt"]').text
        patient_name = self.find_wait_by('//*[@id="ctl00_ContentPlaceHolder1_patientName"]').text
        diagnosis = self.find_wait_by('//*[@id="ctl00_ContentPlaceHolder1_procdName"]').text
        pre_auth_date = self.find_wait_by('//*[@id="ctl00_ContentPlaceHolder1_Label1"]').text
        return case_number, depart_name_web, incentive_amount, patient_name, diagnosis, pre_auth_date

    def name_radio_click_use(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self._radio_name_xpath))).click()
        except (TimeoutException, ElementClickInterceptedException) as e:
            element = self.driver.find_element(By.XPATH, self._radio_name_xpath)
            self.driver.execute_script("arguments[0].click();", element)

    def selection_of_category(self, cat_value):
        # waiting to load
        self.find_wait_by(self._waiting_for_category_xpath)
        # continue
        web_cat_select = self.find_wait_by(self._web_category_xpath)
        cat_select_class = Select(web_cat_select)
        cat_select_class.select_by_value(str(cat_value))

    def selection_of_names(self, list_emp_name):
        # waiting for name to load
        self.find_wait_by(self._waiting_for_emp_name_xpath)
        # continue
        web_emp_name_select = self.find_wait_by(self._web_emp_name_xpath)
        emp_select_class = Select(web_emp_name_select)
        for name in list_emp_name:
            if name == 'MAHENDRA KUMAR HOUSE':
                emp_select_class.select_by_value('N55171003')
            elif name == 'MAHENDRA KUMAR EYE':
                emp_select_class.select_by_value('05170011797')
            elif name == 'MAHENDRA KUMAR':
                raise ValueError("Unexpected employee name: 'MAHENDRA KUMAR'. Choose either MAHENDRA KUMAR EYE or MAHENDRA KUMAR HOUSE")
            else:
                emp_select_class.select_by_visible_text(name)


    def cat_and_name_entry_proper_use(self, cat_and_name_lol):
        final_incentive_names = []
        number = 1
        # function run
        case_number, depart_name_web, incentive_amount, patient_name, diagnosis, pre_auth_date = self.case_details()
        final_incentive_names.append([case_number, float(incentive_amount), depart_name_web, diagnosis, pre_auth_date, patient_name])
        for each_cat_and_name in cat_and_name_lol:
            cat = each_cat_and_name[0]  # hindi category
            cat_value = self._category_all_value_pair[cat]  # 1
            # function run
            percentage = inc_percent_amt_calc(cat)
            names = each_cat_and_name[1:]
            len_names = len(names)
            number += len_names
            if len_names != 0:
                # function run
                self.selection_of_category(cat_value)
                # function run
                self.selection_of_names(names)
                self.add_staff()
                cat_group_inc_amt = self.waiting_for_table(cat, len_names, number, percentage, incentive_amount)
                final_incentive_names.append([cat_group_inc_amt])
            else:
                pass
        # function run
        final_incentive_names_list = ExcelMethods().flatten_list(final_incentive_names)
        return final_incentive_names_list

    def add_staff(self):
        add_butt = self.wait.until(EC.element_to_be_clickable((By.XPATH, self._add_staff_button_xpath)))
        add_butt.click()

    def waiting_for_table(self, cat, len_names, number, percentage, incentive_amount):
        ColourPrint.print_turquoise(f'------------------- {cat} - Names: {len_names} -------------------')
        incentive_names_amount_cat = []
        for num in range(number + 1 - len_names, number + 1):
            _web_name_xpath = f'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[{num}]/td[6]'
            name_in_web_table = self.find_wait_by(_web_name_xpath).text

            name_amount = name_in_web_table + '@' + str(
                percentage * float(incentive_amount) / len_names) + '#' + self._category_all_value_pair[cat]
            print(name_amount)
            incentive_names_amount_cat.append(name_amount)
        return incentive_names_amount_cat

    def final_submit(self, attach_file_path):
        attach_button = self.find_wait_by(self._attachment_file_xpath)
        attach_button.send_keys(attach_file_path)
        submit_button = self.find_wait_by(self._submit_button_xpath)
        submit_button.click()
        time.sleep(0.25)
        alert = self.driver.switch_to.alert
        alert.accept()

    def entry_done_verify(self):
        entry_done_xp = "//div[@class='swal-text']"
        self.find_wait_by(entry_done_xp)  #  checking the pop-up for 'Now This Case Show In Hospital Approver Login !'
        self.find_wait_by("//button[normalize-space()='OK']").click()  # clicking the OK button

        table_text = self.find_wait_by('(//tbody[@id="incentiveTableData"]/tr/td)[1]').text  # waiting for populating table
        print('Table text in verification table', table_text)
        time.sleep(1)
        self.find_wait_by("//a[normalize-space()='Cancel']").click()  # clicking cancel

    def going_to_query_to_reinitate(self, case_number):
        print('Original Site - Here in reinitate')
        self.driver.get(f'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleQuerryViewDME_Edit.aspx?ci={case_number}')

        try:
            self.find_wait_by('//*[@id="ctl00_ContentPlaceHolder1_button_submit"]').click()  # clicking the SUBMIT button
        except ElementClickInterceptedException as e:
            ColourPrint.print_pink("Submit click error")
            self.find_wait_by('//*[@id="ctl00_ContentPlaceHolder1_button_submit"]').click()  # clicking the SUBMIT button

        alert = self.driver.switch_to.alert
        alert.accept()
        self.find_wait_by('/html/body/div[3]/div/div[3]/div/button')  # wait for OK button







