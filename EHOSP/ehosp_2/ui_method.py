import time
from EHOSP.tk_ehosp.alert_boxes import error_tk_box
from dkbssy.utils.colour_prints import ColourPrint, message_box
from playwright.sync_api import sync_playwright, Page, expect, TimeoutError


def nextgen_ui(context, headers, ipd_number_integer):
    page:Page = context.new_page()
    # print("🆕 Opened fresh automation tab (Page).")

    page.goto("https://nextgen.ehospital.gov.in/login")
    try:
        page.wait_for_selector("//span[normalize-space()='IPD']").click()
    except TimeoutError:
        error_tk_box(error_title="NextGen Site Login Error",
                     error_message='User is not logged in in Website. Login First in NextGen Website')
        raise
    #
    time.sleep(5)

    while True:
        page.wait_for_selector("(//i[@class='bx bx-plus arrows'])[1]").click()
        if page.wait_for_selector("//a[normalize-space()='Verify Discharge']"):
            # print('clicked plus')
            break

    page.wait_for_selector("//a[normalize-space()='Verify Discharge']").click()


    for_verify_all_list_resp = context.request.get("https://nextgen.ehospital.gov.in/api/ipd/doc/getDisPrepared?healthFacilityId=7013",
                    headers = headers)


    if for_verify_all_list_resp.ok:
        ColourPrint.print_green("Discharge initiated successfully")
        # print(for_verify_all_list_resp.json())


    page.wait_for_selector('//input[@data-placeholder="Search IPD Id or UHID"]').fill(str(ipd_number_integer))
    for i in range (100):
        page.keyboard.press('Enter')
        try:
            page.wait_for_selector(f'//tbody[@role="rowgroup"]//td[normalize-space()="{ipd_number_integer}"]', timeout=500)
            break
        except TimeoutError:
            ColourPrint.print_yellow(f'Entered pressed. Timeout -> times = {str(i)}')


    # clicking the check mark
    page.wait_for_selector(f'//tbody[@role="rowgroup"]//td[normalize-space()="{ipd_number_integer}"]/following-sibling::td//mat-icon[normalize-space()="check"]').click()

    dialog = page.locator("xpath=//mat-dialog-container[@aria-modal='true']")
    dialog.wait_for(state="visible")
    page.wait_for_timeout(2000)  # optional small delay for animations
    # 2️⃣ take the element‑only screenshot

    # 'getting the name of patient'
    # patient_name = page.wait_for_selector("//b[normalize-space()=\"Patient's Name :\"]/parent::td/following-sibling::td").text_content()


    dialog.screenshot(path=fr"screenshots/img_{ipd_number_integer}.png")  # ➜ modal.png in your working dir
    print(f"✅ Screenshot saved as img_{ipd_number_integer}.png")

    page.wait_for_selector("//button[normalize-space()='Close']").click()
    page.close()


