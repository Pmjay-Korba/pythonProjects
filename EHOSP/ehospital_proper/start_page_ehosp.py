from asyncio import timeout

from playwright.sync_api import sync_playwright, Page, TimeoutError, expect


from EHOSP.ehospital_proper import inject_custom_form_html, ehosp_selectors as selectors
import openpyxl
import os
import time

from EHOSP.tk_ehosp.ehospital_tk import get_data_from_sqlite
from EHOSP.ehospital_proper.colour_print_ehosp import ColourPrint

def excel_data():

    # Get the current working directory (where the script is located)
    base_path = os.getcwd()
    # Construct the file path dynamically
    file_path = os.path.join(base_path, "WARDS NAME.xlsx")
    print("File Path:", file_path)
    excel_wb = openpyxl.load_workbook(file_path)
    ward_ws = excel_wb['Sheet1']
    col_data = ward_ws.iter_cols(min_col=1,max_col=1, min_row=1, values_only=True)
    col_data_ward_name = list(col_data)
    print(col_data_ward_name)
    return list(col_data_ward_name[0])

# def page_loca(page:Page, selector):
#     return page.wait_for_selector(selector)

def main(page):
    # ward_names = excel_data()
    # short_ward_names = []
    # for i in ward_names:
    #     z = i.split( '(General ward)')[0]
    #     # ward_names = [('New Ward (General ward)','LOT (General ward)', 'EYE Ward (General ward)', 'NRC, (General ward)', 'SNCU., (General ward)', 'Female Ward (General ward)', 'Male Ward (General ward)', 'ISOLATION WARD (General ward)', 'Emergency Ward (General ward)', 'Darmatology Ward (General ward)', 'Orthopedic ward (General ward)', 'psychiatric ward (General ward)', 'ENT ward (General ward)', 'Oncology (General ward)', 'Paediatrics (General ward)', 'Burn Ward (General ward)', 'Surgical Ward (General ward)')]
    #     print(z)
    #     short_ward_names.append(z)

    # inject_custom_form_html.inject_department(page, short_ward_names)
    print('----------------=======================')
    ward_web_name = page.wait_for_selector(selectors.selected_ward_selector).text_content()
    print("WARD NAME", ward_web_name)
    uhid_web_id = page.wait_for_selector(selectors.uhid_xp).text_content()
    print("UHID ", uhid_web_id)
    time.sleep(0.5)
    ipd_web_id = page.wait_for_selector(selectors.ipd_id_xp).text_content()
    expect(page.locator(selectors.ipd_id_xp)).to_contain_text('2')
    print("IP ID", ipd_web_id)
    discharge_web_status =  page.wait_for_selector(selectors.discharge_status_xp).text_content()
    print('Discharge Status', discharge_web_status)

    # Injecting the proceed button
    # inject_custom_form_html.inject_department(page, ["Click to Proceed"])

    # clicking the Discharge Summary Menu
    page.wait_for_selector(selectors.discharge_summary_menu).click()

    # print(111111111)
    # time.sleep(5)
    # page.wait_for_selector(selectors.ward_selection_down_arrow).click()

    # check the options displayed or not


    ward_select_xp_effector = f"//span[contains(normalize-space(),'{ward_web_name}')]"
    # checking the selector and its effect
    selector_effector(page, selectors.ward_selection_down_arrow, ward_select_xp_effector)

    # clicking the ward
    page.wait_for_selector(f"//span[contains(normalize-space(),'{ward_web_name}')]").click()

    # searching the IPD ID - clicking the search button
    page.locator("//button[normalize-space()='Search Patient List']").click()

    # ipd_xpath = f"//td[normalize-space()='{ipd_web_id}']"
    #
    # expect(page.locator(ipd_xpath)).to_be_visible()

    print(11111111111111111111)


    search_by_ip = page.locator(selectors.search_ip)  # filling the ip
    print("entered the ip number")
    # search_by_ip.type(ipd_web_id)
    time.sleep(1)
    search_by_ip.type(ipd_web_id,delay=100)
    time.sleep(0.5)
    search_by_ip.press("Enter")
    # page.keyboard.press("Enter")
    print("Enter Pressed")
    # page.keyboard.press("Enter")
    time.sleep(1)

    ipd_xpath = f"//td[normalize-space()='{ipd_web_id}']"
    expect(page.locator(ipd_xpath)).to_be_visible()


    page.locator(selectors.prepare_summary_button).click()
    expect(page.locator(selectors.wait_for_ipd_visible)).to_be_visible()  # waiting for discharge entry page

    # connecting database
    # current_dir = os.path.dirname(__file__)
    # db_path = os.path.join(current_dir, "../tk_ehosp/ward_database_file.db")
    # db_path = os.path.abspath(db_path)  # Convert to absolute path

    current_dir = os.path.dirname(__file__)
    db_path = os.path.join(current_dir, "../tk_ehosp/ward_database_file.db")
    db_path = os.path.abspath(db_path)
    ward_data = get_data_from_sqlite(selectors.ward_dict[ward_web_name], db_path)
    # [(1, 'MALNUTRITION', 'VITALS HR 100, RR 25,\nMUAC LESS THAN 11.5CM\nWT FOR HT LESS THAN 3 SD\t', 'MGSO4\nZINC\nORS\nMV\nIRON\nCALCIUM\nPOTCHLOR', 'STABLE GAINING WEIGHT\t\nVITALS WITH IN NORMAL LIMITS', 'SUPPORTIVE MANAGMENT GIVEN FOR THE SEVERE ACUTE MALNUTRITION'), (2, '2 malnutrition', 'hr 77\nrr 22\nemaciiated\n', 'supportive medicine \nf75, f 100', 'stable\nok condition\n', 'ok')]



    # extracting the diagnosis names and put them in buttons
    ward_button_display = []
    for each_ward_data in ward_data:
        data_for_button = each_ward_data[1]
        ward_button_display.append(data_for_button)
    # print(ward_button_display)
    # selected diagnosis ny inject html
    diagnosis = inject_custom_form_html.inject_department(page, button_names=ward_button_display)
    # print(diagnosis)

    index_of_diagnosis = ward_button_display.index(diagnosis)
    print(diagnosis, 'index-', index_of_diagnosis)

    all_data_of_selected_index = ward_data[index_of_diagnosis]
    print('all', all_data_of_selected_index)

    cond_on_adm, treat_given, cond_on_disc, summary = all_data_of_selected_index[2],all_data_of_selected_index[3],all_data_of_selected_index[4],all_data_of_selected_index[5]

    page.locator(selectors.cond_at_admission_entry).fill(cond_on_adm)
    page.locator(selectors.treatment_given_entry).fill(treat_given)
    page.locator(selectors.cond_at_discharge_entry).fill(cond_on_disc)
    page.locator(selectors.brief_summary_entry).fill(summary)



    # opening the add diagnosis
    page.locator(selectors.view_diagnosis_button).click()
    expect(page.locator(selectors.add_new_diagnosis_button)).to_be_visible()

    def expect_selector_visible(selector_expect:str, page=page):
        return expect(page.locator(selector_expect)).to_be_visible()


    # page.locator(selectors.add_new_diagnosis_button).click()
    # expect_selector_visible(selectors.icd_10)

    # entering the all diagnosis present on choice button html
    all_diagnosis = diagnosis.split(",")
    print('all_diagnosis', all_diagnosis)
    for diag in all_diagnosis:
        diag = diag.strip()
        print('diag ==> ',diag)

        # check diagnosis already exists
        time.sleep(2)
        already_diagnosis_entered = page.locator(selectors.selected_diagnosis_table).text_content()
        print('Entered diagnosis Table', already_diagnosis_entered)
        if diag not in already_diagnosis_entered:

            page.locator(selectors.add_new_diagnosis_button).click()
            expect_selector_visible(selectors.icd_10)

            page.locator(selectors.diagnosis_search_entry).fill(diag)
            diagnosis_search_results_xp = f"//div[@role='listbox']//span[normalize-space()='{diag}']"
            select_new_diag = page.locator(diagnosis_search_results_xp)
            select_new_diag.click()
            expect_selector_visible(selectors.enabled_save)
            page.locator(selectors.enabled_save).click()
            print("Saved-->", diag)
            expect_selector_visible(selectors.add_new_diagnosis_button)

        else:
            print(f'Already entered diagnosis - {diag}')

    # selecting all diagnosis
    time.sleep(1)
    page.locator(selectors.checkbox_diagnosis_select).click()
    # expect(page.locator(selectors.checkbox_diagnosis_select)).to_be_checked()


    # add to diagnosis final
    page.wait_for_selector(selectors.add_to_diagnosis_final_button).click()

    # closing the diagnosis page
    # page.locator(selectors.diagnosis_close).click()


def selector_effector(page:Page, selector:str, effector:str, time_out=5) -> None:
    s_time = time.time()
    while (time.time() - s_time) < time_out:
        print('selector-effector')
        try:
            select_element = page.locator(selector)
            select_element.click(timeout=1000)
            time.sleep(0.5)
            expect(page.locator(effector)).to_be_visible(timeout=1000)
            print('selector is visible', selector)
            return
        except TimeoutError:
            print('Timeout1')
        except AssertionError:
            print(f"Assertion Effect selector '{effector}' not visible yet. Retrying...")
        time.sleep(0.5)

# if __name__ == '__main__':
#     # Call the function
#     with sync_playwright() as p:
#         # Connect to the running Chrome instance on the debugging port
#         browser = p.chromium.connect_over_cdp('http://localhost:9222')
#
#         # Get the active browser context and page (tab)
#         context = browser.contexts[0]  # Assuming you want the first context
#         page = context.pages[0]  # Assuming you want the first tab
#
#         # page =browser.new_page()
#         page.set_default_timeout(5000)
#
#         # Get the current URL
#         current_url = page.url
#         print('Current URL:', current_url)
#
#
#         main(page)

def app_function(target_title:str):
    with sync_playwright() as p:
        # Connect to the running Chrome instance on the debugging port
        browser = p.chromium.connect_over_cdp('http://localhost:9222')

        # Get the active browser context and page (tab)
        context = browser.contexts[0]  # Assuming you want the first context
        # page = context.pages[0]  # Assuming you want the first tab

        for page in context.pages:
            try:
                page_title = page.title()
                print(f"Checking page title: {page_title}")
                print("Current URL: ", page.url)

                if page_title.strip().lower() == target_title.strip().lower():
                # if page_title.strip().lower() == target_title.strip().lower():
                    print(f"Found matching page: {page_title}")
                    page.set_default_timeout(5000)
                    main(page)
                    return
            except Exception as e:
                ColourPrint.print_bg_red('Error')
                print(f"Error accessing a page: {e}")
                ColourPrint.print_bg_red('Error')

        print(f"No open tab found with title: {target_title}")

        # page =browser.new_page()
        # page.set_default_timeout(5000)

        # Get the current URL
        # current_url = page.url
        # print('Current URL:', current_url)


        main(page)



