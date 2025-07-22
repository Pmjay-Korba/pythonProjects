import time

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Page:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def find_wait_by(self, xpath):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))


class FirstPage (Page):
    url = 'https://dkbssy.cg.nic.in/secure/login.aspx'
    username_xpath = '//*[@id="username"]'
    password_xpath = '//*[@id="password"]'
    captcha_xpath = '//*[@id="txtCaptcha"]'
    login_button_xpath = '//*[@id="loginbutton"]'

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def sign_in(self, username_key, pass_key):
        self.driver.get(self.url)
        self.find_wait_by(self.username_xpath).send_keys(username_key)
        self.find_wait_by(self.password_xpath).send_keys(pass_key)
        self.find_wait_by(self.captcha_xpath).click()
        time.sleep(7)
        self.find_wait_by(self.login_button_xpath).click()


def check_chrome_and_tab(target_title):
    try:
        tabs = requests.get("http://localhost:9223/json", timeout=2).json()
        found = any(target_title.lower() in tab.get("title", "").lower() for tab in tabs)
        if found:
            return True
        else:
            print("✅ EDGE browser is running but target tab is NOT open.")
            return False
    except requests.exceptions.RequestException:
        print( "❌ EDGE browser with remote debugging is NOT running.")
        return False
