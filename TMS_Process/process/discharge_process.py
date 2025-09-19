import asyncio
import sys
from playwright.async_api import async_playwright, Page, TimeoutError, expect

async def discharge_main(page:Page, pdf_1mb):
    # await page.locator("//button[normalize-space()='BACK']").click() # to get the discharge page as it was inside the enhancement
    await page.get_by_text('Ready For Discharge').click()

    await page.locator("//input[@type='text' and @role='combobox']").fill('Normal Discharge')
    await page.keyboard.press('Enter')
    # The async with page.expect_download() → waits for the download to begin.
    await page.locator("//div[@id='DischargeStage']//input[@type='text']").fill('After Surgery/Treatment')
    await page.keyboard.press('Enter')

    await page.locator("//label[text()='Yes']//span").click()


    'injecting the button'
    print("PRESS CONTINUE AFTER FILLING BOTH DATES")
    await inject_continue_button(page)

    async with page.expect_download() as download_info:
        await page.locator("//a[@href and normalize-space()='Download Mangalkamna Patra']").click()

    "REMOVING THE BUTTON"
    await remove_continue_button(page)

    'here sice compiling the pages to pdf the above mangalkamna patra will be downloaded'

    await page.set_input_files('//label[@for="DischargeSummary"]//parent::fieldset//input', pdf_1mb)
    await page.set_input_files('//label[@for="AfterDischargePhoto"]//parent::fieldset//input', pdf_1mb)
    await page.set_input_files('//label[@for="Feedback Form"]//parent::fieldset//input', pdf_1mb)
    await page.set_input_files('//label[@for="Upload Medical Slip"]//parent::fieldset//input', pdf_1mb)
    await page.locator("//button[normalize-space()='SAVE']").click()
    await page.wait_for_selector(" //span[normalize-space()='Discharge Information saved successfully.']")
    await page.locator("//button[normalize-space()='DISCHARGE']").click()
    await page.locator("//button[normalize-space()='YES']").click()
    await page.locator("//label[text()='Proceed without Aadhar Authentication']/span").click()
    await page.set_input_files('//label[@for="MedicalSuperintendentDeclarationFormDuringDischarge"]/following-sibling::div//input', pdf_1mb)

    max_retries = 3
    for attempt in range(max_retries):
        await page.locator("//button[normalize-space()='SAVE']").click()
        try:
            await page.wait_for_selector(
                "//span[normalize-space()='Discharge Consent saved successfully.']",
                timeout=5000
            )
            print("Saved successfully ✅")
            break
        except:
            print(f"Attempt {attempt + 1} retrying...")

    else:
        raise Exception("Save failed after multiple attempts ❌")

    await page.locator("//button[normalize-space()='DISCHARGE' and not(@disabled)]").click()
    await asyncio.sleep(5)


    # sys.exit()


async def inject_continue_button(page: Page, button_text: str = "Continue", position: str = "bottom-right"):
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