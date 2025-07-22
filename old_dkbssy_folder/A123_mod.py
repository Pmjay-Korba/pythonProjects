import datetime
import os, time, openpyxl, pandas as pd
import sys
import sqlite3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

# casear = '''
#
# CASE/PS5/HOSP22G146659/CK5327589	Ophthalmology	SICS with non-foldable IOL	2040	21-09-2022	Suni Bai
#
# '''.split('\n')
# name_for_date_check_gmc.checker_with_dict_output(casear)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver: WebDriver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)


def login():
    driver.get('https://dkbssy.cg.nic.in/secure/login.aspx')
    driver.maximize_window()
    driver.find_element(By.NAME, "username").send_keys("HOSP22G146659")
    driver.find_element(By.NAME, "password").send_keys("pmjaykorba")
    driver.find_element(By.ID, 'txtCaptcha').click()
    time.sleep(7)  ### SLEEP GIVEN FOR CAPTCHA ENTRY
    sign_in = driver.find_element(By.NAME, "loginbutton")
    sign_in.click()
    # time.sleep(2)
    driver.get("https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduledme.aspx")
    # driver.get("https://dkbssy.cg.nic.in/secure/incentivemodule/incentivedetailsdme.aspx?c=CASE/PS5/HOSP22G146659/CK5222125&amt=2040")
    '''CHOOSING THE DEPARTMENT'''

    department_list = openpyxl.load_workbook(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto_ver_3.xlsx')
    dept_name_sheet = department_list['Sheet1']
    depart_choice = dept_name_sheet['B2'].value
    # print(depart_choice)
    list_drop = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_speciality')
    drop_down_list = Select(list_drop)
    drop_down_list.select_by_value(depart_choice)
    from_date = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_fdate")
    from_date.send_keys('01')  # from_date.send_keys('01-08-2022')
    # from_date.send_keys(Keys.ARROW_RIGHT)  # Move to month
    # time.sleep(1)
    from_date.send_keys('08')  # from_date.send_keys('01-08-2022')
    # time.sleep(1)
    from_date.send_keys(Keys.ARROW_RIGHT)  # Move to month
    from_date.send_keys('2022')  # from_date.send_keys('01-08-2022')
    # from_date.send_keys(Keys.ARROW_RIGHT)  # Move to month

    to_date = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_tdate")
    to_date.send_keys('31')
    # time.sleep(1)
    to_date.send_keys('12')  # from_date.send_keys('01-08-2022')
    # time.sleep(1)
    to_date.send_keys(Keys.ARROW_RIGHT)  # Move to month
    to_date.send_keys('2023')  # from_date.send_keys('01-08-2022')
    search_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_SearchCases')
    search_button.click()


def entry_proper_3(choosen_case_number, amount):  # WebdriverWait

    t1 = time.time()
    # driver.get(f"https://dkbssy.cg.nic.in/secure/incentivemodule/incentivedetailsdme.aspx?c={choosen_case_number}")

    # choosing the desired incentive case
    driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_GridView1_filter"]/label/input').send_keys(
        choosen_case_number)
    try:
        choosen_incentive_case = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr/td[2]/a'))).text
        # choosen_incentive_case = wait.until(EC.presence_of_element_located((By.LINK_TEXT, choosen_case_number)))
        print("web-item case number", choosen_incentive_case)
        if choosen_incentive_case == choosen_case_number:
            driver.get(
                f"https://dkbssy.cg.nic.in/secure/incentivemodule/incentivedetailsdme.aspx?c={choosen_case_number}&amt={amount}")
    except:
        sys.exit('ALREADY INCENTIVE ENTRY DONE')

    radio_but_name_wise = wait.until(
        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_RadioButtonList1_0")))
    try:
        # radio_but_name_wise = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_RadioButtonList1_0")))
        radio_but_name_wise.click()
    except Exception as e:
        try:
            driver.execute_script("arguments[0].click();", radio_but_name_wise)
        except:
            sys.exit('Radio button error')

    department_and_incentive_names_xl_wbook = openpyxl.load_workbook(
        r'G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto_ver_3.xlsx')

    incentive_names_to_make_entry_work_sheet1 = department_and_incentive_names_xl_wbook['Sheet1']
    incentive_names_to_extract_as_per_dk_work_sheet2 = department_and_incentive_names_xl_wbook['Sheet2']

    category_all = ['अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल  सलाहकार  ',
                    'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )',
                    'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )',
                    'सभी फिजिशियन / सर्जन ', 'सभी सीनियर एवं जूनियर रेसिडेंट ',
                    'एनेस्थीसिया', 'नर्सिंग एवं पैरामेडिकल स्टाफ ', 'चतुर्थ वर्ग एवं सफाई कर्मचारी',
                    'डाटा एंट्री ऑपरेटर']

    category_all_value_pair = {
        'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल  सलाहकार  ': '1',
        'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )': '2',
        'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )': '3',
        'सभी फिजिशियन / सर्जन ': '4', 'सभी सीनियर एवं जूनियर रेसिडेंट ': '5',
        'एनेस्थीसिया': '6', 'नर्सिंग एवं पैरामेडिकल स्टाफ ': '7', 'चतुर्थ वर्ग एवं सफाई कर्मचारी': '8',
        'डाटा एंट्री ऑपरेटर': '9'}

    case_number = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_caseno').text

    final_incentive_names = [case_number]
    depart_name_web = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_dis_main_name"]')

    incentive_amount = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_settledamt"]')
    patient_name = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_patientName"]')
    diagnosis = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_procdName"]')
    pre_auth_date = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Label1"]')

    # print(case_number,incentive_amount.text,depart_name_web.text,diagnosis.text, pre_auth_date.text,patient_name.text)

    final_incentive_names.append(float(incentive_amount.text))
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

    current_timestamp = str(datetime.datetime.now())
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

        percentage = None
        if categ == 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल  सलाहकार  ':
            percentage = .01
        elif categ == 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )':
            percentage = .14
        elif categ == 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )':
            percentage = 0.06
        elif categ == 'सभी फिजिशियन / सर्जन ':
            percentage = .45
        elif categ == 'सभी सीनियर एवं जूनियर रेसिडेंट ':
            percentage = .1
        elif categ == 'एनेस्थीसिया':
            percentage = .1
        elif categ == 'नर्सिंग एवं पैरामेडिकल स्टाफ ':
            percentage = .06
        elif categ == 'चतुर्थ वर्ग एवं सफाई कर्मचारी':
            percentage = .03
        elif categ == 'डाटा एंट्री ऑपरेटर':
            percentage = .05

        if len_names == 0:  # skipping the empty category e.g. Anaesthesia
            pass
        else:
            cat_select.select_by_value(category_all_value_pair[categ])
            # time.sleep(2)#working with this sleep

            wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_empName"]/option[7]')))
            name_wait_elem = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_empName')))
            # print('xx----', name_wait_elem.text)

            for name in incentive_names_to_enter:
                # print(name, 'enrty***************************')
                name_select = Select(name_wait_elem)
                # if name == "CHANDRAKANTA  SHRIVASTAV":
                #     name_select.select_by_value('66170020507')
                if name == "MAHENDRA KUMAR N55171003":
                    name_select.select_by_value('N55171003')
                elif name == name == "MAHENDRA KUMAR":
                    name_select.select_by_value('05170011797')
                else:
                    name_select.select_by_visible_text(name)  # chosen_name_by_dkbssy.strip()

            # Add staff
            add_staff = wait.until(EC.element_to_be_clickable((By.NAME, 'ctl00$ContentPlaceHolder1$Button1')))
            add_staff.click()

            # print(len_names, number)

            '''wating for table'''  # //*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[7]/td[9]
            print('-------', categ, ': Names - ', len_names, '-------')

            for num in range(number + 1 - len_names, number + 1):
                # print('zzzzz', num, len_names, number)
                # new_post_path = f'tr[{num}]/td[5]'  # for getting post web
                # xpath_in_post = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/' + new_post_path
                # table_in_post = wait.until(EC.presence_of_element_located((By.XPATH, xpath_in_post)))

                new_add_path = f'tr[{num}]/td[6]'  # for getting names
                str_xpath_table = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/' + new_add_path
                table_in_name = wait.until(EC.presence_of_element_located((By.XPATH, str_xpath_table)))
                category_in_name_text = wait.until(EC.presence_of_element_located((By.XPATH, f'//*['
                                                                                             f'@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[{num}]/td[3]'))).text

                # if table_in_post

                # table_in_categ = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[{num}]/td[3]')))
                name_amount = table_in_name.text + '@' + str(
                    percentage * float(incentive_amount.text) / len_names) + '#' + category_all_value_pair[categ]
                print(name_amount)
                final_incentive_names.append(name_amount)

    # print(final_incentive_names)

    # input("check and press enter")
    submit = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolder1$button_submit')))
    submit.click()
    time.sleep(0.25)
    alert = driver.switch_to.alert

    alert.accept()

    to_save_list_df = pd.DataFrame(final_incentive_names).T

    splitted_case_number = case_number.split('/')
    file_name_retrieved = splitted_case_number[-1]
    # print(file_name_retrieved)
    save_location = 'G:\\My Drive\\GdrivePC\\Hospital\\RSBY\\New\\Incentive_Entered_New\\'
    file_name = f'{file_name_retrieved}.csv'
    full_path = os.path.join(save_location, file_name)

    '''saving after submit'''
    to_save_list_df.to_csv(full_path, index=False, header=False)
    print(f'File_name - {file_name} saved')

    # sqlite3
    conn = sqlite3.connect(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\incentiveDatabase.db')
    cur = conn.cursor()
    try:
        # Prepare the SELECT statement to check if the case number exists
        check_statement = "SELECT 1 FROM incentive_entry_T WHERE incentive_case_number = ? LIMIT 1"
        # Execute the SELECT statement
        cur.execute(check_statement, (choosen_case_number,))
        result = cur.fetchone()

        # If the case number is found, proceed to delete
        if result:
            # Prepare the DELETE statement
            delete_statement = "DELETE FROM incentive_entry_T WHERE incentive_case_number = ?"
            # Execute the DELETE statement
            cur.execute(delete_statement, (choosen_case_number,))

        for inc_nam in final_incentive_names[6:]:
            cur.execute('''
                INSERT INTO incentive_entry_T (employee_name, incentive_case_number, incentive_amount, inc_categ, timestamp)
                VALUES (?,?,?,?,?)''',
                        (inc_nam.split('@')[0], final_incentive_names[0], inc_nam.split('@')[1].split('#')[0], inc_nam.split('#')[1], current_timestamp))

        conn.commit()
        conn.close()
    except Exception as e:
        print("ERROR OCCURRED, ROLLBACK")
        conn.rollback()

    wb = openpyxl.load_workbook(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\MASTER_INCENTIVE_NAMES_ENTRY.xlsx')
    ws = wb['Sheet1']
    ws.append(final_incentive_names)
    wb.save(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\MASTER_INCENTIVE_NAMES_ENTRY.xlsx')

    t2 = time.time()
    print('Time required: ', t2 - t1)
    print()

    # resetting for next cycle
    driver.get("https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduledme.aspx")
    # driver.get("https://dkbssy.cg.nic.in/secure/incentivemodule/incentivedetailsdme.aspx?c=CASE/PS5/HOSP22G146659/CK5222125&amt=2040")
    '''CHOOSING THE DEPARTMENT'''

    department_list = openpyxl.load_workbook(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto_ver_3.xlsx')
    dept_name_sheet = department_list['Sheet1']
    depart_choice = dept_name_sheet['B2'].value
    # print(depart_choice)
    list_drop = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_speciality')
    drop_down_list = Select(list_drop)
    drop_down_list.select_by_value(depart_choice)
    from_date = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_fdate")
    from_date.send_keys('01')  # from_date.send_keys('01-08-2022')
    # from_date.send_keys(Keys.ARROW_RIGHT)  # Move to month
    # time.sleep(1)
    from_date.send_keys('08')  # from_date.send_keys('01-08-2022')
    # time.sleep(1)
    from_date.send_keys(Keys.ARROW_RIGHT)  # Move to month
    from_date.send_keys('2022')  # from_date.send_keys('01-08-2022')
    # from_date.send_keys(Keys.ARROW_RIGHT)  # Move to month

    to_date = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_tdate")
    to_date.send_keys('31')
    # time.sleep(1)
    to_date.send_keys('12')  # from_date.send_keys('01-08-2022')
    # time.sleep(1)
    to_date.send_keys(Keys.ARROW_RIGHT)  # Move to month
    to_date.send_keys('2023')  # from_date.send_keys('01-08-2022')
    search_button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_SearchCases')
    search_button.click()


def cycle(all_casear):
    casear = all_casear.split('\n')
    # name_for_date_check_gmc.checker_with_dict_output(casear)
    login()
    count = 0
    cycle_time1 = time.time()
    for c in casear:  # casear = list
        if c == "":
            pass
        else:
            # print(c)
            yy = c.split('\t')
            # 'CASE/PS5/HOSP22G146659/CK5222125&amt=2040'
            case_num, amount = yy[0], yy[3]
            print(count + 1, case_num)
            entry_proper_3(case_num, amount)
            count += 1
    cycle_time2 = time.time()
    print(f"Total Cycle Time for {count} cycle (min): ", (cycle_time2 - cycle_time1) / 60)


'''combining the amount getter'''


def emp_code(code):
    # driver.get('https://dkbssy.cg.nic.in/secure/incentivemodule/IncentiveDetails_EmpCodeWiseDME.aspx')
    driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$TextBox1').send_keys(code)
    driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$search').click()
    new_path = (f'//*[@id="ctl00_ContentPlaceHolder1_TextBox1" and @value="{code}"]')
    wait.until(EC.presence_of_element_located((By.XPATH, new_path)))

    total_amount_pending = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Label4"]')
    total_paid_cases = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Label14"]')
    total_paid_amount = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Label5"]')
    try:
        number_of_cases_pending = driver.find_element(By.XPATH,
                                                      '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[2]/td[3]').text
    except NoSuchElementException:
        number_of_cases_pending = 0
    print(code, '\t', number_of_cases_pending, '\t', total_amount_pending.text, '\t', total_paid_cases.text, '\t',
          total_paid_amount.text)
    driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$TextBox1').clear()
    return code, number_of_cases_pending, total_amount_pending.text, total_paid_cases.text, total_paid_amount.text


def names_for_incentive() -> list:
    workbook_auto1 = openpyxl.load_workbook(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto_ver_3.xlsx')
    # workbook_master = openpyxl.load_workbook(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto2.xlsx')
    worksheet_for_getting_names = workbook_auto1["Sheet1"]
    incentive_names_to_enter = []
    column_values = worksheet_for_getting_names.iter_rows(min_col=3, max_col=12, min_row=2, max_row=26)
    for row in column_values:
        row_data = [cell.value for cell in row]
        incentive_names_to_enter += row_data
    incentive_names_to_enter = [i for i in incentive_names_to_enter if i is not None]
    print(incentive_names_to_enter)
    workbook_auto1.close()
    return incentive_names_to_enter


def retrieve_employee_id() -> dict:
    workbook_master = openpyxl.load_workbook(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto2.xlsx')
    worksheet_for_getting_id = workbook_master["Sheet3"]
    column_names_in_sheet3 = worksheet_for_getting_id.iter_rows(min_col=2, max_col=2)
    dict_name_row_number = {}
    for namez in column_names_in_sheet3:
        # print(namez[0].value)
        name_is = namez[0].value
        row_number = namez[0].row
        # print({name_is:row_number})
        dict_name_row_number[name_is] = row_number  # gives the row containing name
    # print(dict_name_row_number)
    workbook_master.close()
    return dict_name_row_number


def sqlite_process() -> list[tuple]:
    conn = sqlite3.connect(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\incentiveDatabase.db')
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute("""
        SELECT employee_name, COUNT(incentive_amount) AS total_count, SUM(incentive_amount) AS total_incentive
        FROM incentive_entry_T
        GROUP BY employee_name
    """)

    # Fetch the result
    results = cursor.fetchall()  # [(n1,c1,a1),(n2,c2,a2)..]

    # Close the cursor and connection
    cursor.close()
    conn.close()
    # print(results)
    return results

def sqlite_process_2() -> list[tuple]:
    conn = sqlite3.connect(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\incentiveDatabase_2.db')
    cursor = conn.cursor()
    # Execute the SQL query
    cursor.execute("""
        SELECT e.name_emp, COUNT(d.d_inc_amt) AS total_incentive_count, SUM(d.d_inc_amt) AS total_incentive
        FROM emp_detail_t e
        JOIN distribution_t d ON e.SN = d.d_emp_code
        GROUP BY e.SN  
    """)
    # Fetch the result
    results = cursor.fetchall()  # [(n1,c1,a1),(n2,c2,a2)..]
    # Close the cursor and connection
    cursor.close()
    conn.close()
    # print(results)
    return results

def updating_amount():
    incentive_names_to_enter = names_for_incentive()  # function ran
    dict_name_row_number = retrieve_employee_id()  # function ran
    results = sqlite_process()
    results2 = sqlite_process_2()  # function ran
    workbook_master = openpyxl.load_workbook(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto2.xlsx')
    worksheet_for_getting_id = workbook_master["Sheet3"]
    driver.get('https://dkbssy.cg.nic.in/secure/incentivemodule/IncentiveDetails_EmpCodeWiseDME.aspx')
    for name in incentive_names_to_enter:
        name = name.strip()
        # print(dict_name_row_number.keys())
        if name in dict_name_row_number.keys():
            # count_names_for_check.append(dict_name_row_number[name])
            chosen_row_number = dict_name_row_number[name]
            # print(chosen_row_number)
            chosen_emp_code = worksheet_for_getting_id.cell(row=chosen_row_number, column=3).value
            # print(chosen_emp_code)
            old_pendng_cases = worksheet_for_getting_id.cell(row=chosen_row_number, column=9).value
            chosen_amount = worksheet_for_getting_id.cell(row=chosen_row_number, column=10).value
            print()
            print(name, chosen_emp_code, old_pendng_cases, chosen_amount)

            '''Function run for getting details of all amount'''
            e_code, pend_cases, pend_amount, total_cases, total_amount = emp_code(chosen_emp_code)  # function ran
            worksheet_for_getting_id.cell(row=chosen_row_number, column=8).value = e_code
            worksheet_for_getting_id.cell(row=chosen_row_number, column=9).value = int(pend_cases)
            # worksheet_for_getting_id.cell(row=chosen_row_number, column=9).fill = fill_pattern_yellow
            worksheet_for_getting_id.cell(row=chosen_row_number, column=10).value = int(pend_amount)
            # worksheet_for_getting_id.cell(row=chosen_row_number, column=10).fill = fill_pattern_blue
            worksheet_for_getting_id.cell(row=chosen_row_number, column=11).value = int(total_cases)
            worksheet_for_getting_id.cell(row=chosen_row_number, column=12).value = int(total_amount)
        else:
            print(name)
            sys.exit(f"THERE OCCURRED AN ERROR, Check {name}in incentive auto 2")
    print('Excel Done')

    # update the databases


    for employee_name, total_count_till_now, total_incentive_till_now in results:
        # if employee_name == "CHANDRAKANTA  SHRIVASTAV":
        #     employee_name = "CHANDRAKANTA SHRIVASTAV"

        chosen_row_number = dict_name_row_number[employee_name]
        worksheet_for_getting_id.cell(row=chosen_row_number, column=13).value = int(total_count_till_now)
        worksheet_for_getting_id.cell(row=chosen_row_number, column=14).value = float(total_incentive_till_now)
        # print(employee_name, total_count_till_now, total_incentive_till_now)
    print('Database Done')

    for employee_name, total_count_till_now, total_incentive_till_now in results2:
        chosen_row_number = dict_name_row_number[employee_name]
        worksheet_for_getting_id.cell(row=chosen_row_number, column=15).value = int(total_count_till_now)
        worksheet_for_getting_id.cell(row=chosen_row_number, column=16).value = float(total_incentive_till_now)

    print('Database Done2')
    workbook_master.save(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto2.xlsx')
    workbook_master.close()
    print('All Saved')
