ward_select_xp = "//input[@type='text']"
hospital_name = '//span[contains(text(),"Lt. Bisahu Das Mahant Memorial Medical College Associated Indira Gandhi Hospital Korba")]'
selected_ward_selector = ".ng-value-label.ng-star-inserted"
# ipd_id_xp = "//td[normalize-space()='IPD ID']/following-sibling::td"
ipd_id_xp = "//mat-card-title[normalize-space()='DISCHARGE']//ancestor::div//td[normalize-space()='IPD ID']/following-sibling::td"
uhid_xp = "//mat-card-title[normalize-space()='DISCHARGE']//ancestor::div//td[normalize-space()='UHID']/following-sibling::td"
discharge_status_xp = "//td[normalize-space()='Discharge Status']/following-sibling::td"
discharge_summary_menu = "//a[normalize-space()='Discharge Summary']"
ward_selection_down_arrow = "//mat-select[@formcontrolname='ward_id']//div[contains(@class,'mat-select-arrow-wrapper')]//div"
prepare_summary_button = "//button[@mattooltip='Prepare Summary']"
search_ip = "//input[@data-placeholder='Search IPD Id or UHID']"
wait_for_ipd_visible = "//span[normalize-space()='IPD ID:']/following-sibling::strong"
cond_at_admission_entry = "//label[contains(text(),'Condition at time of admission')]/following-sibling::textarea"
treatment_given_entry = "//label[contains(text(),'Treatment Details')]/following-sibling::textarea"
cond_at_discharge_entry = "//label[contains(text(),'Condition at time of discharge')]/following-sibling::textarea"
brief_summary_entry = "//label[contains(text(),'Brief Summary')]/following-sibling::textarea"
ward_dict = {
        'New Ward (General ward)': 'New',
        'LOT (General ward)': 'LOT',
        'EYE Ward (General ward)': 'EYE',
        'NRC, (General ward)': 'NRC',
        'SNCU., (General ward)': 'SNCU',
        'Female Ward (General ward)': 'Female',
        'Male Ward (General ward)': 'Male',
        'ISOLATION WARD (General ward)': 'ISOLATION',
        'Emergency Ward (General ward)': 'Emergency',
        'Darmatology Ward (General ward)': 'Darmatology',
        'Orthopedic ward (General ward)': 'Orthopedic',
        'psychiatric ward (General ward)': 'psychiatric',
        'ENT ward (General ward)': 'ENT',
        'Oncology (General ward)': 'Oncology',
        'Paediatrics (General ward)': 'Paediatrics',
        'Burn Ward (General ward)': 'Burn',
        'Surgical Ward (General ward)': 'Surgical',
    }
view_diagnosis_button = "//button[normalize-space()='View Diagnosis']"
add_new_diagnosis_button = "//b[normalize-space()='Add New Diagnosis']"
icd_10 = "//label[normalize-space()='ICD-10 Code']"
diagnosis_search_entry = "//input[@placeholder='Type keyword to search']"
diagnosis_search_results = "//div[@role='listbox']//span[normalize-space()='Anaemia']"
enabled_save = "//button[normalize-space()='SAVE' and not(@disabled)]"
selected_diagnosis_table = "//th[normalize-space()='ICD-10 Code']/ancestor::table"
diagnosis_close = "//b[normalize-space()='X']"
checkbox_diagnosis_select = "(//b[normalize-space()='Add New Diagnosis']/parent::button/parent::div/parent::div//mat-checkbox)[1]"
add_to_diagnosis_final_button = "//span[normalize-space()='Add to Diagnosis(in summary)']"

