'''Claim Query list generate'''

import math
import os
import time
import openpyxl
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

driver.get('https://tms.pmjay.gov.in/OneTMS/loginAction.do')
driver.maximize_window()
driver.find_element(By.NAME, "username").send_keys("CHH009264")
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

# choice = int(input('''PRESS 1 FOR CLAIM QUERY LIST GET,
# PRESS 2 FOR PREAUTH QUERY LIST GET,
# PRESS 3 FOR DISCHARGE LIST GET '''))

#Claim Query
driver.find_element(By.XPATH,'//*[@id="sidebar-menu"]/div/ul/li[7]/a/span[1]').click()
driver.find_element(By.XPATH,'//*[@id="childmenu6"]/li[2]/a/span[1]').click()

#Preauth query
# driver.find_element(By.XPATH,'//*[@id="sidebar-menu"]/div/ul/li[3]/a/span[1]').click()
# driver.find_element(By.XPATH,'//*[@id="childmenu2"]/li[3]/a/span[1]').click()

total_pending = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="javascript:fn_pendingCases();"]/span'))).text
pages_count = math.ceil(int(total_pending)/10)
print(total_pending,pages_count)

driver.switch_to.frame("middleFrame")
# wait.until(EC.presence_of_element_located((By.XPATH,f'//*[@id="no-more-tables"]/table/tbody/tr[{1}]/td[2]/a')))
# a= driver.find_element(By.XPATH,'//*[@id="no-more-tables"]/table/tbody/tr[1]/td[2]/a')
# print(a)
# a.click()

count = 1
for i in range(1,pages_count+1):
    for numx in range(1,11):
        # print('count', count,numx)
        if count <= int(total_pending):
            id = wait.until(EC.presence_of_element_located((By.XPATH,f'//*[@id="no-more-tables"]/table/tbody/tr[{numx}]/td[2]/a')))
            print(id.text)
            # id.click()
            # age = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse1"]/div/div/div[1]/div[5]/div[1]')))
            # print(age.text)
            count+=1
        else:
            break
    if i < pages_count:
        driver.find_element(By.XPATH,f'//*[@id="pageNoDisplay"]/a[{i}]/b').click()
        

'''Claim Query list generate'''