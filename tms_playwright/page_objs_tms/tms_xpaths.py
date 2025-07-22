from dis_tms.utils import utilities

username_value = 'CHH009264'
# username_value = 'CHH008164'
password_value = 'Gmc@12345'
first_page_url_xpath = 'https://tms.pmjay.gov.in/OneTMS/loginnew.htm'
username_xpath = '//*[@id="username"]'
proceed_button_xpath = '//*[@id="proceed"]'
password_xp = '//*[@id="password"]'
captcha_xp = '//*[@id="reqCaptcha"]'
login_checkbox = '//*[@id="checkSubmit"]'
login_button_xp = '//button[@id="login-submit"]'
modal_body_xpath = '//div[contains(@class,"bootbox") and contains(@class,"show")]/descendant::div[@class="bootbox-body"]'
modal_ok_xpath = '//div[contains(@class,"bootbox") and contains(@class,"show")]/descendant::button[text()="OK"]'
AFTER_PROCEED_MODAL_BODY_TEXT = 'Please continue with existing User-id and Password'

# SECOND PAGE
down_arrow_xp = '//span[contains(@style,"display:inline")]'
logout_button_xp = '//a[normalize-space()="Log Out" and not(contains(@style, "color"))]'
dashboard_xp = '//span[normalize-space()="Dashboard"]'
pre_authorisation_xp = '//span[normalize-space()="Preauthorization"]'
discharge_xp = '//span[normalize-space()="Cases for Surgery/Discharge"]'
search_box_xp = '//input[@name="caseNo"]'
search_button_xp = '//button[normalize-space()="Search"]'
# search_case_num_xp = '//*[@id="no-more-tables"]/table/tbody/tr/td[2]/b/u/a'
doctor_type_xp = '//select[@id="surDocType"]'
ip_date_xp = '//b[text()="IP Registered Date: "]/parent::label/parent::div'
actual_registration_date_xp = '//b[text()="Actual Registration Date: "]/parent::label/parent::div'
type_doctor_to_click_xp = '(//span[@role="presentation"])[1]'
type_doctor_input = '//input[@type="search"]'

doctor_type_dd_xp = '//*[@id="surDocType"]'
doctor_type_wait_xp = '//*[@id="surDocType"]/option',
doctor_type_text_is_other = '//*[@id="select2-surDocType-container"]'
doctor_name_label = '//b[text()="Name"]'
doctor_type_value = "O"
doctor_name_dd_xp = '//*[@id="surgeonName"]'
doctor_name_wait_xp = '//select[@id="surgeonName"]/option[3]'
doctor_contact_xp = "//input[@id='surgeonCnctNo']"
# doctor_name_value = utilities.doctor_name()
treatment_date_xp = '//input[@id="surgStartDt"]'
date_picker_xp = '//div[contains(@class,"datepicker-dropdown")]'
treatment_start_date_xp = '//div[contains(@class,"datepicker-dropdown")]//td[not(contains(@class,"disabled"))]'
review_false_xp = '//*[@id="review"]'

save_treatment_date_xp = '//button[@id="dateUpdate"]'
AFTER_TREATMENT_SAVE_MODAL_BODY_TEXT = 'Do you want to save Treatment start/ Surgery dates?'
SAVE_SUCCESSFULLY_TEXT = 'Saved Successfully'
radio_discharge_xp = '//*[@id="discharge"]'

discharge_date_xp = '//input[@id="disDate"]'
discharge_date_datetime_picker_xp = ('//div[contains(@class,"datetimepicker") and contains(@style,"display: block;") '
                                     'and not (contains(@class,"dropdown-menu"))]')
discharge_display_text_month_year_xp = '//div[contains(@class,"picker") and contains(@style,"display: block;")and contains(@class,"dropdown-menu")]//div[contains(@class,"picker") and contains(@style,"display: block;")]//th[contains(@class,"switch")]'
discharge_display_text_month_year_get_class_xp = '//th[contains(@class,"switch")]/ancestor::div[contains(@class,"picker") and contains(@style,"display: block;")]/ancestor::div[contains(@class,"picker") and contains(@style,"display: block;")and contains(@class,"dropdown-menu")]'
discharge_previous_month_arrow_xp = '//div[contains(@class,"picker") and contains(@style,"display: block;")and contains(@class,"dropdown-menu")]//div[contains(@class,"picker") and contains(@style,"display: block;")]//th[@class="prev"]'
follow_up_xp = '//input[@id="nxtFollUpDt"]'
special_xp = '//*[@id="specCase"]'
special_value = 'NO'
procedure_consent_xp = '//*[@id="procedureConsentYes"]'
disclaimer_xp = '//*[@id="disDisClaimer"]'
table_attach_xp = '//div[@id="discharge"]'
attachment_button_xp = '//*[@id="btnattach"]'
middle_frame_xp = "//iframe[@id='middleFrame']"
bottom_frame_xp = "//iframe[@id='bottomFrame']"
modal_div_frame_xp = "//iframe[@id='modalattDivIframe']"

enter_time_tbody_xp = ('//div[contains(@class,"picker") and contains(@style,"display: block;") and contains(@class,'
                       '"dropdown-menu")]//div[contains(@class,"picker") and contains(@style,"display: '
                       'block;")]//tbody')
attachment_close_button_xp = '//button[@class="btn btn-default btn-fade"]'
verify_and_submit_xp = "//b[normalize-space()='Verify and Submit']"
biometric_required_or_not_modal_xp = ('//div[contains(@class,"modal") and contains(@class,"show") and @style="display: '
                                      'block;"]')
yes_bio_auth_required_modal_text = "Please select any one of the below Authentication Modes"
no_bio_auth_required_cum_final_submit_text = "Do you want to Submit ?"
biometric_capture_radio_xp = '//input[@value="BIOMETRIC"]'
biometric_retry_xp = '//button[normalize-space()="Retry"]'
biometric_error_1_xp = '//b[normalize-space()="You have 2 attempt(s) left"]'
biometric_error_2_xp = '//b[normalize-space()="You have 1 attempt(s) left"]'
successfully_captured_modal_ok_xp = ('//div[normalize-space()="Successfully captured Patient '
                                     'Biometric"]/ancestor::div[@class="modal-content"]//button[normalize-space('
                                     ')="OK"]')
final_discharge_confirm_pop_up_xp = '//button[text()="Discharge"]'
final_submit_pop_up_xp = ('//div[normalize-space()="Do you want to Submit ?"]/ancestor::div['
                          '@class="modal-content"]//button[normalize-space()="OK"]')
initiate_pop_up_xp = ('//div[normalize-space()="Discharge Updated.Do you want to initiate the claim '
                      '?"]/ancestor::div[@class="modal-content"]//button[normalize-space()="Yes"]')
notification_xp = '//*[@id="notify"]/div/div/div[3]/button[text()="Close"]'
questionaire_tab_xp = '//*[@id="Questionaire"]'
questionaire_tab_active_xp = '//*[@id="Questionaire" and @class="active"]'
question_radio_1_xp = '(//span[@class="checkmark"])[1]'
question_radio_2_xp = '(//span[@class="checkmark"])[3]'
question_submit_xp = "//button[@id='btnSubmit']"
claim_tab_xp = '//a[@class="tabs" and normalize-space()="Claims"]'
claim_tab_active_xp = '//*[@id="claims" and @class="active"]'
claim_tab_checkbox_1_xp = "//div[@id='collaspeClaimInitDtls']//input[@id='claimDisClaimer']"
claim_tab_checkbox_2_xp = "//div[@class='row']//input[@id='claimDisClaimer']"
claim_tab_action_type_xp = "//select[@id='actionType']"
claim_tab_submit_xp = "//button[@id='submitclaim']"
claim_tab_submit_popup = ('//div[normalize-space()="Do you want to Initiate?"]/ancestor::div['
                          '@class="modal-content"]//button[normalize-space()="OK"]')


def search_case_num_xp(case_number):
    return f'//a[normalize-space()="{case_number}"]'


def date_entry_for_tt_dd_fw_xp(str_date, follow_up_days=0):  # "%d/%m/%Y"
    date = utilities.date_insert(str_date, follow_up_days)
    date = date.split("-")
    print(f'-----{date}-----')
    date = str(int(date[0]))
    print(f'>>>>{date}<<<')
    return (f'//div[contains(@class,"picker") and contains(@style,"display: block;") and contains(@class,'
            f'"dropdown-menu")]//div[contains(@class,"picker") and contains(@style,"display: block;")]//td[contains('
            f'@class,"day") and not(contains(@class,"disabled")) and not(contains(@class,"new")) and not(contains('
            f'@class,"old")) and text()="{date}"]')


files_to_upload_dict = {'pp': ('//td[contains(text(),"After Discharge Photo")]/parent::tr//input[@onchange]',
                               '//td[contains(text(),"After Discharge Photo")]/parent::tr//select',
                               'After Discharge Photo'),  # after disc photo
                        'dd': ('//td[contains(text(),"Discharge summary documents")]/parent::tr//input[@onchange]',
                               '//td[contains(text(),"Discharge summary documents")]/parent::tr//select',
                               'Discharge summary documents'),  # discharge
                        'aa': ('//td[contains(text(),"OperationDocuments")]/parent::tr//input[@onchange]',
                               '//td[contains(text(),"OperationDocuments")]/parent::tr//select',
                               'OperationDocuments'),  # anaesthesia
                        'oo': ('//td[contains(text(),"Operative notes")]/parent::tr//input[@onchange]',
                               '//td[contains(text(),"Operative notes")]/parent::tr//select',
                               'Operative notes'),  # operation notes
                        'bb': ('//td[contains(text(),"new born child")]/parent::tr//input[@onchange]',
                               '//td[contains(text(),"new born child")]/parent::tr//select',
                               'Detailed status of the new born child'),  # baby notes
                        'll': ('//td[contains(text(),"Labour charting")]/parent::tr//input[@onchange]',
                               '//td[contains(text(),"Labour charting")]/parent::tr//select',
                               'Labour charting (Only in case of Elective Caesarean Delivery)'),  # labour charting
                        }

'''xpaths for the discharge to be done , getting the deatis of that for module discharge_to_be_done'''
dis_details_case_number_field_xp = '//input[@id="caseNum" and not(@type="hidden")]'
dis_details_type_down_arrow_xp = '//*[@id="preauthForApproval"]/div[2]/div[2]/span/span[1]/span/span[2]/b'
dis_details_input_box = "//input[@role='textbox']"
dis_details_search_button_xp = "//button[normalize-space()='Search']"
dis_details_wait_for_table_xp = '//*[@id="dataTable"]/tbody/tr/td[2]/a'
dis_details_card_xp = '//*[@id="dataTable"]/tbody/tr/td[6]'
dis_details_status_xp = '//*[@id="dataTable"]/tbody/tr/td[7]'
dis_details_name_xp = '//*[@id="no-more-tables"]/table/tbody/tr[1]/td[4]'
dis_details_depart_xp = '//*[@id="dataTable"]/tbody/tr/td[11]'
dis_details_procedure_xp = '//*[@id="dataTable"]/tbody/tr/td[12]'
dis_details_date_xp = '//*[@id="dataTable"]/tbody/tr/td[9]'
dis_detail_not_found = '//strong'

"""Claim Query xpaths"""
claim_list_gen_menu_xp = '//*[@id="sidebar-menu"]/div/ul/li[7]/a/span[1]'
claim_list_gen_child_menu_xp = '//*[@id="childmenu6"]/li[2]/a/span[1]'
claim_list_pending_count_xp = '//*[@id="javascript:fn_pendingCases();"]/span'

claim_query_searched_case_number_xp = '//*[@id="dataTable"]/tbody/tr/td[2]/a'
claim_query_work_flow_table_xp = '//div[@id="collapseWrkflw"]'
claim_query_table_query_question_xp = '//div[contains(@id,"collapseW")]//th[text()="S.No"]/ancestor::table//tbody[last()]//td[4]'
claim_query_cases_search_tab_xp = '//span[normalize-space()="Cases Search"]'
"""Preauth"""
pre_auth_query_table_question_xp = '//div[@id="collapseWorkflow"]//tbody[last()]//td[4]'
pre_auth_query_left_side_tab_xp = '//*[@id="sidebar-menu"]/div/ul/li[3]/a/span[1]'
pre_auth_query_left_side_tab_sub_tab_xp = '//*[@id="childmenu2"]/li[3]/a/span[1]'
pre_auth_query_count_xp = '//*[@id="javascript:fn_preauthCasesMEDCO();"]/span'

'''discharge list generation'''
list_discharge_left_side_tab_xp = '//*[@id="sidebar-menu"]/div/ul/li[3]/a/span[1]'
list_discharge_left_side_tab_ACTIVE_xp = '//span[normalize-space()="Preauthorization"]/ancestor::li[@class="test active"]'
list_discharge_left_side_tab_sub_tab_xp = '//*[@id="childmenu2"]/li[2]/a/span[1]'
list_discharge_count_xp = '//*[@id="javascript:fn_getDischargeCases()"]/span'
list_discharge_next_xp = "//a[normalize-space()='Next']"


def serial_number_waiting(number):
    return f"//td[normalize-space()='{number}']"


def list_discharge_next_sheet_waiting_xp(sheet):
    return f'''//a[@href="javascript:fn_pagination({sheet + 1},'link')"]'''


def list_discharge_adjacent_page_xp(sheet):
    return f'''//a[@href="javascript:fn_pagination({sheet},'link')"]'''


def case_serial_num_xp(counting):
    return f'//*[@id="no-more-tables"]/table/tbody/tr[{counting}]/td[2]/b/u/a'

def case_serial_num_for_claim_query_gen_xp(counting):
    return f'//*[@id="no-more-tables"]/table/tbody/tr[{counting}]/td[2]/a'
