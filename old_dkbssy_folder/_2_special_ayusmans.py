import os, time, openpyxl, pandas as pd
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import name_for_date_check

casear = '''



CASE/PS5/HS22005049/CK5307484
CASE/PS5/HS22005049/M5302852
CASE/PS5/HS22005049/CK5338926


'''.split('\n')

name_for_date_check.checker_with_dict_output(casear)
input()


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver: WebDriver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)


def login():
    driver.get('https://dkbssy.cg.nic.in/secure/login.aspx')
    driver.maximize_window()
    driver.find_element(By.NAME, "username").send_keys("HS22005049")
    driver.find_element(By.NAME, "password").send_keys("pmjaykorba")
    driver.find_element(By.ID, 'txtCaptcha').click()
    time.sleep(7)  ### SLEEP GIVEN FOR CAPTCHA ENTRY
    sign_in = driver.find_element(By.NAME, "loginbutton")
    sign_in.click()
    new_url = 'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemodule.aspx'
    driver.execute_script(f'window.location.href = "{new_url}"')
    time.sleep(1)
    '''new'''
    driver.execute_script(f'window.location.href = "{new_url}"')

    '''CHOOSING THE DEPARTMENT'''

    department_list = pd.read_excel(r'G:\My Drive\GdrivePC\Hospital\RSBY\Incentive_auto_ver_3_old.xlsx',
                                    sheet_name="Sheet1")
    df = pd.DataFrame(department_list)
    values = df.values
    # print(df.head())
    depart_choice = values[0][1]
    # print(depart_choice)
    ''' depart_choice = DEPARTMENT FOR WHICH ENTRY IS BEING DONE IS PRINTED'''

    list_drop = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_speciality')
    drop_down_list = Select(list_drop)
    drop_down_list.select_by_value(depart_choice)
    # time.sleep(0.1)
    search_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_SearchCases')
    search_button.click()


def entry_proper_3(choosen_case_number):  # WebdriverWait

    t1 = time.time()

    # choosing the desired incentive case
    choosen_incentive_case = wait.until(EC.presence_of_element_located((By.LINK_TEXT, choosen_case_number)))
    try:
        choosen_incentive_case.click()
    except ElementClickInterceptedException:
        for i in range(3):
            try:
                choosen_incentive_case = driver.find_element(By.PARTIAL_LINK_TEXT, choosen_case_number)
                choosen_incentive_case.click()
                print('clicked on next attempts')
                break
            except:
                print('ClickNotPossible on', i)
                continue

    department_and_incentive_names_xl_wbook = openpyxl.load_workbook(
        r'G:\My Drive\GdrivePC\Hospital\RSBY\Incentive_auto_ver_3_old.xlsx')

    incentive_names_to_make_entry_work_sheet1 = department_and_incentive_names_xl_wbook['Sheet1']
    incentive_names_to_extract_as_per_dk_work_sheet2 = department_and_incentive_names_xl_wbook['Sheet2']

    amount_workbook_while_entry = openpyxl.load_workbook(
        r'G:\My Drive\GdrivePC\Hospital\RSBY\Master_amount_sheets.xlsx')

    category_all = ['Administrative Staff - Hospital Consultant', 'Assistant Doctor',
                    'Class IV Employee / Cleanning Staff / Other', 'Data Entry', 'Hospital Head',
                    'Hospital Head & Main Treating Doctor / Surgeon', 'Main Treating Doctor / Surgeon',
                    'OT Technician', 'Other Clinical and Nursing Staff', 'Staff Nurse']

    case_number = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_caseno').text

    final_incentive_names = [case_number]
    depart_name_web = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_speciality"]')
    incentive_amount = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_settledamt"]')
    patient_name = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_patientName"]')
    diagnosis = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_procdName"]')
    pre_auth_date = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Preauth_dt"]')

    final_incentive_names.append(int(incentive_amount.text))
    final_incentive_names.append(depart_name_web.text)
    final_incentive_names.append(diagnosis.text)
    final_incentive_names.append(pre_auth_date.text)
    final_incentive_names.append(patient_name.text)

    number = 2

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
        # print(categ)
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
        # print(incentive_names_to_enter)

        # len number of names in each category
        len_names = len(incentive_names_to_enter)
        print(f'----Number of names in {categ}: ', len_names, "----")

        percentage = None
        if categ == 'Administrative Staff - Hospital Consultant':
            percentage = 0.5 / 100
        elif categ == 'Assistant Doctor':
            percentage = 15 / 100
        elif categ == 'Class IV Employee / Cleanning Staff / Other':
            percentage = 6 / 100
        elif categ == 'Data Entry':
            percentage = 2 / 100
        elif categ == 'Hospital Head':
            percentage = 0.5 / 100
        elif categ == 'Hospital Head & Main Treating Doctor / Surgeon':
            percentage = 0
        elif categ == 'Main Treating Doctor / Surgeon':
            percentage = 45 / 100
        elif categ == 'OT Technician':
            percentage = 4 / 100
        elif categ == 'Other Clinical and Nursing Staff':
            percentage = 20 / 100
        elif categ == 'Staff Nurse':
            percentage = 4 / 100

        for name in incentive_names_to_enter:
            chosen_row_number = dict_name_row_number[name]
            chosen_name_by_dkbssy = incentive_names_to_extract_as_per_dk_work_sheet2.cell(row=chosen_row_number,
                                                                                          column=2).value
            chosen_name_by_dkbssy_post = incentive_names_to_extract_as_per_dk_work_sheet2.cell(row=chosen_row_number,
                                                                                               column=3).value
            print(name, chosen_name_by_dkbssy_post)

            ''' Post wise extracted'''

            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_empCategory"]/option[2]')))
            cat_locator = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$empCategory')
            cat_select = Select(cat_locator)

            cat_select.select_by_visible_text(categ)

            '''waiting for post'''
            "//select[@id='ctl00_ContentPlaceHolder1_empName']/option[text()='Mr. DEVENDRA SINGH GURJAR']"

            new_add_path = f']/option[text()="{chosen_name_by_dkbssy_post}"]'
            str_xpath_pos = '//*[@id="ctl00_ContentPlaceHolder1_empPost"' + new_add_path
            # print(str_xpath_pos)
            wait.until(EC.presence_of_element_located((By.XPATH, str_xpath_pos)))
            # element_post = wait.until(EC.presence_of_element_located((By.XPATH,str_xpath_pos)))
            # wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_empPost"]/option[2]')))
            postLoca = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$empPost')
            postSelect = Select(postLoca)
            # for i in postSelect.options:
            #     print("c",i.text,"CCC")

            # print('p"""', postLoca.text, '"""p')
            postSelect.select_by_visible_text(chosen_name_by_dkbssy_post)
            '''wating for name'''

            new_add_path = f']/option[text()="{chosen_name_by_dkbssy}"]'
            str_xpath_name = '//*[@id="ctl00_ContentPlaceHolder1_empName"' + new_add_path
            # print(str_xpath_name)
            wait.until(EC.presence_of_element_located((By.XPATH, str_xpath_name)))

            nameLoca = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$empName')
            nameSelect = Select(nameLoca)
            if chosen_name_by_dkbssy == "CHANDRAKANTA  SHRIVASTAV ":
                nameSelect.select_by_value('66170020507')
            else:
                nameSelect.select_by_visible_text(chosen_name_by_dkbssy.strip())
            # print('n""""',nameLoca.text,'""""n')
            # print('..........')

            driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$Button1').click()
            # time.sleep(2.5)
            '''wating for table'''  # //*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[7]/td[9]
            new_add_path = f'tr[{number}]/td[9]'
            str_xpath_table = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/' + new_add_path
            # print(str_xpath_table)
            wait.until(EC.presence_of_element_located((By.XPATH, str_xpath_table)))

            new_add_path = f'tr[{number}]/td[5]'  # for getting names
            str_xpath_table = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/' + new_add_path
            table_in_name = wait.until(EC.presence_of_element_located((By.XPATH, str_xpath_table)))
            # print(number,table.text)

            final_incentive_names.append(table_in_name.text)

            # amount calculation during entry
            if name not in amount_workbook_while_entry.sheetnames:
                amount_workbook_while_entry.create_sheet(title=name)
                amount_workbook_while_entry[name].append(
                    ["Case No.", "Amount", "Percent", "Number of person", 0, "Sum"])

            amount_workbook_while_entry[name].append(
                [case_number, int(incentive_amount.text), percentage * 100, len_names,
                 (int(incentive_amount.text)) / len_names * percentage])
            sum_cell = amount_workbook_while_entry[name]["F2"]
            # Enter the SUM formula
            sum_cell.value = "=SUM(E:E)"

            number += 1

    time.sleep(2)
    submit = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$button_submit')
    # time.sleep(7)
    submit.click()

    time.sleep(0.25)
    alert = driver.switch_to.alert
    alert.accept()
    # time.sleep(1)

    to_save_list_df = pd.DataFrame(final_incentive_names).T

    splitted_case_number = case_number.split('/')
    file_name_retrieved = splitted_case_number[-1]
    print(file_name_retrieved)
    save_location = 'G:\\My Drive\\GdrivePC\\Hospital\\RSBY\\Incentive_Entered\\'
    file_name = f'{file_name_retrieved}.csv'
    full_path = os.path.join(save_location, file_name)

    '''saving after submit'''
    to_save_list_df.to_csv(full_path, index=False, header=False)
    print(f'File_name - {file_name} saved')

    wb = openpyxl.load_workbook(r'G:\My Drive\GdrivePC\Hospital\RSBY\MASTER_INCENTIVE_NAMES_ENTRY.xlsx')
    ws = wb['Sheet1']
    ws.append(final_incentive_names)
    wb.save(r'G:\My Drive\GdrivePC\Hospital\RSBY\MASTER_INCENTIVE_NAMES_ENTRY.xlsx')

    # file saving and closing
    # file_to_close = r'G:\My Drive\GdrivePC\Hospital\RSBY\Master_amount_sheets.xlsx'
    # # Create a COM object for Excel
    # excel = win32com.client.Dispatch("Excel.Application")
    # # Check if the specific file is open
    # for wb in excel.Workbooks:
    #     if wb.FullName == file_to_close:
    #         # Save and close the specified workbook
    #         wb.Save()
    #         # wb.Close()
    #         break  # Stop checking once the file is found


    amount_workbook_while_entry.save(r'G:\My Drive\GdrivePC\Hospital\RSBY\Master_amount_sheets.xlsx')

    new_url = 'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemodule.aspx'
    driver.execute_script(f'window.location.href = "{new_url}"')
    # time.sleep(1)

    '''Opening again second incentive form'''
    department_list = pd.read_excel(r'G:\My Drive\GdrivePC\Hospital\RSBY\Incentive_auto_ver_3_old.xlsx', sheet_name="Sheet1")
    df = pd.DataFrame(department_list)
    values = df.values
    # print(df.head())
    depart_choice = values[0][1]
    # print(depart_choice)
    ''' depart_choice = DEPARTMENT FOR WHICH ENTRY IS BEING DONE IS PRINTED'''

    list_drop = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_speciality')
    drop_down_list = Select(list_drop)
    drop_down_list.select_by_value(depart_choice)
    # time.sleep(0.1)
    search_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_SearchCases')
    search_button.click()
    # chosen_incentive_case = driver.find_element(By.PARTIAL_LINK_TEXT, 'CASE')
    # try:
    #     choosen_incentive_case.click()
    # except ElementClickInterceptedException:
    #     for i in range(3):
    #         try:
    #             chosen_incentive_case = driver.find_element(By.PARTIAL_LINK_TEXT, 'CASE')
    #             chosen_incentive_case.click()
    #             print(f"Clicked after {i} attempts")
    #             break
    #         except:
    #             print('PLEASE RESTART THE PROCESS')
    t2 = time.time()
    print('Time required: ', t2 - t1)
    print()
    return case_number




login()
count = 0
cycle_time1 = time.time()
for c in casear:
    if c == "":
        pass
    else:
        print(count + 1, c)
        entry_proper_3(c)
        count += 1
cycle_time2 = time.time()
print(f"Total Cycle Time for {count} cycle:", (cycle_time2 - cycle_time1) / 60)
