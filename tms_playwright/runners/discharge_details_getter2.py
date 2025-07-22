from tms_playwright.discharge_to_be_done.discharge_details import DischargeGetParameters
user_id = 'CHH008164'
raw_excel_file_path = r'H:\My Drive\GdrivePC\Hospital\RSBY\New\discharge2.xlsx'
case_numbers = '''

CASE/PS7/HOSP22G146659/CK8272690
CASE/PS7/HOSP22G146659/CK8278742
CASE/PS7/HOSP22G146659/CK7953279
CASE/PS7/HOSP22G146659/CK7953281
CASE/PS7/HOSP22G146659/CK8013413
CASE/PS7/HOSP22G146659/CK7910045



'''

DischargeGetParameters().main_discharge_detail_tms(user_id,
                                                   case_numbers,
                                                   raw_excel_file_path,
                                                   is_query_question_required=True)
