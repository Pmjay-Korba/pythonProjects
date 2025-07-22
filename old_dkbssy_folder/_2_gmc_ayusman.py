import os, time, openpyxl, pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from dkbssy.utils import name_for_date_check_gmc

casear = '''
CASE/PS5/HOSP22G146659/CK5222125	Ophthalmology	SICS with non-foldable IOL	2040	27-08-2022	Narmda Bai
CASE/PS5/HOSP22G146659/CK5276666	Ophthalmology	SICS with non-foldable IOL	2040	09-09-2022	Rukhamani Bai
CASE/PS5/HOSP22G146659/CK5276696	Ophthalmology	SICS with non-foldable IOL	2040	09-09-2022	Rajkumari Das

'''.split('\n')

name_for_date_check_gmc.checker_with_dict_output(casear)
input()

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver: WebDriver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)


def login():
    driver.get('https://dkbssy.cg.nic.in/secure/login.aspx')
    driver.maximize_window()
    driver.find_element(By.NAME, "username").send_keys("HOSP22G146659")
    driver.find_element(By.NAME, "password").send_keys("nic")
    driver.find_element(By.ID, 'txtCaptcha').click()
    time.sleep(7)  ### SLEEP GIVEN FOR CAPTCHA ENTRY
    sign_in = driver.find_element(By.NAME, "loginbutton")
    sign_in.click()
    # time.sleep(2)
    # driver.get("https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduledme.aspx")
    driver.get("https://dkbssy.cg.nic.in/secure/incentivemodule/incentivedetailsdme.aspx?c=CASE/PS5/HOSP22G146659/CK5222125&amt=2040")
    # '''CHOOSING THE DEPARTMENT'''
    #
    # department_list = openpyxl.load_workbook(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto_ver_3.xlsx')
    # dept_name_sheet = department_list['Sheet1']
    # depart_choice = dept_name_sheet['B2'].value
    # # print(depart_choice)
    # list_drop = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_speciality')
    # drop_down_list = Select(list_drop)
    # drop_down_list.select_by_value(depart_choice)
    # from_date = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_fdate")
    # from_date.send_keys('01-08-2022')
    # to_date = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_tdate")
    # to_date.send_keys('30-08-2023')
    # search_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_SearchCases')
    # search_button.click()

def entry_proper_3(choosen_case_number):  # WebdriverWait

    t1 = time.time()
    driver.get(f"https://dkbssy.cg.nic.in/secure/incentivemodule/incentivedetailsdme.aspx?c={choosen_case_number}")

    # choosing the desired incentive case
    # choosen_incentive_case = wait.until(EC.presence_of_element_located((By.LINK_TEXT, choosen_case_number)))
    # choosen_incentive_case.click()
    radio_but_name_wise = wait.until(EC.presence_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_RadioButtonList1_0")))
    radio_but_name_wise.click()

    department_and_incentive_names_xl_wbook = openpyxl.load_workbook(
        r'G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto_ver_3.xlsx')

    incentive_names_to_make_entry_work_sheet1 = department_and_incentive_names_xl_wbook['Sheet1']
    incentive_names_to_extract_as_per_dk_work_sheet2 = department_and_incentive_names_xl_wbook['Sheet2']

    category_all = ['अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल  सलाहकार  ','पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )',
                    'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )','सभी फिजिशियन / सर्जन ','सभी सीनियर एवं जूनियर रेसिडेंट ',
                    'एनेस्थीसिया','नर्सिंग एवं पैरामेडिकल स्टाफ ','चतुर्थ वर्ग एवं सफाई कर्मचारी','डाटा एंट्री ऑपरेटर']

    category_all_value_pair = {'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल  सलाहकार  ':'1',
                    'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )':'2',
                    'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )':'3',
                    'सभी फिजिशियन / सर्जन ':'4', 'सभी सीनियर एवं जूनियर रेसिडेंट ':'5',
                    'एनेस्थीसिया':'6', 'नर्सिंग एवं पैरामेडिकल स्टाफ ':'7', 'चतुर्थ वर्ग एवं सफाई कर्मचारी':'8',
                    'डाटा एंट्री ऑपरेटर':'9'}

    case_number = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_caseno').text

    final_incentive_names = [case_number]
    depart_name_web = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_dis_main_name"]')

    incentive_amount = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_settledamt"]')
    patient_name = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_patientName"]')
    diagnosis = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_procdName"]')
    pre_auth_date = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Label1"]')

    # print(case_number,incentive_amount.text,depart_name_web.text,diagnosis.text, pre_auth_date.text,patient_name.text)

    final_incentive_names.append(int(incentive_amount.text))
    final_incentive_names.append(depart_name_web.text)
    final_incentive_names.append(diagnosis.text)
    final_incentive_names.append(pre_auth_date.text)
    final_incentive_names.append(patient_name.text)

    number = 1

    extract_dk_names = incentive_names_to_extract_as_per_dk_work_sheet2.iter_rows(min_col=1, max_col=1)
    dict_name_row_number = {}
    for namez in extract_dk_names:
        # print(namez[0].value)
        name_is = namez[0].value
        row_number = namez[0].row
        # print({name_is: row_number})
        dict_name_row_number[name_is] = row_number
    # print(dict_name_row_number)

    for categ in category_all:
        incentive_names_to_enter = []
        # print('aaaaaaaa',categ)
        col_index = None
        for cell in incentive_names_to_make_entry_work_sheet1[1]:  # getting the column index of categ
            if cell.value == categ:
                col_index = cell.column
                # print(col_index)
        column_values_modified_for_categ = incentive_names_to_make_entry_work_sheet1.iter_cols(
            min_col=col_index, max_col=col_index, min_row=2, max_row=26)
        for row in column_values_modified_for_categ:
            row_data = [cell.value for cell in row]
            incentive_names_to_enter += row_data
        incentive_names_to_enter = [i for i in incentive_names_to_enter if i is not None]
        # print('sssssssssss',incentive_names_to_enter)

        # len number of names in each category
        len_names = len(incentive_names_to_enter)
        # print(f'----Number of names in {categ}: ', len_names, "----")
        number += len_names

        # waiting for names to upload
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_empCategory"]/option[10]')))
        cat_locator = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$empCategory')
        cat_select = Select(cat_locator)
        # ops = cat_select.options
        # for op in ops:
        #     print(op.text)
        cat_select.select_by_value(category_all_value_pair[categ])
        # time.sleep(2)#working with this sleep

        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_empName"]/option[7]')))
        name_wait_elem = wait.until(EC.presence_of_element_located((By.ID,'ctl00_ContentPlaceHolder1_empName')))
        # print('xx----', name_wait_elem.text)

        for name in incentive_names_to_enter:
            # chosen_row_number = dict_name_row_number[name]
            # chosen_name_by_dkbssy = incentive_names_to_extract_as_per_dk_work_sheet2.cell(row=chosen_row_number,
            #                                                                               column=2).value
            # chosen_name_by_dkbssy_post = incentive_names_to_extract_as_per_dk_work_sheet2.cell(row=chosen_row_number,
            #                                                                                    column=3).value
            # # print(name,chosen_name_by_dkbssy_post)
            #
            # print(name)
            name_select = Select(name_wait_elem)
            if name == "CHANDRAKANTA  SHRIVASTAV":
                name_select.select_by_value('66170020507')
            else:
                name_select.select_by_visible_text(name) #chosen_name_by_dkbssy.strip()

        #Add staff
        add_staff = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$Button1')
        add_staff.click()

        # print(len_names, number)

        '''wating for table'''  # //*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[7]/td[9]
        print('-------',categ,': Names - ',len_names,'-------')

        for num in range(number+1-len_names, number+1 ):
            # print('zzzzz', num)
            new_add_path = f'tr[{num}]/td[6]'  # for getting names
            str_xpath_table = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/' + new_add_path
            table_in_name = wait.until(EC.presence_of_element_located((By.XPATH, str_xpath_table)))
            # table_in_categ = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[{num}]/td[3]')))

            print(table_in_name.text)
            final_incentive_names.append(table_in_name.text)

    # print(final_incentive_names)

    submit = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolder1$button_submit')))
    submit.click()
    time.sleep(0.25)
    alert = driver.switch_to.alert
    # alert.accept()

    to_save_list_df = pd.DataFrame(final_incentive_names).T

    splitted_case_number = case_number.split('/')
    file_name_retrieved = splitted_case_number[-1]
    # print(file_name_retrieved)
    save_location = 'G:\\My Drive\\GdrivePC\\Hospital\\RSBY\\Incentive_Entered\\'
    file_name = f'{file_name_retrieved}.csv'
    full_path = os.path.join(save_location, file_name)

    '''saving after submit'''
    to_save_list_df.to_csv(full_path, index=False, header=False)
    print(f'File_name - {file_name} saved')

    wb = openpyxl.load_workbook(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\MASTER_INCENTIVE_NAMES_ENTRY.xlsx')
    ws = wb['Sheet1']
    ws.append(final_incentive_names)
    wb.save(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\MASTER_INCENTIVE_NAMES_ENTRY.xlsx')

    t2 = time.time()
    print('Time required: ', t2 - t1)
    print()



login()
cycle_time1 = time.time()
count = 0
for c in casear:
    if c == "":
        pass
    else:
        # print(c)
        yy = c.split('\t')
        'CASE/PS5/HOSP22G146659/CK5222125&amt=2040'
        cna = yy[0] +'&amt=' + yy[3]
        print(count + 1, cna)
        entry_proper_3(cna)
        count += 1
cycle_time2 = time.time()
print(f"Total Cycle Time for {count} cycle (min): ", (cycle_time2 - cycle_time1) / 60)