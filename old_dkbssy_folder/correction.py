import datetime
import os, time, openpyxl, pandas as pd
import sys
import sqlite3
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

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


def correction_cycle(case_number, amount):
    driver.get(f"https://dkbssy.cg.nic.in/secure/incentivemodule/incentivedetailsdme.aspx?c={case_number}&amt={amount}")
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
    wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_empCategory"]/option[10]')))
    cat_locator = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$empCategory')
    cat_select = Select(cat_locator)
    cat_select.select_by_value("1")

    wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_empName"]/option[7]')))
    name_wait_elem = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_empName')))
    name_selection = Select(name_wait_elem)
    name_selection.select_by_visible_text('AVINASH MESHRAM')
    add_staff = wait.until(EC.element_to_be_clickable((By.NAME, 'ctl00$ContentPlaceHolder1$Button1')))
    add_staff.click()
    submit = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolder1$button_submit')))
    submit.click()
    time.sleep(0.25)
    alert = driver.switch_to.alert

    alert.accept()


cn_and_amount_list = '''CASE/PS6/HOSP22G146659/S6253749	9299
CASE/PS6/HOSP22G146659/S6264581	5610
CASE/PS6/HOSP22G146659/S6269237	5610
CASE/PS6/HOSP22G146659/S6280576	5610
CASE/PS6/HOSP22G146659/S6317275	2805
CASE/PS6/HOSP22G146659/S6331848	11220
CASE/PS6/HOSP22G146659/S6562885	6358'''.split('\n')

login()
for i in cn_and_amount_list:
    cn, amt = i.split('\t')[0], i.split('\t')[1]
    print(cn, amt)
    correction_cycle(cn,amt)
