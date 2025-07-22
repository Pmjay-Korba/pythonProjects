from dis_tms.main_webdriver.create_driver_modu import create_driver
from dis_tms.page_obj.first_page import FirstPage
from dis_tms.page_obj.fourth_page import FourthPage
from dis_tms.page_obj.second_page import SecondPage
from dis_tms.page_obj.third_page import ThirdPage
from dis_tms.utils import utilities


class TmsEntry:
    def __init__(self, user_id, password):
        self._user_id = user_id
        self._password = password
        self.driver, self.wait = create_driver(timeout=5)

    def entry_cycle(self, case_number, discharge_date, location):
        # for checking files
        utilities.check_files_in_folder_before_tms_start(location)  # return files path dict
        # SecondPage
        second_page_obj = SecondPage(self.driver, self.wait)
        second_page_obj.second_page_main(case_number, discharge_date)
        third_page_obj = ThirdPage(self.driver, self.wait)
        third_page_obj.third_page_main(location)
        fourth_page_obj = FourthPage(self.driver, self.wait)
        # fourth_page_obj.initiate()

    def main(self, case_number, discharge_date, location):
        # FirstPage
        first_page_obj = FirstPage(self.driver, self.wait)
        first_page_obj.first_page_main(self._user_id, self._password)
        self.entry_cycle(case_number, discharge_date, location)


tms = TmsEntry('CHH008164', 'Gmc@12345')
tms.main(case_number=input('Case Number: ') or 'CASE/PS7/HOSP22G146659/CK8245183',
         discharge_date=input("Discharge Date: ") or '16-6-24',
         location=input("Folder/File location") or r'G:\My Drive\GdrivePC\2024\JUNE\13.06.2024\MULANI RATHORE\lll.jpg')
