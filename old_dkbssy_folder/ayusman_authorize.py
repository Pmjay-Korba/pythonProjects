import os
import time

import pandas as pd
from selenium import webdriver
from selenium.common import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver: WebDriver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
def login_authorise ():
    driver.get('https://dkbssy.cg.nic.in/secure/login.aspx')
    driver.maximize_window()
    driver.find_element(By.NAME, "username").send_keys("HS220050491")
    driver.find_element(By.NAME, "password").send_keys("dhkorba")
    driver.find_element(By.ID, 'txtCaptcha').click()
    time.sleep(7)  ### SLEEP GIVEN FOR CAPTCHA ENTRY
    sign_in = driver.find_element(By.NAME, "loginbutton")
    sign_in.click()
    # input()
    new_url = 'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleAp.aspx'

    driver.execute_script(f'window.location.href = "{new_url}"')


def authorise_proper():

    first_case_number = driver.find_element(By.PARTIAL_LINK_TEXT, 'CASE')
    first_case_number_text =first_case_number.text

    first_case_amount = driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[2]/td[3]')
    first_case_amount_text = first_case_amount.text

    ('incentivemoduleApView.aspx?ci=CASE/PS5/HS22005049/CK5133732&amt=5610'
     'GMC:- https://dkbssy.cg.nic.in/secure/incentivemodule/incentivedetailsdme.aspx?c=CASE/PS5/HOSP22G146659/CK5222125&amt=2040')
    new_new_url = 'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApView.aspx?ci='+f'{first_case_number_text}&amt={first_case_amount_text}'
    driver.execute_script(f'window.location.href = "{new_new_url}"')

    # submit = driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_Button1"]')
    #
    # submit.click()

    # get text of a element in pop window
    approve_query_option = driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$StatusTxt')
    approve_query_select = Select(approve_query_option)
    approve_query_select.select_by_visible_text('Approve')

    try:
        submit = driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$Button1')
        submit.click()
    except (StaleElementReferenceException, ElementClickInterceptedException) as e:
        for i in range(59):
            try:
                submit = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$Button1')
                submit.click()
                print('Clicked on', i, 'attempt(s)')
                break
            except:
                print('StaleElement')



    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_showotp"]')))
    otp_text = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_showotp"]').text

    # otp enter
    driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$otpTxt').send_keys(otp_text)

    # otp_submit = driver.find_element(By.NAME,'ctl00$ContentPlaceHolder1$otpTxt')
    'CASE/PS5/HS22005049/CK5133732'

    driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$statusSubmit').click() #otp_submit =

    # time.sleep(1)
    wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div[3]/div/button')))

    new_url = 'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleAp.aspx'

    driver.execute_script(f'window.location.href = "{new_url}"')


login_authorise()
for i in range(10):
    authorise_proper()
    print(i)