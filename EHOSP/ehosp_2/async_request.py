
import asyncio
import json
from playwright.async_api import async_playwright

from dkbssy.utils.colour_prints import ColourPrint
from async_ui_entry import reach_summary_page
from update_dis_type import updating_discharge_type




async def async_main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        """Request to update the discharge type"""
        # await updating_discharge_type(context=context, ward_id=ward_id, ipd_number=ipd_number, discharge_type_code=discharge_type_code)

        """ UI interaction"""
        await reach_summary_page(context)

# Run it:
if __name__ == '__main__':
    ipd_number = '2018162'
    ward_id = 4057
    discharge_type_code = 1
    asyncio.run(async_main())
