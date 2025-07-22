import os
import time

import pandas as pd
from selenium import webdriver
# from selenium.common import StaleElementReferenceException, ElementClickInterceptedException
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
    driver.find_element(By.NAME, "username").send_keys("HOSP22G146659")
    driver.find_element(By.NAME, "password").send_keys("Pmjaykorba@1")
    driver.find_element(By.ID, 'txtCaptcha').click()
    time.sleep(7)  ### SLEEP GIVEN FOR CAPTCHA ENTRY
    sign_in = driver.find_element(By.NAME, "loginbutton")
    sign_in.click()
    # input()
    new_url = 'https://dkbssy.cg.nic.in/secure/incentivemodule/DMEincentivemodulequery.aspx'

    driver.execute_script(f'window.location.href = "{new_url}"')


def query_del_proper():

    del_case = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[2]/td[6]/a')))
    del_case.click()
    print('Deleted Case')


# def delete_handler(case_number):
#     new_url = f'https://dkbssy.cg.nic.in/secure/incentivemodule/DMEdeleteHandler.ashx?ci={case_number}&amt={aaa}'
#     script = f'window.open("{new_url}", "_blank");'
#     driver.execute_script(script)



login_authorise()
for i in range(670):
    query_del_proper()
    print(i)
    # time.sleep(4)


