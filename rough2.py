from playwright.async_api import async_playwright
import asyncio
import requests

from TMS_new.async_tms_new.desired_page import get_desired_page_indexes_in_cdp_async_for_ASYNC


async def main(case_number, amount):
    user_title_of_page = 'Shaheed Veer Narayan Singh Ayushman Swasthya Yojna'
    page_indexes = await get_desired_page_indexes_in_cdp_async_for_ASYNC(
        user_title_of_page=user_title_of_page
    )

    if not page_indexes:
        print("Desired page not found.")
        return

    async with async_playwright() as p:
        cdp_for_main = 9222
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{cdp_for_main}")
        context = browser.contexts[0]
        page = context.pages[page_indexes[0]]

        # Get cookies
        cookies = await context.cookies()
        session_cookie = next((c for c in cookies if c['name'] == 'ASP.NET_SessionId'), None)

        if not session_cookie:
            print("Session cookie not found.")
            return

        asp_net_session = session_cookie['value']
        print(f"Extracted ASP.NET_SessionId: {asp_net_session}")

        # Make the POST request to get data
        url = "https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApViewDME.aspx/getRemark"
        headers = {
            "Content-Type": "application/json"
        }
        cookies_dict = {
            "ASP.NET_SessionId": asp_net_session
        }
        payload = {
            "caseNoReqR": f"{case_number}"  # Example case number
        }

        response = requests.post(url, headers=headers, cookies=cookies_dict, json=payload)

        if response.ok:
            data = response.json()
            print("Data fetched successfully:")
            print(data)
        else:
            print(f"Error {response.status_code}: {response.text}")

        url = "https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApViewDME.aspx/getData"
        payload = {
            "caseNoReqR": f"{case_number}",
            "incentiveAmtText": f"{amount}"
        }

        response = requests.post(url, headers=headers, cookies=cookies_dict, json=payload)

        if response.ok:
            data = response.json()
            print(data)
        else:
            print(f"Error {response.status_code}: {response.text}")

        # Do NOT close the browser since it’s externally managed

asyncio.run(main(

    case_number='CASE/PS6/HOSP22G146659/CK6983418',
    amount=2210
))
