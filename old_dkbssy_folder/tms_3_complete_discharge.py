# discharge 3
import datetime
import os
import random
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver_creating: WebDriver = webdriver.Chrome(options=options)
    # wait = WebDriverWait(driver, 20) # created below
    return driver_creating


def colour_print(colour_code, message):
    print(f'\033[{colour_code}m{message}\033[0m')


def find_only_elem_xpath(xpath):
    try:
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException as exe:
        # print(f'\033[95mERROR MESSAGE in find_only_elem_xpath:- *{exe.msg}*\033[0m, XPATH- {xpath}')
        colour_print(95, f'ERROR MESSAGE in find_only_elem_xpath:- *{exe.msg}*, XPATH- {xpath}')
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))  # second time find element


def find_and_click_xpath(xpath):
    try:
        return wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    except (TimeoutException, ElementClickInterceptedException) as exe:
        # JS click
        # print(f'\033[95mERROR MESSAGE in find_and_click_xpath:- *{exe.msg}*\033[0m, XPATH- {xpath}')
        colour_print(95, f'ERROR MESSAGE in find_and_click_xpath:- *{exe.msg}*, XPATH- {xpath}')
        button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", button)


def click_and_check_selen(click_xpath, verify_xpath, identify_button=None):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, click_xpath)))
    button_name = button.text
    if button_name == "":
        button_name = identify_button
    button.click()
    print("Selen Click:-", button_name)
    # checking for the next item to appear
    check = wait.until(EC.visibility_of_element_located((By.XPATH, verify_xpath)))
    check_name = check.text
    print("Selen Verified-Text:-", check_name)
    print(">>>>", "Selen Click:-", button_name, "&&", "Selen Verified-Text:-", check_name)
    return


def click_and_check_js(click_xpath, verify_xpath, identify_button=None):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, click_xpath)))
    button_name = button.text
    if button_name == "":
        button_name = identify_button
    driver.execute_script("arguments[0].click();", button)
    print("JS Click:-", button_name)
    check = wait.until(EC.visibility_of_element_located((By.XPATH, verify_xpath)))
    check_name = check.text
    print("JS Verified-Text:-", check_name)
    print(">>##", "JS Click:-", button.text, "&&", "JS Verified-Text:-", check_name)
    return


def click_and_check(click_xpath, verify_xpath, identify_button=None):
    try:
        click_and_check_selen(click_xpath, verify_xpath, identify_button=None)
    except (TimeoutException, ElementClickInterceptedException) as exe:
        # print(f'\033[95mERROR MESSAGE in click_and_check :- *{exe.msg}*\033[0m,  {click_xpath}')
        colour_print(95, f'ERROR MESSAGE in click_and_check :- *{exe.msg}*, XPATH-{click_xpath}')
        click_and_check_js(click_xpath, verify_xpath, identify_button=None)


def modal_click_and_check_selen(click_xpath, verify_xpath=None):
    if verify_xpath is None:
        verify_xpath = click_xpath
    button = wait.until(EC.element_to_be_clickable((By.XPATH, click_xpath)))
    button_name = button.text
    button.click()
    print("--Modal Selen Click:-", button_name, "button")
    # checking for item to disappear
    check = wait.until_not(EC.visibility_of_element_located((By.XPATH, verify_xpath)))
    print("--Until Selen not:-", check)
    print(f"--Modal Selen Verified-Text:-{button_name} disappeared")
    return


def modal_click_and_check_js(click_xpath, verify_xpath=None):
    if verify_xpath is None:
        verify_xpath = click_xpath
    button = wait.until(EC.element_to_be_clickable((By.XPATH, click_xpath)))
    button_name = button.text
    driver.execute_script("arguments[0].click();", button)
    print("==Modal JS Click:- ", button_name, "button")
    check = wait.until_not(EC.visibility_of_element_located((By.XPATH, verify_xpath)))
    print("==Until JS not:-", check)
    print(f"==Modal JS Verified-Text:- {button_name} disappeared")
    return


def modal_click_and_check(click_xpath, verify_xpath=None):
    try:
        modal_click_and_check_js(click_xpath, verify_xpath=None)
    except (TimeoutException, ElementClickInterceptedException) as exe:
        # print(f'\033[95mERROR MESSAGE in modal_click_and_check:- *{exe.msg}*\033[0m, XPATH- {click_xpath}')
        colour_print(95, f'ERROR MESSAGE in modal_click_and_check:- *{exe.msg}*, XPATH- {click_xpath}')
        modal_click_and_check_selen(click_xpath, verify_xpath=None)


def date_insert(date, follow_up_days=0) -> str:
    if "/" in date:
        str_day, str_mon, str_year = date.split("/")
    if "-" in date:
        str_day, str_mon, str_year = date.split("-")
    if len(str_day) != 2:
        str_day = "0" + str_day
    if len(str_mon) != 2:
        str_mon = '0' + str_mon
    if len(str_year) != 4:
        str_year = '20' + str_year
    dat_tim_obj = datetime.date(day=int(str_day), month=int(str_mon), year=int(str_year))
    follow_up_days = datetime.timedelta(follow_up_days)
    dat_tim_obj += follow_up_days
    return datetime.date.strftime(dat_tim_obj, "%d-%m-%Y")


def upload_files_2(location_0, starts_with):
    # print('l0', location_0)
    extensions = ['jpg', 'jpeg', 'pdf']
    full_path = location_0.strip('"')
    # print('full',full_path)
    folder_path = os.path.dirname(full_path)
    # print('fol', folder_path)
    for filename in os.listdir(folder_path):
        # print(filename)
        if filename.startswith(starts_with) and any(filename.endswith(ext) for ext in extensions):
            # print('2', filename)
            file_to_upload = os.path.join(folder_path, filename)
            # print(f"File to upload found: {file_to_upload}")
            return file_to_upload


def upload_files(location_0, starts_with):
    starts_with = starts_with.lower()
    extensions = ['jpg', 'jpeg', 'pdf']
    full_path = location_0.strip('"')
    directory = os.path.dirname(full_path)

    matched_files = []
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().startswith(starts_with):
                # Check if the name (excluding extension) is alphabetic and allowed extension
                if filename.split('.')[0].isalnum() and filename.split('.')[1] in extensions:
                    matched_files.append(os.path.join(root, filename))
    # print(matched_files)
    if matched_files:
        return matched_files[0]


def radio_and_checkbox_click(xpath):
    is_checked = find_only_elem_xpath(xpath).is_selected()
    print("is_cheked_or_not", is_checked)
    find_and_click_xpath(xpath)  # click xpath
    # checking clicked or not
    time.sleep(0.5)
    is_checked = find_only_elem_xpath(xpath).is_selected()
    print('is_checked', is_checked)
    if not is_checked:
        find_and_click_xpath(xpath)
        print('is_checked_again')


def initiate():
    driver.switch_to.default_content()
    driver.switch_to.frame("middleFrame")
    # click questionaire, verify - questionaire active
    click_and_check('//*[@id="Questionaire"]',
                    '//*[@id="Questionaire" and @class="active"]')
    driver.switch_to.frame('bottomFrame')
    # clicking Yes radio 1
    radio_and_checkbox_click('(//span[@class="checkmark"])[1]')
    # Clicking Yes radio 2
    radio_and_checkbox_click('(//span[@class="checkmark"])[3]')
    # click submit button
    click_and_check("//button[@id='btnSubmit']",
                    '//div[normalize-space()="Submitted successfully"]/ancestor::div[@class="modal-content"]//button[normalize-space()="OK"]')

    print("Question Submit")
    driver.switch_to.default_content()
    driver.switch_to.frame("middleFrame")
    # claim tab
    click_and_check('//a[@class="tabs" and normalize-space()="Claims"]',
                    '//*[@id="claims" and @class="active"]')
    print("Claim tab")
    driver.switch_to.frame('bottomFrame')
    # claim check box
    radio_and_checkbox_click("//div[@id='collaspeClaimInitDtls']//input[@id='claimDisClaimer']")
    # select drop down box
    action_type = find_only_elem_xpath("//select[@id='actionType']")
    selection_action_type = Select(action_type)
    # waiting for dropdown to load
    find_only_elem_xpath('//select[@id="actionType"]/option[@value="20"]')
    selection_action_type.select_by_value("20")
    # claim submission check box
    radio_and_checkbox_click("//div[@class='row']//input[@id='claimDisClaimer']")
    # click submit button
    claim_submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button["
                                                                                                "@id='submitclaim']")))
    print(claim_submit_button.text)
    claim_submit_button.click()
    # waiting for pop up
    '''IS BUTTON ENABLED CAN BE EMPLOYED'''
    try:
        find_only_elem_xpath('//div[normalize-space()="Do you want to Initiate?"]/ancestor::div['
                             '@class="modal-content"]//button[normalize-space()="OK"]')
    except TimeoutException:
        print('SECOND CLICK')
        claim_submit_button.click()
    # modal_click_and_check_inc_timeout("//button[@id='submitclaim']", '//div[normalize-space()="Do you want to
    # Initiate?"]/ancestor::div[@class="modal-content"]//button[normalize-space()="OK"]') CONFIRM claim initiation
    # modal pop up
    # time.sleep(.5)
    modal_click_and_check('//div[normalize-space()="Do you want to Initiate?"]/ancestor::div['
                          '@class="modal-content"]//button[normalize-space()="OK"]')


def sign_in():
    driver.get('https://tms.pmjay.gov.in/OneTMS/loginAction.do')
    driver.maximize_window()
    find_only_elem_xpath('//*[@id="username"]').send_keys("CHH009264")
    click_and_check('//*[@id="proceed"]', '//div[contains(text(),"User-id and Password")]')
    # modal click ok wait to clear
    modal_click_and_check('//div[contains(text(),"User-id and Password")]/ancestor::div['
                          '@class="modal-content"]//button[contains(text(),"OK")]')
    find_only_elem_xpath('//*[@id="password"]').send_keys("Gmc@12345")
    # clicking to get cursor in captcha input
    find_and_click_xpath('//*[@id="reqCaptcha"]')
    # sleep for captcha entry
    time.sleep(10)
    # click checkbox, verify - enabled submit button
    click_and_check('//*[@id="checkSubmit"]', '//*[@id="login-submit" and not(@disabled)]',
                    identify_button="Submit-Checkbox")
    # click submit, verify - dashboard
    click_and_check('//*[@id="login-submit"]', '//span[contains(text(),"Dashboard")]')
    # click pre-auth, verify - Discharge
    click_and_check('//a[normalize-space()="Preauthorization"]',
                    '//span[normalize-space()="Cases for Surgery/Discharge"]')
    # click Discharge, verify - Discharge again because of change in frame
    click_and_check('//span[normalize-space()="Cases for Surgery/Discharge"]',
                    '//span[normalize-space()="Cases for Surgery/Discharge"]')


def discharge_cycle(case_number, discharge_date, location):
    # click Discharge, verify - Discharge again because of change in frame
    click_and_check('//span[normalize-space()="Cases for Surgery/Discharge"]',
                    '//span[normalize-space()="Cases for Surgery/Discharge"]')
    driver.switch_to.frame("middleFrame")
    find_only_elem_xpath('//*[@id="caseNum"]').send_keys(case_number)
    # click search, verify - result
    click_and_check('//*[@id="preauthForApproval"]/div[3]/button[1]',
                    '//*[@id="no-more-tables"]/table/tbody/tr/td[2]/b/u/a')
    # click result, verify - ip date
    click_and_check('//*[@id="no-more-tables"]/table/tbody/tr/td[2]/b/u/a',
                    '//*[@id="collapse1"]/div/div/div[1]/div[2]/div[3]')
    # getting date
    ip_date = find_only_elem_xpath('//*[@id="collapse1"]/div/div/div[1]/div[2]/div[3]').text.split("\n")[1]
    # print(ip_date)
    driver.switch_to.frame('bottomFrame')

    # find the doctor type
    doctor_type_select_web = find_only_elem_xpath('//*[@id="surDocType"]')
    # waiting for drop down to load
    find_only_elem_xpath('//option[@value="DD"]')
    doctor_type_selection_list = Select(doctor_type_select_web)
    doctor_type_selection_list.select_by_value('O')
    # doctor selection
    doctor_name = random.choice(
        ["DR ADITI SINGH PARIHAR (CGMC10585/2020)", "dr a sisodiya (3775)", "DR. BHARTI PATEL (CGMC 9308/2019)",
         "DR JYOTI SAHU (CGMC12299)", "dr m kujur (3077)", "DR NIKITA SHRIVASTAVA (1349734)"])
    # waiting for names to load
    find_only_elem_xpath('//option[@value="DR. BHARTI PATEL"]')
    doctor_selection_web = find_only_elem_xpath('//*[@id="surgeonName"]')
    # print(doctor_selection_web.text)
    doctor_select = Select(doctor_selection_web)
    doctor_select.select_by_visible_text(doctor_name)

    # admission date entry process
    date_input = find_only_elem_xpath('//*[@id="surgStartDt"]')
    desired_date = date_insert(ip_date)
    script = f"arguments[0].value = '{desired_date}'; arguments[0].dispatchEvent(new Event('change'));"
    driver.execute_script(script, date_input)
    print('Admission Date Entered')
    # discharge radio enabled?
    is_discharge_enable = find_only_elem_xpath('//*[@id="discharge"]').is_enabled()
    # click discharge radio, verify - discharge date
    if is_discharge_enable:
        click_and_check('//*[@id="discharge"]', '//b[text()="Discharge Date"]',
                        identify_button="Discharge-radio")
    # discharge date entry
    discharge_date_input = find_only_elem_xpath('//*[@id="disDate"]')
    # discharge_date = date_insert('26-05-2024')
    discharge_date = date_insert(discharge_date)
    # discharge_time generate
    dis_hour = random.choice(['13', '14', '15', '16', '17', '18'])
    dis_minute = random.choice(['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'])
    discharge_date_and_time = discharge_date + " " + dis_hour + ":" + dis_minute
    print(f"Discharge date and time", discharge_date_and_time)
    script = f"arguments[0].value = '{discharge_date_and_time}'; arguments[0].dispatchEvent(new Event('change'));"
    driver.execute_script(script, discharge_date_input)
    # next follow-up date flag
    follow_up_input = find_only_elem_xpath('//*[@id="nxtFollUpDt"]')
    follow_up_date = date_insert(discharge_date, 5)
    script = f"arguments[0].value = '{follow_up_date}'; arguments[0].dispatchEvent(new Event('change'));"
    driver.execute_script(script, follow_up_input)
    # special case flag2
    special = find_only_elem_xpath('//*[@id="specCase"]')
    special_select = Select(special)
    # waiting for loading dropdown
    find_only_elem_xpath('//select[@name="specCase"]/option[@value="NO"]')
    special_select.select_by_value("NO")
    # procedure consent radio flag
    radio_and_checkbox_click('//*[@id="procedureConsentYes"]')
    # Disclaimer flag
    radio_and_checkbox_click('//*[@id="disDisClaimer"]')
    # click save_date, verify modal pop up
    click_and_check('//button[@id="dateUpdate"]',
                    '//div[normalize-space()="Do you want to save Treatment start/ Surgery dates?"]')
    # modal save pop up ok clicked
    modal_click_and_check('//div[@class="bootbox modal fade bootbox-confirm show"]//button[normalize-space()="OK"]')
    print('Date saved pop up 1')
    # modal saved notification ok click
    try:
        modal_click_and_check_js(
            '//div[@class="bootbox modal fade bootbox-alert show"]//button[normalize-space()="OK"]')
        print('Date saved pop up 2')
    except TimeoutException:
        print('No Save Button')
    # attachment button
    click_and_check('//*[@id="btnattach"]',
                    '//*[@id="titleModal" and text()="Attachments"]')
    files_to_upload_dict = {'PP': ('//td[contains(text(),"After Discharge Photo")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"After Discharge Photo")]/parent::tr//select',
                                   'After Discharge Photo'),  # after disc photo
                            'DD': ('//td[contains(text(),"Discharge summary documents")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"Discharge summary documents")]/parent::tr//select',
                                   'Discharge summary documents'),  # discharge
                            'AA': ('//td[contains(text(),"OperationDocuments")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"OperationDocuments")]/parent::tr//select',
                                   'OperationDocuments'),  # anaesthesia
                            'OO': ('//td[contains(text(),"Operative notes")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"Operative notes")]/parent::tr//select',
                                   'Operative notes'),  # operation notes
                            'BB': ('//td[contains(text(),"new born child")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"new born child")]/parent::tr//select',
                                   'Detailed status of the new born child'),  # baby notes
                            'LL': ('//td[contains(text(),"Labour charting")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"Labour charting")]/parent::tr//select',
                                   'Labour charting (Only in case of Elective Caesarean Delivery)'),  # labour charting
                            }
    driver.switch_to.default_content()
    driver.switch_to.frame("middleFrame")
    driver.switch_to.frame('bottomFrame')
    driver.switch_to.frame('modalattDivIframe')

    table_attach = find_only_elem_xpath('//div[@id="discharge"]')
    t_body = table_attach.find_elements(By.TAG_NAME, "tbody")
    print('t_body len=', len(t_body), t_body)
    t_body_list = []
    for t_b in t_body:
        t_body_list.append(t_b.text)
    print(t_body_list)
    # attachment_list = ['After Discharge Photo',
    #                    'Discharge summary documents',
    #                    'OperationDocuments',
    #                    'Patient satisfaction letter',
    #                    'Video Recordings',
    #                    'Webex Recordings',
    #                    'Operative notes',
    #                    'Detailed status of the new born child',
    #                    'Labour charting (Only in case of Elective Caesarean Delivery)']

    for k, v in files_to_upload_dict.items():
        count_list = []
        for i in t_body_list:
            n = (i.count(v[2]))
            count_list.append(n)
        print(count_list)
        # print(sum(count_list))
        if sum(count_list) == 1:
            max_retries = 1
            retries = 0
            is_done_correct = False
            while not is_done_correct and retries < max_retries:
                try:
                    driver.switch_to.default_content()
                    driver.switch_to.frame("middleFrame")
                    driver.switch_to.frame('bottomFrame')
                    driver.switch_to.frame('modalattDivIframe')
                    # upload button and files uploaded
                    print('to upload', upload_files(location, k))
                    find_only_elem_xpath(v[0]).send_keys(upload_files(location, k))
                    # get modal text
                    # time.sleep(0.5)
                    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(),"pload")]')))
                    modal_dialog_text = find_only_elem_xpath('//div[contains(text(),"pload")]').text
                    # '//button[normalize-space()="OK"]/ancestor::div[@class="modal-content"]/descendant::div[@class="bootbox-body"]'
                    print('---------------------------------------------------------------------------')
                    print('Modal_text = ', modal_dialog_text)
                    if 'Duplicate document is being uploaded. Do you want to proceed?' in modal_dialog_text:
                        modal_click_and_check(
                            "//div[div[div[normalize-space()='Duplicate document is being uploaded. Do you want to "
                            "proceed?']]]//button[normalize-space()='OK']")
                        print('Going Dupli')
                        choice = find_only_elem_xpath(v[1])
                        choices_drop = Select(choice)
                        choices_drop.select_by_value("SAME")
                        print('Same selected')
                        find_only_elem_xpath(v[0]).send_keys(upload_files(location, k))
                        modal_click_and_check(
                            '//div[contains(text(),"pload")]/ancestor::div[@class="modal-content"]/descendant::button['
                            'normalize-space()="OK"]')
                        is_done_correct = True
                        print(k, 'Duplicate')
                    elif 'Cannot Upload similar documents' in modal_dialog_text:
                        modal_click_and_check(
                            '//div[contains(text(),"pload")]/ancestor::div[@class="modal-content"]/descendant::button['
                            'normalize-space()="OK"]')
                        is_done_correct = True
                        print(k, 'Cannot upload same')

                    else:
                        modal_click_and_check(
                            '//div[contains(text(),"pload")]/ancestor::div[@class="modal-content"]/descendant::button['
                            'normalize-space()="OK"]')
                        is_done_correct = True
                        print(k, 'Uploaded')
                    print("---------------------------------------------------------------------------")
                except TimeoutException as e:
                    print(k, "Uploaded Previously 2")
                    print(f"Retries - {retries + 1}")
                    retries += 1
                except ElementClickInterceptedException as exe:
                    # print(f'\033[95mERROR MESSAGE Attachment - Click Intercept:- *{exe.msg}*\033[0m')
                    colour_print(92, f'ERROR MESSAGE Attachment - Click Intercept:- *{exe.msg}*')
                    driver.switch_to.default_content()
                    driver.switch_to.frame("middleFrame")
                    driver.switch_to.frame('bottomFrame')
                    # clicking saved pop up if occurs
                    modal_click_and_check_js('//div[@class="bootbox modal fade bootbox-alert show"]'
                                             '//button[normalize-space()="OK"]')
                    print('Date saved pop up 2')
                    driver.switch_to.default_content()
                    driver.switch_to.frame("middleFrame")
                    driver.switch_to.frame('bottomFrame')
                    driver.switch_to.frame('modalattDivIframe')
                    # closing the current popup
                    modal_click_and_check('//div[contains(text(),"pload")]/preceding-sibling::button['
                                          '@class="bootbox-close-button close"]')
    driver.switch_to.default_content()
    driver.switch_to.frame("middleFrame")
    driver.switch_to.frame('bottomFrame')
    # recheck of saved notification pop up
    try:
        modal_click_and_check_js(
            '//div[@class="bootbox modal fade bootbox-alert show"]//button[normalize-space()="OK"]')
        print('Date saved pop up 2')
    except TimeoutException:
        print('No Save Button Again')

    # attachment close button
    find_and_click_xpath("//button[@class='btn btn-default btn-fade']")
    # VERIFY AND SUBMIT
    # click verify and submit button
    find_and_click_xpath("//b[normalize-space()='Verify and Submit']")
    # click radio bio-auth
    try:
        find_and_click_xpath('//input[@value="BIOMETRIC"]')
        print('Fingerprint scan')
        time.sleep(3)
        # check for biometric machine
        try:
            find_only_elem_xpath('//div[div[div[contains(text(), "device is connected to the system")]]]//button['
                                 'contains(text(), "OK")]')
            colour_print(93, "Connect MANTRA Device")
            colour_print(93, 'Press Enter after connecting')
            input()
            modal_click_and_check('//div[div[div[contains(text(), "device is connected to the system")]]]//button['
                                  'contains(text(), "OK")]')
            # click verify and submit button again
            find_and_click_xpath("//b[normalize-space()='Verify and Submit']")
            # click radio bio-auth
            radio_and_checkbox_click('//input[@value="BIOMETRIC"]')
            print('Fingerprint scan')
            time.sleep(1)
        except TimeoutException:
            pass
        try:
            modal_click_and_check('//button[normalize-space()="Retry"]')
            print("Fingerprint scan Retry 2")
            time.sleep(1)
        except:
            pass
        try:
            modal_click_and_check('//button[normalize-space()="Retry"]')
            print("Fingerprint scan Retry 3")
            time.sleep(1)
        except:
            pass

        try:
            modal_click_and_check('//div[normalize-space()="Successfully captured Patient '
                                  'Biometric"]/ancestor::div[@class="modal-content"]//button[normalize-space('
                                  ')="OK"]')
        except:
            pass
        try:
            modal_click_and_check('//div[normalize-space()="Successfully captured Patient '
                                  'Biometric"]/ancestor::div[@class="modal-content"]//button[normalize-space('
                                  ')="OK"]')
        except:
            pass
        try:
            modal_click_and_check('//div[normalize-space()="Successfully captured Patient '
                                  'Biometric"]/ancestor::div[@class="modal-content"]//button[normalize-space('
                                  ')="OK"]')
        except:
            pass
        try:
            time.sleep(1)
            modal_click_and_check('//button[text()="Discharge"]')
        except:
            pass
    except (ElementNotInteractableException, TimeoutException) as exe:
        # print(f'\033[95mERROR MESSAGE in Biometric start:- *{exe.msg}*\033[0m')
        colour_print(93, f'ERROR MESSAGE in Biometric start:- *{exe.msg}*')
    # submit after attachment
    modal_click_and_check('//div[normalize-space()="Do you want to Submit ?"]/ancestor::div['
                          '@class="modal-content"]//button[normalize-space()="OK"]')
    # Do you want to initiate the claim ? pop up
    modal_click_and_check('//div[normalize-space()="Discharge Updated.Do you want to initiate the claim '
                          '?"]/ancestor::div[@class="modal-content"]//button[normalize-space()="Yes"]')
    driver.switch_to.default_content()
    driver.switch_to.frame("middleFrame")
    #  Notification
    modal_click_and_check('//*[@id="notify"]/div/div/div[3]/button[text()="Close"]')
    print("NotifiCASE/PS7/HOSP22G146659/CK8070164cation")
    # initiate
    initiate()
    driver.switch_to.default_content()


driver = create_driver()
wait = WebDriverWait(driver, 3)
sign_in()


def details_entry():
    while True:
        case_number = input("\033[93mEnter Case number: \033[0m").strip()
        discharge_date = input("\033[93mEnter Discharge date: \033[0m").strip()
        location = input(f"\033[93mEnter Address: \033[0m")
        user_input = input(f'\033[94mPress Enter to continue OR 1 to re-enter: \033[0m')
        if user_input != '1':
            return case_number, discharge_date, location


while True:
    case_number, discharge_date, location = details_entry()
    discharge_cycle(case_number, discharge_date, location)
    # discharge_cycle('CASE/PS7/HOSP22G146659/CK8043887', '06-05-24', location)
    'CASE/PS7/HOSP22G146659/CK8043887'
