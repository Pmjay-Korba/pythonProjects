import os, time, openpyxl, pandas as pd
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import name_for_date_check

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver: WebDriver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

driver.get('https://tms.pmjay.gov.in/OneTMS/loginAction.do')
driver.maximize_window()
driver.find_element(By.NAME, "username").send_keys("CHH008164")
driver.find_element(By.XPATH,'//*[@id="proceed"]').click()
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[10]/div/div/div[2]/button'))).click()
# driver.find_element(By.XPATH,'/html/body/div[10]/div/div/div[2]/button').click()
driver.find_element(By.NAME, "password").send_keys("Gmc@12345")
driver.find_element(By.ID, 'reqCaptcha').click()
time.sleep(10)  ### SLEEP GIVEN FOR CAPTCHA ENTRY
driver.find_element(By.XPATH,'//*[@id="checkSubmit"]').click()
sign_in = driver.find_element(By.ID, "login-submit")
sign_in.click()


def cycle(case_number):

    pedia_list =[]
    # print(case_number)
    driver.switch_to.frame("middleFrame")
    driver.find_element(By.XPATH,'//*[@id="caseNum"]').send_keys(case_number)

    # casetype = driver.find_element(By.XPATH,'//*[@id="preauthForApproval"]/div[2]/div[2]/label/b')
    driver.find_element(By.XPATH,'//*[@id="preauthForApproval"]/div[2]/div[2]/span/span[1]/span/span[2]/b').click()
    input_box = driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
    input_box.send_keys('All')
    input_box.send_keys(Keys.ENTER)
    driver.find_element(By.XPATH,'//*[@id="preauthForApproval"]/div[6]/button[1]').click()
    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="dataTable"]/tbody/tr/td[2]/a'))).click() # clicking case number
    age = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse1"]/div/div/div[1]/div[5]/div[1]'))).text.split('\n')[1]
    card = driver.find_element(By.XPATH,'/html/body/form[1]/div/div[2]/div/div/div[1]/div[1]/div[2]').text.split('\n')[1]
    status = driver.find_element(By.XPATH, '/html/body/form[1]/div/div[2]/div/div/div[1]/div[2]/div[1]').text.split('\n')[1]
    name = driver.find_element(By.XPATH, '/html/body/form[1]/div/div[2]/div/div/div[1]/div[1]/div[1]').text.split('\n')[1]

    driver.switch_to.frame("bottomFrame")
    icd_diagnosis = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="icdCodesValuesDiv"]/tr[1]/td[3]'))).text
    # print(icd_diagnosis)
    procedure = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form[1]/div[2]/div[1]/div[4]/div[2]/section/table/tbody/tr/td[2]'))).text
    # print(procedure)
    department = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/form[1]/div[2]/div[1]/div[4]/div[2]/section/table/tbody/tr/td[1]'))).text
    amount = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form[1]/div[2]/div[1]/div[4]/div[2]/section/table/tbody/tr/td[4]'))).text
    query = driver.find_element(By.XPATH, '//*[@id="reasonsTableID"]/tbody/tr[1]/td[4]').text

    # print(query)
    # print(department)
    # print(amount)
    # print(department2)

    driver.switch_to.default_content()


    try:
        newborn_baby = driver.find_element(By.XPATH,'//*[@id="collapse1"]/div/div/div[1]/div[4]/div/label/b').text
        age = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse1"]/div/div/div[1]/div[5]/div[1]')))
        # print(age.text)
    except NoSuchElementException:
        newborn_baby = False

    pedia_list.extend([department,card, name, status, case_number, age, newborn_baby, procedure, icd_diagnosis, query, int(amount)])

    print(pedia_list)
    wb = openpyxl.load_workbook(r'H:\My Drive\GdrivePC\Hospital\RSBY\New\pedia_extract.xlsx')
    ws = wb['Sheet1']
    ws.append(pedia_list)
    wb.save(r'H:\My Drive\GdrivePC\Hospital\RSBY\New\pedia_extract.xlsx')

    driver.switch_to.default_content()
    driver.find_element(By.XPATH,'//*[@id="sidebar-menu"]/div/ul/li[5]/a').click()



casear = '''

CASE/PS5/HOSP22G146659/M5575524
CASE/PS5/HOSP22G146659/CK5618212
CASE/PS5/HOSP22G146659/S5670485
CASE/PS5/HOSP22G146659/CK5670244
CASE/PS5/HOSP22G146659/CK5696962
CASE/PS5/HOSP22G146659/CK5698752
CASE/PS5/HOSP22G146659/CK5694999
CASE/PS5/HOSP22G146659/CK5707217


'''.split('\n')

for c in casear:
    if c == "":
        pass
    else:
        t1 = time.time()
        cycle(c)
        t2 = time.time()
        duration = t2 - t1
        print(duration)


