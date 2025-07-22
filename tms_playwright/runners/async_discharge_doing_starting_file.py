import asyncio
import random
from playwright.async_api import async_playwright, TimeoutError, Page
import time

from dis_tms.utils import utilities
from dkbssy.utils.colour_prints import ColourPrint
from tms_playwright.page_objs_tms import tms_xpaths

# chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"


async def modal_ok_box(page,
                       partial_body_text,
                       modal_body_xpath=tms_xpaths.modal_body_xpath,
                       modal_ok_xpath=tms_xpaths.modal_ok_xpath):
    modal_body_web = await page.wait_for_selector(modal_body_xpath, timeout=3000)
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


async def second_page(page: Page, case_number, discharge_date, location):
    # discharge_button = await page.wait_for_selector(tms_xpaths.discharge_xp)
    # await discharge_button.click()
    middle_frame_element = await page.wait_for_selector(tms_xpaths.middle_frame_xp)
    # Get the iframe's content frame
    middle_frame_content = await middle_frame_element.content_frame()
    search_box = await middle_frame_content.wait_for_selector(tms_xpaths.search_box_xp)
    await search_box.type(case_number)
    search_button = await middle_frame_content.wait_for_selector(tms_xpaths.search_button_xp)
    await search_button.click()

    try:
        searched_case_number = await middle_frame_content.wait_for_selector(tms_xpaths.search_case_num_xp(case_number))
        web_case_number = await searched_case_number.inner_html()
        # print(web_case_number)
        if web_case_number == case_number:
            await searched_case_number.click()

    except TimeoutError:
        ColourPrint.print_pink("ALREADY DONE")
        ColourPrint.print_yellow("Press Enter to continue")


async def third_page(page: Page, discharge_date):
    middle_frame_element = await page.wait_for_selector(tms_xpaths.middle_frame_xp)
    middle_frame_content = await middle_frame_element.content_frame()
    get_ip_date = await middle_frame_content.wait_for_selector(tms_xpaths.ip_date_xp)
    ip_date = str(await get_ip_date.inner_text())
    # page.wait_for_selector(timeout=)
    ip_date = ip_date.split("\n")[1]

    get_actual_registration_date = await middle_frame_content.wait_for_selector(tms_xpaths.actual_registration_date_xp)
    actual_registration_date = str(await get_actual_registration_date.inner_text())
    actual_registration_date = actual_registration_date.split("\n")[1].split()[0]

    bottom_frame_element = await middle_frame_content.wait_for_selector(tms_xpaths.bottom_frame_xp)
    bottom_frame_content = await bottom_frame_element.content_frame()

    # waiting for loading doctor type drop down
    await bottom_frame_content.select_option(tms_xpaths.doctor_type_dd_xp, tms_xpaths.doctor_type_value)
    print(101)
    doctor_type_filled = await bottom_frame_content.locator(tms_xpaths.doctor_type_text_is_other).inner_text()
    if doctor_type_filled == '':
        await bottom_frame_content.select_option(tms_xpaths.doctor_type_dd_xp, tms_xpaths.doctor_type_value)
        print("Doctor type filled by second attempt")
    await bottom_frame_content.select_option(tms_xpaths.doctor_name_dd_xp, utilities.doctor_name())
    # check the contact number of doctor
    contact_number = await bottom_frame_content.wait_for_selector(tms_xpaths.doctor_contact_xp)
    contact_number_text = await contact_number.text_content()
    print(contact_number_text)
    if contact_number_text.isdigit() and len(contact_number_text) > 5:
        print(contact_number_text)
    else:
        await bottom_frame_content.select_option(tms_xpaths.doctor_name_dd_xp, utilities.doctor_name())

    print(202)
    await bottom_frame_content.wait_for_selector('html body div#myDiv.animate-bottom form div#clinical-notes.clinical-Notes div.x_panel div.x_content span#surAndDis div.row div#treatmentSurgDateDiv.row div.x_content.row.depHeadBorder div#collapseTrtmntSurgDt.x_content.collapse.show div.row div.col-md-4.col-sm-3.col-xs-12 label b b')
    element = await bottom_frame_content.query_selector('//*[@id="surgStartDt"]')
    # Clear the existing value
    await element.fill('')

    # Set the new date value
    await  element.fill('20/04/2024')

    # Trigger the 'change' event manually
    await element.evaluate('(element) => element.dispatchEvent(new Event("change"))')


    ''''# treatment start date
    treatment_start_date = await bottom_frame_content.wait_for_selector(tms_xpaths.treatment_date_xp)
    await treatment_start_date.click()
    # function ran
    print(1111111)
    try:
        await utilities.date_entry_in_tt_dd_follow(
        page=bottom_frame_content,
        date=ip_date,
        display_year_month_xpath=tms_xpaths.discharge_display_text_month_year_xp,
        arrow_xpath=tms_xpaths.discharge_previous_month_arrow_xp,
        date_only_xp=tms_xpaths.date_entry_for_tt_dd_fw_xp(ip_date))
    except TimeoutError:
        # demo/false click
        review_button = await bottom_frame_content.wait_for_selector(tms_xpaths.review_false_xp)
        await review_button.click()
        # treatment start date
        treatment_start_date = await bottom_frame_content.wait_for_selector(tms_xpaths.treatment_date_xp)
        await treatment_start_date.click()

        await utilities.date_entry_in_tt_dd_follow(
            page=bottom_frame_content,
            date=actual_registration_date,
            display_year_month_xpath=tms_xpaths.discharge_display_text_month_year_xp,
            arrow_xpath=tms_xpaths.discharge_previous_month_arrow_xp,
            date_only_xp=tms_xpaths.date_entry_for_tt_dd_fw_xp(actual_registration_date))'''


    # date_picker_treatment_start_date = await bottom_frame_content.wait_for_selector(tms_xpaths.treatment_start_date_xp)
    # await date_picker_treatment_start_date.click()
    # saving the date
    print(22222222222)
    save_button = await bottom_frame_content.wait_for_selector(tms_xpaths.save_treatment_date_xp)
    await save_button.click()
    await page.keyboard.press('PageUp')
    print(33333333333)
    await modal_ok_box(bottom_frame_content, tms_xpaths.AFTER_TREATMENT_SAVE_MODAL_BODY_TEXT)
    print('save 1 popup')
    try:
        await modal_ok_box(bottom_frame_content, tms_xpaths.SAVE_SUCCESSFULLY_TEXT)
    except TimeoutError:
        ColourPrint.print_yellow("NO SAVE BUTTON")
    discharge_radio = await bottom_frame_content.wait_for_selector(tms_xpaths.radio_discharge_xp)
    is_dis_radio_checked = await discharge_radio.is_checked()
    print(is_dis_radio_checked)
    if not is_dis_radio_checked:
        await discharge_radio.click()
        await bottom_frame_content.wait_for_selector(tms_xpaths.discharge_date_xp)
    else:
        ColourPrint.print_turquoise("Already Discharged Clicked")
    discharge_date_input = await bottom_frame_content.wait_for_selector(tms_xpaths.discharge_date_xp)
    await discharge_date_input.click()
    await utilities.date_entry_in_tt_dd_follow(
        page=bottom_frame_content,
        date=discharge_date,
        display_year_month_xpath=tms_xpaths.discharge_display_text_month_year_xp,
        arrow_xpath=tms_xpaths.discharge_previous_month_arrow_xp,
        date_only_xp=tms_xpaths.date_entry_for_tt_dd_fw_xp(discharge_date))

    # follow-up entry
    follow_up_input = await bottom_frame_content.wait_for_selector(tms_xpaths.follow_up_xp)
    await follow_up_input.click()
    await utilities.date_entry_in_tt_dd_follow(
        page=bottom_frame_content,
        date=discharge_date,
        display_year_month_xpath=tms_xpaths.discharge_display_text_month_year_xp,
        arrow_xpath=tms_xpaths.discharge_previous_month_arrow_xp,
        date_only_xp=tms_xpaths.date_entry_for_tt_dd_fw_xp(discharge_date, follow_up_days=5),
        follow_up_days=5)
    # is special case
    await bottom_frame_content.select_option(tms_xpaths.special_xp, tms_xpaths.special_value)
    # procedure consent radio
    consent_radio = await bottom_frame_content.wait_for_selector(tms_xpaths.procedure_consent_xp)
    await consent_radio.click()
    # attachment
    attachment_button = await bottom_frame_content.wait_for_selector(tms_xpaths.attachment_button_xp)
    await attachment_button.click()


async def fourth_page(page: Page, location):
    middle_frame_element = await page.wait_for_selector(tms_xpaths.middle_frame_xp)
    middle_frame_content = await middle_frame_element.content_frame()

    bottom_frame_element = await middle_frame_content.wait_for_selector(tms_xpaths.bottom_frame_xp)
    bottom_frame_content = await bottom_frame_element.content_frame()

    modal_div_frame_element = await bottom_frame_content.wait_for_selector(tms_xpaths.modal_div_frame_xp)
    modal_div_frame_content = await modal_div_frame_element.content_frame()

    # main attachment table
    table_attach = await modal_div_frame_content.wait_for_selector(tms_xpaths.table_attach_xp)
    t_body_items = await table_attach.query_selector_all('//tbody')
    print('t_body len=', len(t_body_items))
    t_body_list = []
    for t_b in t_body_items:
        text_content = await t_b.text_content()
        t_body_list.append(text_content)
        # print(text_content.strip())
    print(t_body_list)
    # uploading process
    for k, v in tms_xpaths.files_to_upload_dict.items():
        count_list = []

        for i in t_body_list:
            n = (i.count(v[2]))
            count_list.append(n)
        print(v[2], count_list)
        # print(sum(count_list))
        if sum(count_list) == 1:
            max_retries = 1
            retries = 0
            is_done_correct = False
            while not is_done_correct and retries < max_retries:
                print('to upload', utilities.upload_files(location, k))
                upload_key = await modal_div_frame_content.query_selector(v[0])
                upload_file_name_with_path = utilities.upload_files(location, k)
                last_name_of_file = upload_file_name_with_path.split('\\')[-1]
                # print(upload_file_name_with_path)
                # print(upload_file_name_with_path.split())
                print(last_name_of_file)
                await upload_key.set_input_files(upload_file_name_with_path)
                # modal pop up next
                modal_div_frame_modal_box_text = await modal_div_frame_content.wait_for_selector(
                    '//div[contains(text(),"pload")]')
                modal_dialog_text = await modal_div_frame_modal_box_text.text_content()
                print('---------------------------------------------------------------------------')
                print('Modal_text = ', modal_dialog_text)
                if 'Duplicate document is being uploaded. Do you want to proceed?' in modal_dialog_text:
                    dupli_ok = await modal_div_frame_content.wait_for_selector(
                        "//div[div[div[normalize-space()='Duplicate document is being uploaded. Do you want to "
                        "proceed?']]]//button[normalize-space()='OK']")
                    await dupli_ok.click()
                    print('Going Dupli')
                    # same selected
                    await modal_div_frame_content.select_option(v[1], "SAME")
                    print('Same selected')
                    upload_key = await modal_div_frame_content.query_selector(v[0])
                    await upload_key.set_input_files(upload_file_name_with_path)
                    print('After Same upload pop up to come')
                    dupli_ok_second_ok = await modal_div_frame_content.wait_for_selector(
                        f'//div[contains(text(),"{last_name_of_file}")]/ancestor::div['
                        f'@class="modal-content"]/descendant::button[normalize-space()="OK"]')
                    await dupli_ok_second_ok.click()
                    # await modal_ok_box(modal_div_frame_content, "pload",)
                    print('After Same upload pop up done')
                    is_done_correct = True
                    print(k, 'Duplicate')
                elif 'Cannot Upload similar documents' in modal_dialog_text:
                    cannot_double = await modal_div_frame_content.wait_for_selector(
                        f'//div[contains(text(),"{last_name_of_file}")]/ancestor::div['
                        f'@class="modal-content"]/descendant::button[normalize-space()="OK"]')
                    await cannot_double.click()
                    is_done_correct = True
                    print(k, 'Cannot upload same')
                else:
                    uploaded = await modal_div_frame_content.wait_for_selector(
                        f'//div[contains(text(),"{last_name_of_file}")]/ancestor::div['
                        f'@class="modal-content"]/descendant::button[normalize-space()="OK"]')
                    await uploaded.click()
                    is_done_correct = True
                    print(k, 'Uploaded')
                print("---------------------------------------------------------------------------")
        else:
            ColourPrint.print_yellow('Already Uploaded')
    # closing the attachment box
    attach_close = await bottom_frame_content.wait_for_selector(tms_xpaths.attachment_close_button_xp)
    await attach_close.click()
    # disclaimer_box
    disclaimer_checkbox = await bottom_frame_content.wait_for_selector(tms_xpaths.disclaimer_xp)
    await disclaimer_checkbox.click()
    verify_and_submit_button = await bottom_frame_content.wait_for_selector(tms_xpaths.verify_and_submit_xp)
    await verify_and_submit_button.click()


async def biometric(page: Page):
    middle_frame_element = await page.wait_for_selector(tms_xpaths.middle_frame_xp)
    middle_frame_content = await middle_frame_element.content_frame()

    bottom_frame_element = await middle_frame_content.wait_for_selector(tms_xpaths.bottom_frame_xp)
    bottom_frame_content = await bottom_frame_element.content_frame()

    # modal_div_frame_element = await bottom_frame_content.wait_for_selector(tms_xpaths.modal_div_frame_xp)
    # modal_div_frame_content = await modal_div_frame_element.content_frame()

    # choice of biometric or directly submit
    biometric_req_or_do_submit = await bottom_frame_content.wait_for_selector(
        tms_xpaths.biometric_required_or_not_modal_xp)
    is_biometric_or_is_submit = await biometric_req_or_do_submit.inner_text()
    if tms_xpaths.yes_bio_auth_required_modal_text in is_biometric_or_is_submit:
        # biometric start
        print('b1')
        # click radio
        fingerprint_radio = await bottom_frame_content.wait_for_selector(tms_xpaths.biometric_capture_radio_xp)
        await fingerprint_radio.click()
        print('b2')
        # second retry
        await bottom_frame_content.wait_for_selector(tms_xpaths.biometric_error_1_xp)
        retry_button = await bottom_frame_content.wait_for_selector(tms_xpaths.biometric_retry_xp)
        await retry_button.click()
        # third retry
        await bottom_frame_content.wait_for_selector(tms_xpaths.biometric_error_2_xp)
        retry_button = await bottom_frame_content.wait_for_selector(tms_xpaths.biometric_retry_xp)
        await retry_button.click()
        # successfully captured pop up - 3 times
        print('su0')
        success_ok_buttons = await bottom_frame_content.query_selector_all(tms_xpaths.successfully_captured_modal_ok_xp)
        for button in reversed(success_ok_buttons):
            await button.click()
            await page.wait_for_timeout(250)  # Add a short delay if needed
            print(9999)

        final_discharge_pop_up = await bottom_frame_content.wait_for_selector(
            tms_xpaths.final_discharge_confirm_pop_up_xp)
        await final_discharge_pop_up.click()

    # final submit
    final_submit_ok_button = await bottom_frame_content.wait_for_selector(tms_xpaths.final_submit_pop_up_xp)
    await final_submit_ok_button.click()
    # initiate
    initiate_button = await bottom_frame_content.wait_for_selector(tms_xpaths.initiate_pop_up_xp)
    await initiate_button.click()
    #  Notification
    notification_button = await middle_frame_content.wait_for_selector(tms_xpaths.notification_xp)
    await notification_button.click()


async def fifth_page(page):
    middle_frame_element = await page.wait_for_selector(tms_xpaths.middle_frame_xp)
    middle_frame_content = await middle_frame_element.content_frame()

    bottom_frame_element = await middle_frame_content.wait_for_selector(tms_xpaths.bottom_frame_xp)
    bottom_frame_content = await bottom_frame_element.content_frame()

    # click questionaire
    question_tab = await middle_frame_content.wait_for_selector(tms_xpaths.questionaire_tab_xp)
    await question_tab.click()
    # wait for active
    await middle_frame_content.wait_for_selector(tms_xpaths.questionaire_tab_active_xp)

    radio_1 = await bottom_frame_content.wait_for_selector(tms_xpaths.question_radio_1_xp)
    await radio_1.click()
    radio_2 = await bottom_frame_content.wait_for_selector(tms_xpaths.question_radio_2_xp)
    await radio_2.click()
    # click submit
    question_submit = await bottom_frame_content.wait_for_selector(tms_xpaths.question_submit_xp)
    await question_submit.click()
    # claim_tab
    claim_tab = await middle_frame_content.wait_for_selector(tms_xpaths.claim_tab_xp)
    await claim_tab.click()
    await middle_frame_content.wait_for_selector(tms_xpaths.claim_tab_active_xp)

    claim_tab_checkbox_1 = await bottom_frame_content.wait_for_selector(tms_xpaths.claim_tab_checkbox_1_xp)
    await claim_tab_checkbox_1.click()
    await bottom_frame_content.select_option(tms_xpaths.claim_tab_action_type_xp, value='20')
    claim_tab_checkbox_2 = await bottom_frame_content.wait_for_selector(tms_xpaths.claim_tab_checkbox_2_xp)
    await claim_tab_checkbox_2.click()
    claim_tab_submit = await bottom_frame_content.wait_for_selector(tms_xpaths.claim_tab_submit_xp)
    await claim_tab_submit.click()
    # submit pop up
    submit_pop_up = await bottom_frame_content.wait_for_selector(tms_xpaths.claim_tab_submit_popup)
    await submit_pop_up.click()


async def restart_page(page: Page):
    await page.wait_for_load_state()
    dashboard = await page.wait_for_selector(tms_xpaths.dashboard_xp)
    await dashboard.click()
    await page.wait_for_load_state()
    pre_auth_button = await page.wait_for_selector(tms_xpaths.pre_authorisation_xp)
    await pre_auth_button.click()
    discharge_button = await page.wait_for_selector(tms_xpaths.discharge_xp)
    await discharge_button.click()



def details_entry():
    while True:
        case_number = input("\033[93mEnter Case number: \033[0m").strip()
        discharge_date = input("\033[93mEnter Discharge date: \033[0m").strip()
        location = input(f"\033[93mEnter Address: \033[0m")
        user_input = input(f'\033[94mPress Enter to continue OR 1 to re-enter: \033[0m')
        if user_input != '1':
            return case_number, discharge_date, location

async def main_tms():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=['--start-maximized'])
        # browser = await p.firefox.launch(headless=False)
        page = await browser.new_page(no_viewport=True)
        page.set_default_timeout(10000)
        await page.goto(tms_xpaths.first_page_url_xpath)
        username = await page.wait_for_selector(tms_xpaths.username_xpath)
        await username.fill(tms_xpaths.username_value)
        # click proceed
        proceed_button = await page.wait_for_selector(tms_xpaths.proceed_button_xpath)
        await proceed_button.click()
        await modal_ok_box(page, tms_xpaths.AFTER_PROCEED_MODAL_BODY_TEXT)
        password = await page.wait_for_selector(tms_xpaths.password_xp)
        await password.type(tms_xpaths.password_value)
        captcha = await page.wait_for_selector(tms_xpaths.captcha_xp)
        await captcha.click()
        time.sleep(10)
        login_checkbox_button = await page.wait_for_selector(tms_xpaths.login_checkbox)
        await login_checkbox_button.click()
        login_button = await page.wait_for_selector(tms_xpaths.login_button_xp)
        await login_button.click()
        # waiting for pre-auth and discharge button to load
        await page.wait_for_load_state()
        pre_auth_button = await page.wait_for_selector(tms_xpaths.pre_authorisation_xp)
        await pre_auth_button.click()
        discharge_button = await page.wait_for_selector(tms_xpaths.discharge_xp)
        await discharge_button.click()

        # SECOND PAGE
        while True:
            case_number, discharge_date, location = details_entry()
            # print(details_entry())
            print(case_number, discharge_date, location)
            utilities.check_files_in_folder_before_tms_start(location)
            print(2233)
        # for case_number, discharge_date, location in [('CASE/PS7/HOSP22G146659/CK8434473', '22-7-24',
        #                                                r"G:\My Drive\GdrivePC\2024\JULY 2024\18.07.2024\PHULMAT BAI 13\n.jpg")]:  # case_number_details
        #     'CASE/PS7/HOSP22G146659/CK7875173'
        #     'CASE/PS7/HOSP22G146659/CK8509660'
            try:
                await second_page(page, case_number, discharge_date, location)
                ColourPrint.print_blue(case_number)
                await page.wait_for_load_state()
                await third_page(page, discharge_date)
                await page.wait_for_load_state()
                await fourth_page(page, location)
                await page.wait_for_load_state()
                await biometric(page)
                await page.wait_for_load_state()
                await fifth_page(page)
                await restart_page(page)

            except Exception as e:
                ColourPrint.print_blue("here except")
                print(e)
                # sleep to close
                time.sleep(30)
                down_logout_arrow = await page.wait_for_selector(tms_xpaths.down_arrow_xp)
                await down_logout_arrow.click()
                logout_button = await page.wait_for_selector(tms_xpaths.logout_button_xp)
                await logout_button.click()
                break

        # manual closing
        await page.wait_for_event("close", timeout=0)


asyncio.run(main_tms())
