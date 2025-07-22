import asyncio
import math
import time

# user_id = 'CHH009264'
import gspread
import gspread_dataframe
import openpyxl
import pandas as pd
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright, TimeoutError, Page
from dkbssy.utils.colour_prints import ColourPrint
from dkbssy.utils.file_renamer import rename_file
from old_dkbssy_folder import tms_department_wise_2
from tms_playwright.discharge_to_be_done.discharge_details import DischargeGetParameters
from tms_playwright.page_objs_tms import tms_xpaths
from tms_playwright.discharge_to_be_done.detail_list_getter_all import AllListGenerator


class AllListGenerator_2:

    async def modal_ok_box(self,
                           page,
                           partial_body_text,
                           modal_body_xpath=tms_xpaths.modal_body_xpath,
                           modal_ok_xpath=tms_xpaths.modal_ok_xpath):
        modal_body_web = await page.wait_for_selector(modal_body_xpath)
        web_modal_body_text = await modal_body_web.inner_text()
        # print(web_modal_body_text)
        if partial_body_text in web_modal_body_text:
            modal_ok_button = await page.wait_for_selector(modal_ok_xpath)
            # Scroll the element into view
            # page.keyboard.press('PageUp')
            # await page.evaluate("() => { window.scrollTo(0, -5000); }")
            await modal_ok_button.click()
            ColourPrint.print_green(web_modal_body_text, "-> Done Till Here")
        else:
            ColourPrint.print_bg_red(f'No button containing "{partial_body_text}"')
            return None

    async def g_sheet_getter(self, context):
        page_g = await context.new_page()
        await page_g.goto('https://docs.google.com/spreadsheets/d/19HHTQZe9_8hMQJDZM4aZ01RcBqVH1-xXVv3RkR2W1ls/edit#gid=0')

    async def login_main_for_all(self, context, user_id) -> Page:
        page = await context.new_page()
        await page.goto(tms_xpaths.first_page_url_xpath)
        username = await page.wait_for_selector(tms_xpaths.username_xpath)
        await username.fill(user_id)
        # click proceed
        proceed_button = await page.wait_for_selector(tms_xpaths.proceed_button_xpath)
        await proceed_button.click()
        await self.modal_ok_box(page, tms_xpaths.AFTER_PROCEED_MODAL_BODY_TEXT)
        password = await page.wait_for_selector(tms_xpaths.password_xp)
        await password.type(tms_xpaths.password_value)
        captcha = await page.wait_for_selector(tms_xpaths.captcha_xp)
        await captcha.click()
        time.sleep(15)
        login_checkbox_button = await page.wait_for_selector(tms_xpaths.login_checkbox)
        await login_checkbox_button.click()
        login_button = await page.wait_for_selector(tms_xpaths.login_button_xp)
        await login_button.click()
        # waiting for pre-auth and discharge button to load
        await page.wait_for_load_state()
        return page


    async def pending_count_numbers(self, context):
        # pre auth pending count
        page = await self.login_main_for_all(context, 'chh009264')
        pre_auth_query = await page.wait_for_selector(tms_xpaths.pre_auth_query_left_side_tab_xp)
        await pre_auth_query.click()
        total_pre_auth_query_count = await page.wait_for_selector(tms_xpaths.pre_auth_query_count_xp)
        total_pre_auth_query_count = await total_pre_auth_query_count.inner_text()

        # discharge pending count
        total_pending_dis_count = await page.wait_for_selector(tms_xpaths.list_discharge_count_xp)
        total_pending_dis_count = await total_pending_dis_count.inner_text()

        # claim count
        claim_menu = await page.wait_for_selector(tms_xpaths.claim_list_gen_menu_xp)
        await claim_menu.click()
        total_pending_claim_count = await page.wait_for_selector(tms_xpaths.claim_list_pending_count_xp)
        total_pending_claim_count = await total_pending_claim_count.inner_text()

        print('Pre_auth_query', total_pre_auth_query_count,
              '\nClaim count', total_pending_claim_count,
              '\nTotal discharge pending',total_pending_dis_count)

        # LOGGING OUT
        # await page.wait_for_event("close", timeout=0)
        down_logout_arrow = await page.wait_for_selector(tms_xpaths.down_arrow_xp)
        await down_logout_arrow.click()
        logout_button = await page.wait_for_selector(tms_xpaths.logout_button_xp)
        await logout_button.click()
        print('LOGGED OUT')

        # manual closing
        # await page.wait_for_event("close", timeout=0)
        return total_pre_auth_query_count, total_pending_claim_count, total_pending_dis_count



    async def both_query_generator(self, context, user_id, total_pre_auth_query_count):
        print('d1')
        page = await self.login_main_for_all(context, user_id)
        try:  # pre-auth is already opened
            await page.wait_for_selector(tms_xpaths.list_discharge_left_side_tab_ACTIVE_xp, timeout=3000)
            pass
        except TimeoutError:
            pre_auth_query = await page.wait_for_selector(tms_xpaths.pre_auth_query_left_side_tab_xp)
            await pre_auth_query.click()
        pre_auth_query_child_menu = await page.wait_for_selector(tms_xpaths.pre_auth_query_left_side_tab_sub_tab_xp)
        await pre_auth_query_child_menu.click()

        pages_count = math.ceil(int(total_pre_auth_query_count) / 10)
        print(total_pre_auth_query_count, pages_count)

        middle_frame_element = await page.wait_for_selector(tms_xpaths.middle_frame_xp)
        middle_frame_content = await middle_frame_element.content_frame()
        print('d2')

        count_individual_cases = 1
        to_save_list_pre = []
        for sheet in range(1, pages_count + 1):
            for numx in range(1, 11):
                if count_individual_cases <= int(total_pre_auth_query_count):
                    await middle_frame_content.wait_for_selector(tms_xpaths.serial_number_waiting(count_individual_cases))
                    idx = await middle_frame_content.wait_for_selector(tms_xpaths.case_serial_num_xp(numx))
                    idx_text = await idx.inner_text()
                    print(idx_text)
                    count_individual_cases += 1
                    to_save_list_pre.append(idx_text)
                else:
                    break
            if sheet == 9:
                print('pq1')
                try:
                    next_sheet = await middle_frame_content.wait_for_selector(tms_xpaths.list_discharge_next_xp)
                    await next_sheet.click()
                    waiting = await middle_frame_content.wait_for_selector(tms_xpaths.list_discharge_next_sheet_waiting_xp(sheet))
                    await waiting.click()
                except TimeoutError:
                    break
            elif (sheet + 1) % 10 == 0:
                print('pq2')
                try:
                    next_sheet = await middle_frame_content.wait_for_selector(tms_xpaths.list_discharge_next_xp)
                    await next_sheet.click()
                    waiting = await middle_frame_content.wait_for_selector(
                        tms_xpaths.list_discharge_next_sheet_waiting_xp(sheet))
                    await waiting.click()
                except TimeoutError:
                    break
            else:
                print('pq3')
                if sheet < pages_count:
                    sheet += 1
                    adjacent_sheet = await middle_frame_content.wait_for_selector(
                        tms_xpaths.list_discharge_adjacent_page_xp(sheet))
                    await adjacent_sheet.click()
                    sheet -= 1
        return to_save_list_pre







    async def main_all_list_getter_tms(self):

        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        user_data_dir = r'C:\Users\RAKESH\AppData\Local\Google\Chrome\User Data'
        async with async_playwright() as p:
            # browser = p.chromium.launch_persistent_context(headless=False, user_data_dir=user_data_dir,executable_path=chrome_path)
            browser = await p.chromium.launch(headless=False, args=['--start-maximized'])
            # page = browser.new_page(no_viewport=True)

            # Create a new browser context
            context = await browser.new_context(no_viewport=True)
            total_pending_query_count, total_pending_claim_count, total_pending_dis_count = await self.pending_count_numbers(context)

            # LOGGING OUT
            # await self.both_query_generator(context,'chh009264',total_pending_query_count)

            await asyncio.gather(self.g_sheet_getter(context),
                                 # self.both_query_generator(context,'CHH009264'),
                                 self.both_query_generator(context, 'Chh008162',total_pending_query_count)
            )



            # all_list_gen_obj = AllListGenerator()
            # await page_g.goto('https://docs.google.com/spreadsheets/d/19HHTQZe9_8hMQJDZM4aZ01RcBqVH1-xXVv3RkR2W1ls/edit#gid=0')
            # await page_q.goto('https://tms.pmjay.gov.in/OneTMS/loginnew.htm')
            # # download spreadsheet
            # await all_list_gen_obj.spreadsheet_download_and_rename(page_g)
            #
            # await DischargeGetParameters().login(user_id, page_q)




if __name__ == '__main__':
    asyncio.run(AllListGenerator_2().main_all_list_getter_tms())
    # AllListGenerator().manipulating_downloaded_excel()
