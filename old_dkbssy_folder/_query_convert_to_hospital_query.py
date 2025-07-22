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
    driver.find_element(By.NAME, "username").send_keys("HOSP22G1466591")
    driver.find_element(By.NAME, "password").send_keys("Gmc@pmjay1")
    driver.find_element(By.ID, 'txtCaptcha').click()
    time.sleep(10)  ### SLEEP GIVEN FOR CAPTCHA ENTRY
    sign_in = driver.find_element(By.NAME, "loginbutton")
    sign_in.click()
    # input()
    new_url = 'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApDME.aspx'

    driver.execute_script(f'window.location.href = "{new_url}"')


def query_proper(case_number:str):

    '''WHEN OLD STYLE WHEN QUERY IS VISIBLE

    web_location = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_GridView1_filter"]/label/input')))
    web_location.clear()
    web_location.send_keys(case_number)
    # clicable_case_number = driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr/td[3]/a')
    str_amount = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr/td[4]').text
    '''

    '''NEW WHEN QUERY IS NOT VISIBLE => DIRECT METHOD'''
    case_number, str_amount = case_number.split()

    new_link = f'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApViewDME.aspx?ci={case_number}&{str_amount}'
    print(new_link)
    driver.execute_script(f'window.location.href = "{new_link}"')

    # get text of a element in pop window
    approve_query_option = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$StatusTxt')
    approve_query_select = Select(approve_query_option)
    approve_query_select.select_by_visible_text('Query')
    text_area = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_queryText"]'))).send_keys(
        "REINITIATE".upper())
    submit = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$statusSubmit')
    submit.click()
    # waiting for OK dialog
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[3]/div/button"))).click()



login_authorise()
list_query = '''CASE/PS6/HOSP22G146659/CK7373890	2655.4
CASE/PS6/HOSP22G146659/CK7303028	2655.4
CASE/PS6/HOSP22G146659/CK7232381	3927
CASE/PS6/HOSP22G146659/CK7208586	785.4
CASE/PS6/HOSP22G146659/CK7156278	785.4
CASE/PS6/HOSP22G146659/CK7124008	3141.6
CASE/PS6/HOSP22G146659/CK7111315	2655.4
CASE/PS6/HOSP22G146659/CK7052935	785.4
CASE/PS6/HOSP22G146659/CK7050511	1570.8
CASE/PS6/HOSP22G146659/CK7042524	785.4
CASE/PS6/HOSP22G146659/CK6338729	7480
CASE/PS6/HOSP22G146659/CK7282627	28050'''.split("\n")
for cn in list_query:
    query_proper(cn)
    print(cn)