import asyncio
import sys
import time

import openpyxl
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from dkbssy.dk_pages.dk_login_page import Page
from dkbssy.utils.colour_prints import ColourPrint
from dkbssy.utils.excel_utils import ExcelMethods
from playwright.async_api import async_playwright, Page as Page_play

from svnsssy.new_svnsssy.async_dkbssy import select_department


class SecondPage(Page):
    second_page_url = "https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduledme.aspx"
    speciality_DD_xpath = '//*[@id="ctl00_ContentPlaceHolder1_speciality"]'
    waiting_element_neonatal = '//option[@value="Neonatal care"]'
    from_date_xpath = '//*[@id="ctl00_ContentPlaceHolder1_fdate"]'
    to_date_xpath = '//*[@id="ctl00_ContentPlaceHolder1_tdate"]'
    search_button_xpath = '//*[@id="ctl00_ContentPlaceHolder1_SearchCases"]'
    search_box_xpath = '//input[@type="search"]'
    web_search_case_number_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr/td[2]/a'
    waiting_for_nav_bar_xp = '//*[@id="divsummary"]/ul'

    def select_department_use(self, depart_choice):
        # wait for presence of element of dropdown
        self.driver.get(self.second_page_url)
        self.find_wait_by(self.waiting_for_nav_bar_xp)  # waiting for loading
        self.find_wait_by(self.waiting_element_neonatal)
        # function run
        speciality_dd = self.find_wait_by(self.speciality_DD_xpath)
        speciality_dd_select = Select(speciality_dd)
        speciality_dd_select.select_by_value(depart_choice)

    def date_entry(self, date_xpath, date):
        dd, mm, yyyy = date.split('-')
        date_element = self.find_wait_by(date_xpath)

        'seleium'
        date_element.send_keys(dd)
        # time.sleep(2)
        date_element.send_keys(mm)
        # time.sleep(2)
        date_element.send_keys(Keys.ARROW_RIGHT)
        # time.sleep(2)
        date_element.send_keys(yyyy)

        'Javascript'
        # self.driver.execute_script("arguments[0].value = arguments[1];", date_element, date)

    def from_to_date_entry_use(self, from_date, to_date):
        # from_date_entry
        self.date_entry(self.from_date_xpath, from_date)
        self.date_entry(self.to_date_xpath, to_date)
        # click search button
        self.find_wait_by(self.search_button_xpath).click()




    def web_selection_of_case_use(self, case_number):
        # get search box and send keys
        self.find_wait_by(self.search_box_xpath).send_keys(case_number)
        try:
            web_incentive_case = self.find_wait_by(self.web_search_case_number_xpath)
            web_incentive_case_text = web_incentive_case.text
            ColourPrint.print_green("Web-item case number", web_incentive_case_text)
            if web_incentive_case_text == case_number:
                web_incentive_case.click()
        except TimeoutException:
            sys.exit(f'''ALREADY INCENTIVE ENTRY DONE FOR THE INCENTIVE CASE NUMBER - {case_number}''')

    def reload_page(self):
        return self.driver.get(self.second_page_url)

    async def select_department(self, depart_choice, from_date, to_date):
        play = await async_playwright().start()
        browser = await play.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0]
        await page.goto(self.second_page_url)
        # await page.wait_for_selector(self.waiting_element_neonatal)
        await page.select_option(self.speciality_DD_xpath, depart_choice)
        await page.locator(self.from_date_xpath).fill(from_date)
        await page.locator(self.to_date_xpath).fill(to_date)
        await page.locator(self.search_button_xpath).click()
        await play.stop()

    def async_second_page(self,depart_choice, from_date, to_date):
        asyncio.run(self.select_department(depart_choice, from_date, to_date))


# async def get_multiple_async(number_of_page, case_number_list):
#     play = await async_playwright().start()
#     browser = await play.chromium.connect_over_cdp('http://localhost:9222')
#     context = browser.contexts[0]
#     pages = [context.new_page() for i in number_of_page]