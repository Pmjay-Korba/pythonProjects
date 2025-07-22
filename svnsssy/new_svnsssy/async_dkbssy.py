import asyncio
import datetime
import json
import time
from playwright.async_api import async_playwright, Page, TimeoutError,Keyboard
from dkbssy.utils.excel_utils import ExcelMethods

async def launch_first_page(page):


    await page.goto('https://dkbssy.cg.nic.in/secure/login.aspx')
    username_xpath = '//*[@id="username"]'
    password_xpath = '//*[@id="password"]'
    captcha_xpath = '//*[@id="txtCaptcha"]'
    login_button_xpath = '//*[@id="loginbutton"]'

    username_key = "HOSP22G146659"
    pass_key = "Pmjaykorba@1"


    await page.locator(username_xpath).fill(username_key)
    await page.locator(password_xpath).fill(pass_key)
    await page.locator(captcha_xpath).click()
    await page.wait_for_timeout(10000)
    await page.locator(login_button_xpath).click()

async def select_department(department_choice, page:Page):
    speciality_DD_xpath = '//*[@id="ctl00_ContentPlaceHolder1_speciality"]'
    await page.select_option(speciality_DD_xpath, department_choice)



async def date_entry(page:Page, date_xp, date)-> None:
    dd, mm, yyyy = date.split('-')

    await page.locator(date_xp).fill(dd)
    await page.keyboard.press(key="ARROW_RIGHT")
    await page.locator(date_xp).fill(mm)
    await page.keyboard.press(key="ARROW_RIGHT")
    await page.locator(date_xp).fill(yyyy)




async def incentive_page(page:Page):
    await page.goto('https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduledme.aspx')
    depart_choice = ExcelMethods().entry_department()
    await select_department(department_choice=depart_choice, page=page)
    from_date_xp = '//*[@id="ctl00_ContentPlaceHolder1_fdate"]'
    to_date_xp = '//*[@id="ctl00_ContentPlaceHolder1_tdate"]'

    await date_entry(page,from_date_xp, date = '2022-08-01')
    await date_entry(page,to_date_xp, date = '2023-12-31')





async def main():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False , args=['--start-maximized'])
    context = await browser.new_context(no_viewport=True)
    page = await context.new_page()
    page.set_default_timeout(5000)
    #
    await launch_first_page(page=page)
    await incentive_page(page)






    await page.wait_for_timeout(10000)
    await p.stop()



# asyncio.run(main())