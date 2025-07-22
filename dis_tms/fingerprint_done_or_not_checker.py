from selenium.common import TimeoutException

from dis_tms.main_webdriver.create_driver_modu import create_driver
from dis_tms.page_obj.first_page import FirstPage
from dis_tms.page_obj.fourth_page import FourthPage
from dis_tms.page_obj.second_page import SecondPage
from dis_tms.page_obj.third_page import ThirdPage
from dis_tms.utils import utilities


class TmsEntry:
    _user_id = 'CHH008164'
    _password = 'Gmc@12345'

    # _discharge_date = '22/7/2024'

    def main(self, case_numbers):
        driver, wait = create_driver(timeout=3)
        # FirstPage
        first_page_obj = FirstPage(driver, wait)
        first_page_obj.first_page_main(self._user_id, self._password)
        sec_page_obj = SecondPage(driver, wait)
        for case_number in case_numbers.split('\n'):
            sec_page_obj.pre_auth(case_number)
            ip_date = sec_page_obj.get_ip_date()
            print(case_numbers.index(case_number))
            try:
                bio = sec_page_obj.find_wait_by_presence(
                '//b[text()="Authentication at Reg/Dis: "]/parent::label/parent::div').text.split("\n")[1]
                status = sec_page_obj.find_wait_by_presence('//b[text()="Case Status: "]/parent::label/parent::div').text.split("\n")[1]
                print(case_number, "*", ip_date, "*", bio, "*", status)
            except TimeoutException:
                print('done', case_number)
            finally:
                first_page_obj.switch_frames('default')
                first_page_obj.find_wait_by_clickable('//*[@id="sidebar-menu"]/div/ul/li[3]/a/span[1]').click()



case_numbers = '''CASE/PS6/HOSP22G146659/CK7564157
CASE/PS6/HOSP22G146659/CK7702358
CASE/PS6/HOSP22G146659/CK7715140
CASE/PS6/HOSP22G146659/CK7748735
CASE/PS6/HOSP22G146659/CK7753043
CASE/PS7/HOSP22G146659/CK7846082
CASE/PS7/HOSP22G146659/CK7888171
CASE/PS7/HOSP22G146659/CK7934432
CASE/PS7/HOSP22G146659/CK7938685
CASE/PS7/HOSP22G146659/CK7932442
CASE/PS7/HOSP22G146659/CK7938664
CASE/PS7/HOSP22G146659/CB7938702
CASE/PS7/HOSP22G146659/CK7938729
CASE/PS7/HOSP22G146659/CB7955140
CASE/PS7/HOSP22G146659/CK8037614
CASE/PS7/HOSP22G146659/CK8089996
CASE/PS7/HOSP22G146659/CK8037411
CASE/PS7/HOSP22G146659/CK8043683
CASE/PS7/HOSP22G146659/CK8070333
CASE/PS7/HOSP22G146659/CK8074026
CASE/PS7/HOSP22G146659/CK8149454
CASE/PS7/HOSP22G146659/CB8176308
CASE/PS7/HOSP22G146659/CK8202669
CASE/PS7/HOSP22G146659/CK8217449
CASE/PS7/HOSP22G146659/CK8208413
CASE/PS7/HOSP22G146659/CB8244456
CASE/PS7/HOSP22G146659/CK8244185
CASE/PS7/HOSP22G146659/CK8245183
CASE/PS7/HOSP22G146659/CB8391428
CASE/PS7/HOSP22G146659/CK8245634
CASE/PS7/HOSP22G146659/CK8300598
CASE/PS7/HOSP22G146659/CK8312687
CASE/PS7/HOSP22G146659/CK8314458
CASE/PS7/HOSP22G146659/CK8314530
CASE/PS7/HOSP22G146659/CK8316514
CASE/PS7/HOSP22G146659/CK8325104
CASE/PS7/HOSP22G146659/CK8325147
CASE/PS7/HOSP22G146659/CK8325239
CASE/PS7/HOSP22G146659/CK8325526
CASE/PS7/HOSP22G146659/CK8327482
CASE/PS7/HOSP22G146659/CK8340906
CASE/PS7/HOSP22G146659/CK8373745
CASE/PS7/HOSP22G146659/CK8380207
CASE/PS7/HOSP22G146659/CK8382919
CASE/PS7/HOSP22G146659/CK8391141
CASE/PS7/HOSP22G146659/CK8391174
CASE/PS7/HOSP22G146659/CK8391226
CASE/PS7/HOSP22G146659/CK8391248
CASE/PS7/HOSP22G146659/CK8391265
CASE/PS7/HOSP22G146659/CK8391298
CASE/PS7/HOSP22G146659/CK8391320
CASE/PS7/HOSP22G146659/CK8391407
CASE/PS7/HOSP22G146659/CK8391470'''

TmsEntry().main(case_numbers)
