
from playwright.async_api import async_playwright, Page, expect
import pyautogui
import asyncio
from EHOSP.ehosp_2.nextgen_request import fetch_excel
from TMS_Process.process.file_folder_searcher import ProjectPaths
from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC
from dkbssy.utils.colour_prints import ColourPrint



async def right_click_duplicate(n, tab_x=111, tab_y=23, duplicate_x=171,duplicate_y=266):
    for _ in range(n):
        # Step 1: Right-click on the Chrome tab area
        # tab_x, tab_y = 111, 23  # Your captured tab position
        pyautogui.rightClick(tab_x, tab_y)  # Right-click on the tab

        await asyncio.sleep(3)  # Wait for the menu to appear

        # Step 2: Click on "Duplicate" at exact coordinates
        # duplicate_x, duplicate_y = 171, 266  # Your captured "Duplicate" position
        pyautogui.click(duplicate_x, duplicate_y)

        print("Clicked on 'Duplicate' in the right-click menu")

        await asyncio.sleep(5)  # Wait for tab duplication to complete



async def reach_summary_page(context):
    page:Page = context.pages[0]

    home_icon = '//a[@href="https://nextgen.ehospital.gov.in/adminHome" or href="/adminHome"]'

    await expect(page.locator(home_icon)).to_be_visible()
    await expect(page.locator(home_icon)).to_be_enabled()
    await page.locator(home_icon).click()

    home_page_ipd_link = "//span[normalize-space()='IPD']"
    await expect(page.locator(home_page_ipd_link)).to_be_visible()
    await expect(page.locator(home_page_ipd_link)).to_be_enabled()
    await page.locator(home_page_ipd_link).click()

    admission_locator = page.get_by_text('Admission/Discharge/Transfer', exact=True)
    # await _expect_visible_enable(page, admission_locator)
    await expect(admission_locator).to_be_visible()
    await expect(admission_locator).to_be_enabled()
    await admission_locator.click()


# asyncio.run(right_click_duplicate(3)) reach summary page and search all the names than duplicate -> Duplicate page comes blank

async def apply_throttle(page, mode: str | None = None):
    """Apply or reset network throttling profile using CDP (async).
       mode=None or "none" → reset to normal network.
    """
    client = await page.context.new_cdp_session(page)
    await client.send("Network.enable")

    if mode is None or mode == "none":
        # Reset to normal (no throttling)
        await client.send("Network.emulateNetworkConditions", {
            "offline": False,
            "latency": 0,
            "downloadThroughput": -1,
            "uploadThroughput": -1,
        })
        print("[INFO] No throttling (reset to normal).")
        return

    NETWORK_PRESETS = {
        "2g": {
            "latency": 1200,  # 1.2 sec delay per request
            "download": 15 * 1024 / 8,  # ~15 KB/s
            "upload": 7 * 1024 / 8,  # ~7 KB/s
        },
        "slow3g": {"latency": 400, "download": 50 * 1024 / 8, "upload": 20 * 1024 / 8},
        "fast3g": {"latency": 150, "download": 1.6 * 1024 * 1024 / 8, "upload": 750 * 1024 / 8},
        "4g": {"latency": 70, "download": 4 * 1024 * 1024 / 8, "upload": 3 * 1024 * 1024 / 8},
        "wifi": {"latency": 30, "download": 30 * 1024 * 1024 / 8, "upload": 15 * 1024 * 1024 / 8},
    }

    if mode not in NETWORK_PRESETS:
        raise ValueError(f"Invalid mode: {mode}. Choose from {list(NETWORK_PRESETS)} or 'none'.")

    profile = NETWORK_PRESETS[mode]
    await client.send("Network.emulateNetworkConditions", {
        "offline": False,
        "latency": profile["latency"],
        "downloadThroughput": profile["download"],
        "uploadThroughput": profile["upload"],
    })

    print(f"[INFO] Applied throttling: {mode.upper()} "
          f"(latency={profile['latency']}ms, "
          f"down={profile['download']*8/1024/1024:.2f}Mbps, "
          f"up={profile['upload']*8/1024/1024:.2f}Mbps)")


async def next_gen_ui_process(cdp_port=9222):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{cdp_port}")
        context = browser.contexts[0]
        all_pages = context.pages

        pages_indexes = await get_desired_page_indexes_in_cdp_async_for_ASYNC(user_title_of_page='NextGen eHospital',
                                                                              cdp_port=cdp_port)
        page_index = pages_indexes[0]  # selecting the first index of matching page

        page = all_pages[page_index]  # selecting the first PAGE of matching page
        page.set_default_timeout(20000)

        dischargeable_ipd = fetch_excel(ProjectPaths.PROJECT_ROOT/'EHOSP'/'ehosp_2'/'ward_discharge_entry.xlsx')

        try:
            new_page_for_working = await context.new_page()
            new_page_for_working.set_default_timeout(120_000)
            new_page_for_working.set_default_navigation_timeout(120_000)
            # await apply_throttle(page=new_page_for_working, mode='2g')
            await apply_throttle(page=new_page_for_working, mode='slow3g')
            await ui_interaction(page=new_page_for_working)
        finally:
            await new_page_for_working.close()


async def ui_interaction(page:Page):
    await page.goto('https://nextgen.ehospital.gov.in/adminHome')
    await page.get_by_text('IPD').click()
    await page.goto("https://nextgen.ehospital.gov.in/ipd/discharge_init")
    await page.locator("//span[contains(text(),'IPD ID')]/preceding-sibling::span").click()
    await page.get_by_placeholder('Enter IPD ID').fill('20235894')
    await page.get_by_role(role='button', name='Search Patient').click()
    await page.get_by_role(role='button', name='Select').click()

    # GETTING THE DISCHARGE STATUS BEFORE CHANGING
    # Check visibility safely
    if await page.locator("//td[normalize-space()='Discharge Status']").is_visible():
        print("Discharge Status is visible")
    elif await page.locator("//mat-select[@role='combobox' and @formcontrolname='dis_type']").is_visible():
        print("Discharge Type combobox is visible")
    # NOW SELECTING THE RIGHT PANEL FOR THE DISCHARGE TYPE
    # await page.locator("//mat-select[@role='combobox' and @formcontrolname='dis_type']").click()

    # GETTING THE DISCHARGE TYPE MAPPER

    mapper = {
        "D": "Cured",
        "DEATH": "Expired",
        "T": "Transferred",
        "M": "DAMA Discharge against Medical Advice",
        "L": "LAMA Leave against Medical Advice",
        "A": "Absconded",
        "R": "Referral"
    }
    # Select option by visible text
    await page.get_by_role("option", name="DAMA Discharge against Medical Advice").click()

    await page.get_by_role(role='button', name='Save').click()







    await asyncio.sleep(5)





if __name__ == "__main__":
    asyncio.run(next_gen_ui_process())