import time

from selenium.common import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from dis_tms.page_obj.first_page import Page
from dis_tms.utils.utilities import upload_files
from dkbssy.utils.colour_prints import ColourPrint


class ThirdPage(Page):
    files_to_upload_dict = {'pp': ('//td[contains(text(),"After Discharge Photo")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"After Discharge Photo")]/parent::tr//select',
                                   'After Discharge Photo'),  # after disc photo
                            'dd': ('//td[contains(text(),"Discharge summary documents")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"Discharge summary documents")]/parent::tr//select',
                                   'Discharge summary documents'),  # discharge
                            'aa': ('//td[contains(text(),"OperationDocuments")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"OperationDocuments")]/parent::tr//select',
                                   'OperationDocuments'),  # anaesthesia
                            'oo': ('//td[contains(text(),"Operative notes")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"Operative notes")]/parent::tr//select',
                                   'Operative notes'),  # operation notes
                            'bb': ('//td[contains(text(),"new born child")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"new born child")]/parent::tr//select',
                                   'Detailed status of the new born child'),  # baby notes
                            'll': ('//td[contains(text(),"Labour charting")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"Labour charting")]/parent::tr//select',
                                   'Labour charting (Only in case of Elective Caesarean Delivery)'),  # labour charting
                            }
    _upload_text = 'pload'
    _verify_and_submit_xp = "//b[normalize-space()='Verify and Submit']"
    _verify_and_submit_pop_up_xp = '//div[normalize-space()="Do you want to Submit ?"]/ancestor::div[@class="modal-content"]//button[normalize-space()="OK"]'
    _attachment_button_close_xp = "//button[@class='btn btn-default btn-fade']"
    _biometric_process_xp = '//input[@value="BIOMETRIC"]'
    _bio_machine_xp = '//div[div[div[contains(text(), "device is connected to the system")]]]//button[contains(text(), "OK")]'
    _biometric_machine_text = "device is connected to the system"

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def attach_table(self) -> list:
        self.switch_frames('modalattDivIframe')
        table_attach = self.find_wait_by_presence('//div[@id="discharge"]')
        t_body = table_attach.find_elements(By.TAG_NAME, "tbody")
        t_body_list = []
        for t_b in t_body:
            t_body_list.append(t_b.text)
        return t_body_list

    def upload_required_or_not(self):
        t_body_list = self.attach_table()
        print(t_body_list)
        count_list = {}
        for k, v in self.files_to_upload_dict.items():
            for i in t_body_list:
                print('i', i)
                n = (i.count(v[2]))
                print('n', n)
                count_list[k] = n
                print('cl', count_list)
        print(count_list)

    def third_page_main(self, location):
        self.upload_required_or_not()
