import random
from playwright.sync_api import sync_playwright, TimeoutError, Page, expect
import time
from dis_tms.utils import utilities
from dkbssy.utils.colour_prints import ColourPrint
from tms_playwright.page_objs_tms import tms_xpaths

# chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"


def modal_ok_box(page,
                 partial_body_text,
                 modal_body_xpath=tms_xpaths.modal_body_xpath,
                 modal_ok_xpath=tms_xpaths.modal_ok_xpath):
    modal_body_web = page.wait_for_selector(modal_body_xpath, timeout=3000)
    web_modal_body_text = modal_body_web.inner_text()
    if partial_body_text in web_modal_body_text:
        modal_ok_button = page.wait_for_selector(modal_ok_xpath)
        modal_ok_button.click()
        ColourPrint.print_green(web_modal_body_text, "-> Done Till Here")
    else:
        ColourPrint.print_bg_red(f'No button containing "{partial_body_text}"')
        return None


def second_page(page: Page, case_number, discharge_date, location):
    discharge_button = page.wait_for_selector(tms_xpaths.discharge_xp)
    discharge_button.click()
    middle_frame_element = page.wait_for_selector(tms_xpaths.middle_frame_xp)
    # Get the iframe's content frame
    print(1100)
    middle_frame_content = middle_frame_element.content_frame()
    search_box = middle_frame_content.wait_for_selector(tms_xpaths.search_box_xp)
    search_box.fill(case_number)
    print(110022)
    search_button = middle_frame_content.wait_for_selector(tms_xpaths.search_button_xp)
    search_button.click()

    try:
        searched_case_number = middle_frame_content.wait_for_selector(tms_xpaths.search_case_num_xp(case_number))
        web_case_number = searched_case_number.inner_html()
        # print(web_case_number)
        if web_case_number == case_number:
            searched_case_number.click()

    except TimeoutError:
        ColourPrint.print_pink("ALREADY DONE")
        ColourPrint.print_yellow("Press Enter to continue")


def third_page(page: Page, discharge_date):
    middle_frame_element = page.wait_for_selector(tms_xpaths.middle_frame_xp)
    middle_frame_content = middle_frame_element.content_frame()
    get_ip_date = middle_frame_content.wait_for_selector(tms_xpaths.ip_date_xp)
    ip_date = str(get_ip_date.inner_text())
    # print('kkkk', ip_date)
    ip_date = ip_date.split("\n")[1]

    bottom_frame_element = middle_frame_content.wait_for_selector(tms_xpaths.bottom_frame_xp)
    bottom_frame_content = bottom_frame_element.content_frame()

    # waiting for loading doctor type drop down
    bottom_frame_content.select_option(tms_xpaths.doctor_type_dd_xp, tms_xpaths.doctor_type_value)
    # print(1)
    doctor_type_filled = bottom_frame_content.locator(tms_xpaths.doctor_type_text_is_other).inner_text()
    if doctor_type_filled == '':
        bottom_frame_content.select_option(tms_xpaths.doctor_type_dd_xp, tms_xpaths.doctor_type_value)
        print("Doctor type filled by second attempt")
    bottom_frame_content.select_option(tms_xpaths.doctor_name_dd_xp, utilities.doctor_name())
    # check the contact number of doctor
    contact_number = bottom_frame_content.wait_for_selector(tms_xpaths.doctor_contact_xp)
    contact_number_text = contact_number.text_content()
    print(contact_number_text)
    if contact_number_text.isdigit() and len(contact_number_text) > 5:
        print(contact_number_text)
    else:
        bottom_frame_content.select_option(tms_xpaths.doctor_name_dd_xp, utilities.doctor_name())
    # treatment start date
    treatment_start_date = bottom_frame_content.wait_for_selector(tms_xpaths.treatment_date_xp)
    treatment_start_date.click()
    # function ran
    print(1111111)
    utilities.date_entry_SYNC_in_tt_dd_follow(
        page=bottom_frame_content,
        date=ip_date,
        display_year_month_xpath=tms_xpaths.discharge_display_text_month_year_xp,
        arrow_xpath=tms_xpaths.discharge_previous_month_arrow_xp,
        date_only_xp=tms_xpaths.date_entry_for_tt_dd_fw_xp(ip_date))
    # saving the date
    print(22222222222)
    save_button = bottom_frame_content.wait_for_selector(tms_xpaths.save_treatment_date_xp)
    save_button.click()
    page.keyboard.press('PageUp')
    print(33333333333)
    modal_ok_box(bottom_frame_content, tms_xpaths.AFTER_TREATMENT_SAVE_MODAL_BODY_TEXT)
    print('save 1 popup')
    try:
        modal_ok_box(bottom_frame_content, tms_xpaths.SAVE_SUCCESSFULLY_TEXT)
    except TimeoutError:
        ColourPrint.print_yellow("NO SAVE BUTTON")

    discharge_radio = bottom_frame_content.wait_for_selector(tms_xpaths.radio_discharge_xp)
    is_dis_radio_checked = discharge_radio.is_checked()
    print(is_dis_radio_checked)
    if not is_dis_radio_checked:
        discharge_radio.click()
        bottom_frame_content.wait_for_selector(tms_xpaths.discharge_date_xp)
    else:
        ColourPrint.print_turquoise("Already Discharged Clicked")
    discharge_date_input = bottom_frame_content.wait_for_selector(tms_xpaths.discharge_date_xp)
    discharge_date_input.click()

    utilities.date_entry_SYNC_in_tt_dd_follow(
        page=bottom_frame_content,
        date=discharge_date,
        display_year_month_xpath=tms_xpaths.discharge_display_text_month_year_xp,
        arrow_xpath=tms_xpaths.discharge_previous_month_arrow_xp,
        date_only_xp=tms_xpaths.date_entry_for_tt_dd_fw_xp(discharge_date))

    # follow-up entry
    follow_up_input = bottom_frame_content.wait_for_selector(tms_xpaths.follow_up_xp)
    follow_up_input.click()
    utilities.date_entry_SYNC_in_tt_dd_follow(
        page=bottom_frame_content,
        date=discharge_date,
        display_year_month_xpath=tms_xpaths.discharge_display_text_month_year_xp,
        arrow_xpath=tms_xpaths.discharge_previous_month_arrow_xp,
        date_only_xp=tms_xpaths.date_entry_for_tt_dd_fw_xp(discharge_date, follow_up_days=5))
    # is special case
    bottom_frame_content.select_option(tms_xpaths.special_xp, tms_xpaths.special_value)
    # procedure consent radio
    consent_radio = bottom_frame_content.wait_for_selector(tms_xpaths.procedure_consent_xp)
    consent_radio.click()
    # attachment
    attachment_button = bottom_frame_content.wait_for_selector(tms_xpaths.attachment_button_xp)
    attachment_button.click()


def fourth_page(page: Page, location):
    middle_frame_element = page.wait_for_selector(tms_xpaths.middle_frame_xp)
    middle_frame_content = middle_frame_element.content_frame()

    bottom_frame_element = middle_frame_content.wait_for_selector(tms_xpaths.bottom_frame_xp)
    bottom_frame_content = bottom_frame_element.content_frame()

    modal_div_frame_element = bottom_frame_content.wait_for_selector(tms_xpaths.modal_div_frame_xp)
    modal_div_frame_content = modal_div_frame_element.content_frame()

    # main attachment table
    table_attach = modal_div_frame_content.wait_for_selector(tms_xpaths.table_attach_xp)
    t_body_items = table_attach.query_selector_all('//tbody')
    print('t_body len=', len(t_body_items))
    t_body_list = []
    for t_b in t_body_items:
        text_content = t_b.text_content()
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
                upload_key = modal_div_frame_content.query_selector(v[0])
                upload_file_name_with_path = utilities.upload_files(location, k)
                last_name_of_file = upload_file_name_with_path.split('\\')[-1]
                # print(upload_file_name_with_path)
                # print(upload_file_name_with_path.split())
                print(last_name_of_file)
                upload_key.set_input_files(upload_file_name_with_path)
                # modal pop up next
                modal_div_frame_modal_box_text = modal_div_frame_content.wait_for_selector(
                    '//div[contains(text(),"pload")]')
                modal_dialog_text = modal_div_frame_modal_box_text.text_content()
                print('---------------------------------------------------------------------------')
                print('Modal_text = ', modal_dialog_text)
                if 'Duplicate document is being uploaded. Do you want to proceed?' in modal_dialog_text:
                    dupli_ok = modal_div_frame_content.wait_for_selector(
                        "//div[div[div[normalize-space()='Duplicate document is being uploaded. Do you want to "
                        "proceed?']]]//button[normalize-space()='OK']")
                    dupli_ok.click()
                    print('Going Dupli')
                    # same selected
                    modal_div_frame_content.select_option(v[1], "SAME")
                    print('Same selected')
                    upload_key = modal_div_frame_content.query_selector(v[0])
                    upload_key.set_input_files(upload_file_name_with_path)
                    print('After Same upload pop up to come')
                    dupli_ok_second_ok = modal_div_frame_content.wait_for_selector(
                        f'//div[contains(text(),"{last_name_of_file}")]/ancestor::div['
                        f'@class="modal-content"]/descendant::button[normalize-space()="OK"]')
                    dupli_ok_second_ok.click()
                    # await modal_ok_box(modal_div_frame_content, "pload",)
                    print('After Same upload pop up done')
                    is_done_correct = True
                    print(k, 'Duplicate')
                elif 'Cannot Upload similar documents' in modal_dialog_text:
                    cannot_double = modal_div_frame_content.wait_for_selector(
                        f'//div[contains(text(),"{last_name_of_file}")]/ancestor::div['
                        f'@class="modal-content"]/descendant::button[normalize-space()="OK"]')
                    cannot_double.click()
                    is_done_correct = True
                    print(k, 'Cannot upload same')
                else:
                    uploaded = modal_div_frame_content.wait_for_selector(
                        f'//div[contains(text(),"{last_name_of_file}")]/ancestor::div['
                        f'@class="modal-content"]/descendant::button[normalize-space()="OK"]')
                    uploaded.click()
                    is_done_correct = True
                    print(k, 'Uploaded')
                print("---------------------------------------------------------------------------")
            else:
                ColourPrint.print_yellow('Already Uploaded')
            # closing the attachment box
            attach_close = bottom_frame_content.wait_for_selector(tms_xpaths.attachment_close_button_xp)
            attach_close.click()
            # disclaimer_box
            disclaimer_checkbox = bottom_frame_content.wait_for_selector(tms_xpaths.disclaimer_xp)
            disclaimer_checkbox.click()
            verify_and_submit_button = bottom_frame_content.wait_for_selector(tms_xpaths.verify_and_submit_xp)
            verify_and_submit_button.click()


def biometric(page: Page):
    middle_frame_element = page.wait_for_selector(tms_xpaths.middle_frame_xp)
    middle_frame_content = middle_frame_element.content_frame()

    bottom_frame_element = middle_frame_content.wait_for_selector(tms_xpaths.bottom_frame_xp)
    bottom_frame_content = bottom_frame_element.content_frame()

    # modal_div_frame_element = await bottom_frame_content.wait_for_selector(tms_xpaths.modal_div_frame_xp)
    # modal_div_frame_content = await modal_div_frame_element.content_frame()

    # choice of biometric or directly submit
    biometric_req_or_do_submit = bottom_frame_content.wait_for_selector(
        tms_xpaths.biometric_required_or_not_modal_xp)
    is_biometric_or_is_submit = biometric_req_or_do_submit.inner_text()
    if tms_xpaths.yes_bio_auth_required_modal_text in is_biometric_or_is_submit:
        # biometric start
        print('b1')
        # click radio
        fingerprint_radio = bottom_frame_content.wait_for_selector(tms_xpaths.biometric_capture_radio_xp)
        fingerprint_radio.click()
        print('b2')
        # second retry
        bottom_frame_content.wait_for_selector(tms_xpaths.biometric_error_1_xp)
        retry_button = bottom_frame_content.wait_for_selector(tms_xpaths.biometric_retry_xp)
        retry_button.click()
        # third retry
        bottom_frame_content.wait_for_selector(tms_xpaths.biometric_error_2_xp)
        retry_button = bottom_frame_content.wait_for_selector(tms_xpaths.biometric_retry_xp)
        retry_button.click()
        # successfully captured pop up - 3 times
        print('su0')
        success_ok_buttons = bottom_frame_content.query_selector_all(
            tms_xpaths.successfully_captured_modal_ok_xp)
        for button in reversed(success_ok_buttons):
            button.click()
            page.wait_for_timeout(250)  # Add a short delay if needed
            print(9999)
        final_discharge_pop_up = bottom_frame_content.wait_for_selector(
            tms_xpaths.final_discharge_confirm_pop_up_xp)
        final_discharge_pop_up.click()

    # final submit
    final_submit_ok_button = bottom_frame_content.wait_for_selector(tms_xpaths.final_submit_pop_up_xp)
    final_submit_ok_button.click()
    # initiate
    initiate_button = bottom_frame_content.wait_for_selector(tms_xpaths.initiate_pop_up_xp)
    initiate_button.click()
    #  Notification
    notification_button = middle_frame_content.wait_for_selector(tms_xpaths.notification_xp)
    notification_button.click()


def fifth_page(page):
    middle_frame_element = page.wait_for_selector(tms_xpaths.middle_frame_xp)
    middle_frame_content = middle_frame_element.content_frame()

    bottom_frame_element = middle_frame_content.wait_for_selector(tms_xpaths.bottom_frame_xp)
    bottom_frame_content = bottom_frame_element.content_frame()

    # click questionaire
    question_tab = middle_frame_content.wait_for_selector(tms_xpaths.questionaire_tab_xp)
    question_tab.click()
    # wait for active
    middle_frame_content.wait_for_selector(tms_xpaths.questionaire_tab_active_xp)

    radio_1 = bottom_frame_content.wait_for_selector(tms_xpaths.question_radio_1_xp)
    radio_1.click()
    radio_2 = bottom_frame_content.wait_for_selector(tms_xpaths.question_radio_2_xp)
    radio_2.click()
    # click submit
    question_submit = bottom_frame_content.wait_for_selector(tms_xpaths.question_submit_xp)
    question_submit.click()
    # claim_tab
    claim_tab = middle_frame_content.wait_for_selector(tms_xpaths.claim_tab_xp)
    claim_tab.click()
    middle_frame_content.wait_for_selector(tms_xpaths.claim_tab_active_xp)

    claim_tab_checkbox_1 = bottom_frame_content.wait_for_selector(tms_xpaths.claim_tab_checkbox_1_xp)
    claim_tab_checkbox_1.click()
    bottom_frame_content.select_option(tms_xpaths.claim_tab_action_type_xp, value='20')
    claim_tab_checkbox_2 = bottom_frame_content.wait_for_selector(tms_xpaths.claim_tab_checkbox_2_xp)
    claim_tab_checkbox_2.click()
    claim_tab_submit = bottom_frame_content.wait_for_selector(tms_xpaths.claim_tab_submit_xp)
    claim_tab_submit.click()
    # submit pop up
    submit_pop_up = bottom_frame_content.wait_for_selector(tms_xpaths.claim_tab_submit_popup)
    submit_pop_up.click()


def details_entry():
    while True:
        case_number = input("\033[93mEnter Case number: \033[0m").strip()
        discharge_date = input("\033[93mEnter Discharge date: \033[0m").strip()
        location = input(f"\033[93mEnter Address: \033[0m")
        user_input = input(f'\033[94mPress Enter to continue OR 1 to re-enter: \033[0m')
        if user_input != '1':
            return case_number, discharge_date, location


def main_sync_tms():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--start-maximized'])
        page = browser.new_page(no_viewport=True)
        page.set_default_timeout(20000)
        page.goto(tms_xpaths.first_page_url_xpath)
        username = page.wait_for_selector(tms_xpaths.username_xpath)
        username.fill(tms_xpaths.username_value)
        proceed_button = page.wait_for_selector(tms_xpaths.proceed_button_xpath)
        proceed_button.click()
        modal_ok_box(page, tms_xpaths.AFTER_PROCEED_MODAL_BODY_TEXT)
        password = page.wait_for_selector(tms_xpaths.password_xp)
        password.type(tms_xpaths.password_value)
        captcha = page.wait_for_selector(tms_xpaths.captcha_xp)
        captcha.click()
        time.sleep(10)
        login_checkbox_button = page.wait_for_selector(tms_xpaths.login_checkbox)
        login_checkbox_button.click()
        login_button = page.wait_for_selector(tms_xpaths.login_button_xp)
        login_button.click()
        # waiting for pre-auth and discharge button to load
        page.wait_for_load_state()
        pre_auth_button = page.wait_for_selector(tms_xpaths.pre_authorisation_xp)
        pre_auth_button.click()
        discharge_button = page.wait_for_selector(tms_xpaths.discharge_xp)
        discharge_button.click()

        # SECOND PAGE
        while True:
            case_number, discharge_date, location = details_entry()
            # print(details_entry())
            print(case_number, discharge_date, location)
            utilities.check_files_in_folder_before_tms_start(location)
            print(2233)
            # for case_number, discharge_date, location in [('CASE/PS7/HOSP22G146659/CK8509660', '8-8-24', r"G:\My Drive\GdrivePC\2024\AUGUST 2024\03.08.2024\ARTI PATEL 25\AAAA.jpeg")]:  # case_number_details
            try:
                second_page(page, case_number, discharge_date, location)
                page.wait_for_load_state()
                third_page(page, discharge_date)
                page.wait_for_load_state()
                fourth_page(page, location)
                page.wait_for_load_state()
                biometric(page)
                page.wait_for_load_state()
                fifth_page(page)

            except Exception as e:
                ColourPrint.print_blue("HERE except PAUSED")
                page.pause()
                # sleep to close
                time.sleep(30)
                down_logout_arrow = page.wait_for_selector(tms_xpaths.down_arrow_xp)
                down_logout_arrow.click()
                logout_button = page.wait_for_selector(tms_xpaths.logout_button_xp)
                logout_button.click()
            page.pause()


main_sync_tms()
