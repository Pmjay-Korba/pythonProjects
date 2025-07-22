import time
import openpyxl
from selenium.common import TimeoutException
from dis_tms.main_webdriver.create_driver_modu import create_driver
from dkbssy.dk_pages.dk_login_page import FirstPage, check_chrome_and_tab
from dkbssy.dk_pages.fifth_page import FifthPage
from dkbssy.dk_pages.fourth_page import FourthPage
from dkbssy.dk_pages.second_page import SecondPage
from dkbssy.dk_pages.third_page import ThirdPage
from dkbssy.dk_pages.sixth_page import IncentiveScraper
from dkbssy.utils import file_renamer, incen_percent
from dkbssy.utils.colour_prints import ColourPrint
from dkbssy.utils.excel_and_sql_matcher import CheckerUpdate
from dkbssy.utils.excel_utils import ExcelMethods
from dkbssy.utils.file_renamer import get_default_download_dir
from dkbssy.utils.sqlite_updation_long import sql_update
from dkbssy.utils import name_for_date_check_gmc
from dkbssy.utils import entry_via_query
from dkbssy.utils import excel_utils

class DkbssyIncentiveEntry:
    # Define the download directory
    # download_dir = r"G:\My Drive\GdrivePC\Hospital\RSBY\New\down"  # Use raw string notation for Windows paths
    download_dir = get_default_download_dir()  # Use raw string notation for Windows paths

    username_key = "HOSP22G146659"
    pass_key = "Pmjaykorba@1"
    # from_date = '01-08-2022'
    from_date = '2022-08-01'
    # to_date = '31-12-2023'
    to_date = '2023-12-31'
    page_title_given = 'Shaheed Veer Narayan Singh Ayushman Swasthya Yojna'

    def main(self, all_casear):

        # function ran
        name_for_date_check_gmc.checker_with_dict_output(all_casear.split('\n'))

        is_chrome_dev_open = check_chrome_and_tab(target_title=self.page_title_given)
        # print(is_chrome_dev_open)
        if not is_chrome_dev_open:
            ColourPrint.print_pink('FIRST LOGIN IN TO THE "APPROVER SITE" BY USING THE EDGE-DEV')

        def file_attach_check():
            is_correct = False
            while not is_correct:
                file_loc = input("Enter File Path: ").strip('"')

                is_correct = input("Press Enter to continue, 1 for re-enter file location")
                if is_correct == '1':
                    print("Press Enter to input file path again")
                    is_correct = False
                else:
                    return file_loc
            return None

        attach_file_path = file_attach_check()
        # input("Press Enter to continue")
        global final_names

        driver, wait = create_driver(timeout=120,port_value='9222', title_given='Shaheed Veer Narayan Singh Ayushman Swasthya Yojna')
        first_page_obj = FirstPage(driver, wait)

        "commenting this for CDP mode as already signed in"
        # first_page_obj.sign_in(username_key=self.username_key, pass_key=self.pass_key)
        # time.sleep(2)

        depart_choice = ExcelMethods().entry_department()
        sec_page_obj = SecondPage(driver, wait)

        '''"making this by playwright"
        sec_page_obj.select_department_use(depart_choice)
        sec_page_obj.from_to_date_entry_use(self.from_date, self.to_date)
        '''
        sec_page_obj.async_second_page(depart_choice=depart_choice, from_date=self.from_date, to_date=self.to_date)
        case_numbers_to_do_list = incen_percent.case_cycle(all_casear)
        # all case_numbers = case_numbers_to_do
        for case_number in case_numbers_to_do_list:
            t1 = time.time()
            ColourPrint.print_pink(str(case_numbers_to_do_list.index(case_number) + 1), case_number)

            ColourPrint.print_turquoise("Query Modify")
            # query_modify = f'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApViewDME.aspx?ci={case_number}&{amount}'
            query_modify = f'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApViewDME.aspx?ci={case_number}'
            ColourPrint.print_yellow(query_modify)

            sec_page_obj.web_selection_of_case_use(case_number)


            # third page
            third_page_obj = ThirdPage(driver, wait)
            third_page_obj.name_radio_click_use()
            excel_meths_obj = ExcelMethods()

            '''inserting the names according to category'''
            # get the incentives names with Category in header
            cat_and_name_lol = excel_meths_obj.get_cat_wise_inc_names()
            final_names = third_page_obj.cat_and_name_entry_proper_use(cat_and_name_lol)
            '''submit button'''
            third_page_obj.final_submit(attach_file_path)

            """ ---> Adding to the Excel for getting the STUCK at Query stage """
            query_stage_excel = r"G:\My Drive\GdrivePC\Hospital\RSBY\New\down\query_stage_pending.xlsx"
            excel_utils.add_in_excel_for_query_stage_pending(excel_path=query_stage_excel, case_number=case_number)

            'Excel and SQL'
            excel_meths_obj.excel_saves(final_names)
            excel_meths_obj.sql_save(final_names)
            t2 = time.time()

            '''Adding the amount checking steps''' "--> ADDED BUT NOT IMPROVED BY THIS"
            # third_page_obj.entry_done_verify()


            '''Going to authorize browser and raising query'''
            # entry_via_query.dk_via_query(case_number=case_number)

            entry_via_query.dk_play_async(case_number=case_number)

            '''Coming again in old browser and clearing the query'''
            # third_page_obj.going_to_query_to_reinitate(case_number=case_number)  # selenium based
            entry_via_query.dk_play_async_submit(case_number)  # playwright based

            '''  <--- Removing the case number from the QUERY STUCK Excel'''
            excel_utils.remove_case_number_from_excel(excel_path=query_stage_excel, case_number=case_number)

            ColourPrint.print_blue(str(t2 - t1))

            '''reloading the page'''
            '''"making this by playwright"
                sec_page_obj.select_department_use(depart_choice)
                sec_page_obj.from_to_date_entry_use(self.from_date, self.to_date)
            '''
            sec_page_obj.async_second_page(depart_choice=depart_choice, from_date=self.from_date, to_date=self.to_date)

        '''All entry complete'''

        '''Checking Removing, Adding to database 2'''
        # download file - skipped in newer version
        # file_renamer.download_and_rename_file(driver, wait, self.download_dir)

        # check for record to delete
        check_update_object = CheckerUpdate()
        check_update_object.sql_delete_cycle_2()

        # after all entry, update incentive_db_2 by direct web check
        to_be_updated_excel_diff = check_update_object.update_record()
        to_be_updated_in_sql = check_update_object.check_proper_to_update_sql()
        to_be_updated_in_sql = to_be_updated_excel_diff + to_be_updated_in_sql
        fifth_page_obj = FifthPage(driver, wait)


        print(f'To be updated - Total:{len(to_be_updated_in_sql)}')
        IncentiveScraper().start(to_be_updated_in_sql)


        fourth_page_obj = FourthPage(driver, wait)
        fourth_page_obj.updating_amount_use(final_names)

# if __name__ == '__main__':
#     dk = DkbssyIncentiveEntry()
#     dk.main('CASE/PS5/HOSP22G146659/CK5678370')
