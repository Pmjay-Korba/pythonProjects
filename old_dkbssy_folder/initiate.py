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


def upload_files(location_0, starts_with):
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


def initiate(case_number):
    driver.switch_to.default_content()
    find_and_click_xpath('//div[@id="sidebar-menu"]//span[normalize-space()="Claims"]')
    find_and_click_xpath('//div[@id="sidebar-menu"]//span[normalize-space()="Claim Initiation"]')
    driver.switch_to.frame("middleFrame")
    find_only_elem_xpath('//input[@id="caseNum" and @onchange]').send_keys(case_number)
    find_and_click_xpath('/html/body/div[2]/form/div[1]/div/div[2]/div[3]/button[1]')
    find_and_click_xpath('/html/body/div[2]/form/div[3]/section/table/tbody/tr/td[2]/a')

    time.sleep(3)
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



    # # click questionaire, verify - questionaire active
    # click_and_check('//*[@id="Questionaire"]',
    #                 '//*[@id="Questionaire" and @class="active"]')
    # driver.switch_to.frame('bottomFrame')
    # # clicking Yes radio 1
    # find_and_click_xpath('(//span[@class="checkmark"])[1]')
    # # Clicking Yes radio 2
    # find_and_click_xpath('(//span[@class="checkmark"])[3]')
    # # click submit button
    # find_and_click_xpath("//button[@id='btnSubmit']")
    # print("Question Submit")
    # driver.switch_to.default_content()
    # driver.switch_to.frame("middleFrame")
    # # claim tab
    # click_and_check('//a[@class="tabs" and normalize-space()="Claims"]',
    #                 '//*[@id="claims" and @class="active"]')
    # print("Claim tab")
    # driver.switch_to.frame('bottomFrame')
    # # claim check box
    # find_and_click_xpath("//div[@id='collaspeClaimInitDtls']//input[@id='claimDisClaimer']")
    # # select drop down box
    # action_type = find_only_elem_xpath("//select[@id='actionType']")
    # selection_action_type = Select(action_type)
    # # waiting for dropdown to load
    # find_only_elem_xpath('//select[@id="actionType"]/option[@value="20"]')
    # selection_action_type.select_by_value("20")
    # # claim submission check box
    # find_and_click_xpath("//div[@class='row']//input[@id='claimDisClaimer']")
    # # click submit button
    # claim_submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button["
    #                                                                                             "@id='submitclaim']")))
    # print(claim_submit_button.text)
    # claim_submit_button.click()
    # # waiting for pop up
    # try:
    #     find_only_elem_xpath('//div[normalize-space()="Do you want to Initiate?"]/ancestor::div['
    #                          '@class="modal-content"]//button[normalize-space()="OK"]')
    # except TimeoutException:
    #     print('SECOND CLICK')
    #     claim_submit_button.click()
    # # modal_click_and_check_inc_timeout("//button[@id='submitclaim']", '//div[normalize-space()="Do you want to
    # # Initiate?"]/ancestor::div[@class="modal-content"]//button[normalize-space()="OK"]') CONFIRM claim initiation
    # # modal pop up
    # # time.sleep(.5)
    # modal_click_and_check('//div[normalize-space()="Do you want to Initiate?"]/ancestor::div['
    #                       '@class="modal-content"]//button[normalize-space()="OK"]')


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




def details_entry():
    while True:
        case_number = input("\033[93mEnter Case number: \033[0m").strip()
        discharge_date = input("\033[93mEnter Discharge date: \033[0m").strip()
        location = input(f"\033[93mEnter Address: \033[0m")
        user_input = input(f'\033[94mPress Enter to continue OR 1 to re-enter: \033[0m')
        if user_input != '1':
            return case_number, discharge_date, location


driver = create_driver()
wait = WebDriverWait(driver, 3)
sign_in()
initiate('CASE/PS7/HOSP22G146659/CK8129948')
