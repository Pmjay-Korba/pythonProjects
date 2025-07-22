
from playwright.async_api import async_playwright, Page, expect
import pyautogui
import asyncio
import json
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
