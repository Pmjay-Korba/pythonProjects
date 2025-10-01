import asyncio
import sys
from playwright.async_api import async_playwright, Page, TimeoutError, expect
from EHOSP.tk_ehosp.alert_boxes import error_tk_box, tk_ask_yes_no, tk_ask_input, select_ward
import random

async def enhancement(page:Page, pdf_1):
    # verify_under_treatment =
    await page.locator("//button[normalize-space()='Initiate Enhancement']").click()
    await page.locator("//button[normalize-space()='YES']").click()
    depart = await page.locator("//th[normalize-space()='Speciality']/ancestor::table/tbody//tr[1]/td[2]").text_content()

    # show more
    await page.locator("//th[normalize-space()='Speciality']/ancestor::table/tbody//tr[1]/td[3]//span").click()
    diagnosis = await page.locator("//th[normalize-space()='Speciality']/ancestor::table/tbody//tr[1]/td[3]/p").text_content()
    if diagnosis.endswith("Show Less"):
        diagnosis = diagnosis.removesuffix("Show Less")

    print(depart, diagnosis)

    await page.locator("(//label[normalize-space()='Speciality:']/ancestor::div[normalize-space(@class)='row']//input[@type='text' and contains(@id,'react-select')])[1]").fill(depart)
    # await page.locator("//input[@id='react-select-36-input']").fill(depart)
    await page.keyboard.press(key='Enter')
    # await asyncio.sleep(1)

    " added this here so that option populates gets time"
    days_enhanced_str = await page.locator("//th[normalize-space()='No. of Days/Units']//ancestor::table/tbody//tr/td[5]").all_text_contents()
    days_enhanced_int = [int(i) for i in days_enhanced_str]
    total_enhanced = sum(days_enhanced_int)
    answer = tk_ask_yes_no(
        question=f'The total enhanced already taken is: {total_enhanced} days.\nDo You want to take more enhancement.\n\nIf clicked "NO" it will proceed to next case')  # returns True False
    if answer:
        "if yes diagnosis is filled"
        dd = page.locator("(//label[normalize-space()='Speciality:']/ancestor::div[normalize-space(@class)='row']//input[@type='text' and contains(@id,'react-select')])[2]")
        await dd.wait_for(state="visible")
        await dd.fill(diagnosis)
        await page.keyboard.press(key='Enter')

        # "asking the ward type"
        ward_type = select_ward()

        "selecting the type of ward"
        ward_stay =page.locator("(//label[normalize-space()='Speciality:']/ancestor::div[normalize-space(@class)='row']//input[@type='text' and contains(@id,'react-select')])[3]")
        await ward_stay.wait_for(state="visible")
        await ward_stay.fill(ward_type)
        await page.keyboard.press(key='Enter')

        user_input_days = tk_ask_input(question="How many days you want to take enhancement.\nType in below for desired days.\nPRESSING Enter without typing number of days\nwill automatically take 3 days", default="3")
        if user_input_days is None:
            error_tk_box(error_message='User Cancelled', error_title='Error')
            raise ValueError('User cancelled the user input prompt')

        await page.locator("//input[@id='noofdays']").fill(user_input_days)


        reason_enhance = random.choice(['Additional facts were diagnosed during treatment.',
                          'Details submitted during pre-auth was not correct.',
                          'Others',
                          'Treatment plan changed during hospitalization.',
                          'Treatment plan is optimized for better outcome.'
                          ])

        reason_web = page.locator("(//label[normalize-space()='Speciality:']/ancestor::div[normalize-space(@class)='row']//input[@type='text' and contains(@id,'react-select')])[4]")
        await reason_web.wait_for(state="visible")
        await reason_web.fill(reason_enhance)
        await page.keyboard.press(key='Enter')

        await page.set_input_files("//input[@type='file']", pdf_1)
        await page.locator("//div[div[label[normalize-space()='Enhancement Reason:']]]//img[@class='m9FzljqXbDJyFhzambbf']").click()
        await page.locator("//div[contains(text(),'Investigations')]/parent::div//parent::div//button[@type]").click()
        await page.locator("//button[normalize-space()='Add Bed Side Photo']").click()
        await page.set_input_files("//label[normalize-space()='Upload Attachment']/following-sibling::div//input", pdf_1)
        await page.locator("//button[contains(@data-toggle,'collapse')][normalize-space()='ADD']").click()

        await page.locator("//button[normalize-space()='VALIDATE & PREVIEW']").click()
        await page.locator("//button[normalize-space()='SUBMIT ENHANCEMENT']").click()
        await page.locator("//label[normalize-space()='Are you sure want to submit?']/ancestor::div[@class='modal-content']//button[normalize-space()='YES']").click()

async def enhancement_type_2(page:Page, pdfs_list):
    await page.locator("//button[normalize-space()='Initiate Enhancement']").click()
    await page.locator("//button[normalize-space()='YES']").click()
    await page.locator('(//tr[not(.//p[contains(., "High end radiol")])]//img[@data-tip="you can change Stratification and no.of days"] )[last()]').click()  # skipping the enhancing the radiology

    pdf_1, pdf_2, pdf_3 = pdfs_list
    # "added this here so that option populates gets time"
    # days_enhanced_str = await page.locator(
    #     "//th[normalize-space()='No. of Days/Units']//ancestor::table/tbody//tr/td[5]").all_text_contents()
    # days_enhanced_int = [int(i) for i in days_enhanced_str]
    # total_enhanced = sum(days_enhanced_int)
    # answer = tk_ask_yes_no(question=f'The total enhanced already taken is: {total_enhanced} days.\nDo You want to take more enhancement.\n\nIf clicked "NO" it will proceed to next case')  # returns True False
    # if answer:

    # select ward type
    ward_type = select_ward()

    ward_stay = page.locator("//div[contains(@class,'formgroup')]/ancestor::tr/td[4]//input[@tabindex]")
    await ward_stay.wait_for(state="visible")
    await ward_stay.fill(ward_type)
    await page.keyboard.press('Enter')

    user_input_days = tk_ask_input(
        question="How many days you want to take enhancement.\nType in below for desired days.\nPRESSING Enter without typing number of days\nwill automatically take 3 days",
        default="3")
    if user_input_days is None:
        error_tk_box(error_message='User Cancelled', error_title='Error')
        raise ValueError('User cancelled the user input prompt')

    await page.locator("//div[contains(@class,'formgroup')]/ancestor::tr/td[5]//input[@placeholder='Type here']").fill(user_input_days)
    reason_enhance = random.choice(['Additional facts were diagnosed during treatment.',
                                    'Details submitted during pre-auth was not correct.',
                                    'Others',
                                    'Treatment plan changed during hospitalization.',
                                    'Treatment plan is optimized for better outcome.'
                                    ])

    reason_web = page.locator("//div[contains(@class,'formgroup')]/ancestor::tr/td[10]//input[@tabindex='0']")
    await reason_web.wait_for(state="visible")
    await reason_web.fill(reason_enhance)
    await page.keyboard.press(key='Enter')

    # click save icon
    await page.locator("//div[contains(@class,'formgroup')]/ancestor::tr/td[13]//img[2]").click()

    # click investigation
    await page.locator("//div[normalize-space()='Investigations']/following-sibling::h2/button | //div[contains(text(),'Investigations')]/parent::div/following-sibling::h2/button").click()

    await page.locator("//button[normalize-space()='Add Other Documents']").click()
    await page.locator("//label[@for='otherInvest']/parent::div/parent::div/following-sibling::div/button[normalize-space()='ADD']").click()
    await page.set_input_files("(//p[contains(text(),'Null')]/parent::td/following-sibling::td//input)[last()]", pdf_1)
    await asyncio.sleep(1)


    await page.locator("//button[normalize-space()='Add Bed Side Photo']").click()
    await page.locator("//label[@for='otherInvest']/parent::div/parent::div/following-sibling::div/button[normalize-space()='ADD']").click()
    await page.set_input_files("//p[contains(text(),'Bed Side Photo')]/parent::td/following-sibling::td//input", pdf_2)
    await asyncio.sleep(1)


    await page.locator("//button[normalize-space()='Add Other Documents']").click()
    await page.locator("//label[@for='otherInvest']/parent::div/parent::div/following-sibling::div/button[normalize-space()='ADD']").click()
    await page.set_input_files("(//p[contains(text(),'Null')]/parent::td/following-sibling::td//input)[last()]", pdf_3)
    await asyncio.sleep(1)


    await page.locator("//button[normalize-space()='VALIDATE & PREVIEW']").click()
    await page.locator("//button[normalize-space()='SUBMIT ENHANCEMENT']").click()
    await page.locator("//label[normalize-space()='Are you sure want to submit?']/ancestor::div[@class='modal-content']//button[normalize-space()='YES']").click()

    await asyncio.sleep(3)


    # sys.exit()


