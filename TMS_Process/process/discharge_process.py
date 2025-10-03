import asyncio
import sys
from playwright.async_api import async_playwright, Page, TimeoutError, expect

from EHOSP.tk_ehosp.alert_boxes import discharge_type_selector_tk


async def discharge_main(page:Page, pdfs_list):
    # await page.locator("//button[normalize-space()='BACK']").click() # to get the discharge page as it was inside the enhancement
    await page.get_by_text('Ready For Discharge').click()
    "Ask discharge type tk"
    discharge_type = discharge_type_selector_tk()
    await page.locator("//input[@type='text' and @role='combobox']").fill(discharge_type)
    await page.keyboard.press('Enter')
    # The async with page.expect_download() → waits for the download to begin.
    await page.locator("//div[@id='DischargeStage']//input[@type='text']").fill('After Surgery/Treatment')
    await page.keyboard.press('Enter')

    "retries logic for getting the hospital bill upload"
    yes_radio = page.locator("//label[text()='Yes']//span")
    upload_label = page.locator("//label[@for='Upload Medical Slip']")
    await yes_radio.check()
    try:
        await expect(upload_label).to_be_visible(timeout=5000)
    except TimeoutError:
        await page.evaluate("el => el.click()", await yes_radio.element_handle())
        await expect(upload_label).to_be_visible(timeout=5000)

    'injecting the button'
    print("PRESS CONTINUE AFTER FILLING BOTH DATES")
    await inject_continue_button(page)

    async with page.expect_download() as download_info:
        await page.locator("//a[@href and normalize-space()='Download Mangalkamna Patra']").click()

    "REMOVING THE BUTTON"
    await remove_continue_button(page)

    'here sice compiling the pages to pdf the above mangalkamna patra will be downloaded'

    pdf_1, pdf_2, pdf_3, pdf_4 = pdfs_list
    await page.set_input_files('//label[@for="DischargeSummary"]//parent::fieldset//input', pdf_1)
    await asyncio.sleep(1)
    await page.set_input_files('//label[@for="AfterDischargePhoto"]//parent::fieldset//input', pdf_2)
    await asyncio.sleep(1)
    await page.set_input_files('//label[@for="Feedback Form"]//parent::fieldset//input', pdf_3)
    await asyncio.sleep(1)
    await page.set_input_files('//label[@for="Upload Medical Slip"]//parent::fieldset//input', pdf_4)
    await asyncio.sleep(1)
    await page.locator("//button[normalize-space()='SAVE' and not(@disabled)]").click()
    await page.wait_for_selector(" //span[normalize-space()='Discharge Information saved successfully.']")
    await page.locator("//button[normalize-space()='DISCHARGE']").click()
    await page.locator("//button[normalize-space()='YES']").click()
    await page.locator("//label[text()='Proceed without Aadhar Authentication']/span").click()
    await page.set_input_files('//label[@for="MedicalSuperintendentDeclarationFormDuringDischarge"]/following-sibling::div//input', pdf_2)
    await asyncio.sleep(1)

    # max_retries = 3
    # for attempt in range(max_retries):
    #     await page.locator("//button[normalize-space()='SAVE']").click()
    #     try:
    #         await page.wait_for_selector("//span[normalize-space()='Discharge Consent saved successfully.']")
    #         print("Saved successfully ✅")
    #         break
    #     except TimeoutError:
    #         print(f"Attempt {attempt + 1} retrying...")
    #
    # else:
    #     raise Exception("Save failed after multiple attempts ❌")

    await page.locator("//button[normalize-space()='SAVE']").click()
    loader = page.locator("//img[@id='loading-image' and @alt='Loading...']")  # loader
    await loader.wait_for(state="visible", timeout=15000)
    await loader.wait_for(state="detached")

    await page.wait_for_selector("//span[normalize-space()='Discharge Consent saved successfully.']")

    await page.locator("//button[normalize-space()='DISCHARGE' and not(@disabled)]").click()
    await asyncio.sleep(5)
    # sys.exit()




async def inject_continue_button(page: Page, button_text: str = "Fill Discharge & Surgery Date than\nClick Here", position: str = "bottom-right"):
    pos_styles = {
        "bottom-right": {"right": "20px", "bottom": "20px"},
        "top-right": {"right": "20px", "top": "20px"},
        "bottom-left": {"left": "20px", "bottom": "20px"},
        "top-left": {"left": "20px", "top": "20px"},
    }
    chosen = pos_styles.get(position, pos_styles["bottom-right"])

    # Inject button (safe, does not trigger CSP unsafe-eval)
    await page.evaluate(
        """({text, chosen}) => {
            if (document.getElementById('my-continue-btn')) return;
            const btn = document.createElement('button');
            btn.id = 'my-continue-btn';
            btn.textContent = text;
            Object.assign(btn.style, {
                position: 'fixed',
                zIndex: '2147483647',
                padding: '14px 20px',
                fontSize: '18px',
                background: '#36d431',
                color: '#fff',
                border: 'none',
                borderRadius: '6px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
                cursor: 'pointer',
                ...chosen
            });
            btn.setAttribute('aria-label', text);

            btn.addEventListener('click', () => {
                btn.dataset.clicked = '1';
                btn.style.opacity = '0.6';
                btn.style.pointerEvents = 'none';
            });

            document.body.appendChild(btn);
        }""",
        {"text": button_text, "chosen": chosen},
    )

    # Manual polling loop instead of wait_for_function
    while True:
        clicked = await page.evaluate(
            "() => document.getElementById('my-continue-btn')?.dataset.clicked === '1'"
        )
        if clicked:
            break
        await asyncio.sleep(0.3)  # adjust poll interval if needed

async def remove_continue_button(page: Page):
    await page.evaluate(
        """() => {
            const btn = document.getElementById('my-continue-btn');
            if (btn) btn.remove();
        }"""
    )