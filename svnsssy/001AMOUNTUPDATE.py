from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set too False to watch it work
    context = browser.new_context()

    # Add the ASP.NET session cookie
    context.add_cookies([{
        'name': 'ASP.NET_SessionId',
        'value': 'cmk0jeoqitvunzzrvivzcans',  # <-- Replace with actual session value
        'domain': 'dkbssy.cg.nic.in',
        'path': '/',
        'httpOnly': True,
        'secure': True,
        'sameSite': 'Lax'
    }])

    page = context.new_page()
    page.goto("https://dkbssy.cg.nic.in/secure/incentivemodule/IncentiveDetails_EmpCodeWiseDME.aspx", wait_until='networkidle')


    # for emp_code in emp_code_list:
    # Fill in the Employee Code
    page.fill('input[id="ctl00_ContentPlaceHolder1_TextBox1"]', '66170010344')

    # Click Search
    page.click('input[id="ctl00_ContentPlaceHolder1_search"]')

    # Wait for results to load (this ID is present in the table of results)
    page.wait_for_selector('#ctl00_ContentPlaceHolder1_Label3')

    # Extract data
    unpaid_cases = page.inner_text('#ctl00_ContentPlaceHolder1_Label3')
    unpaid_amount = page.inner_text('#ctl00_ContentPlaceHolder1_Label4')
    paid_cases = page.inner_text('#ctl00_ContentPlaceHolder1_Label14')
    paid_amount = page.inner_text('#ctl00_ContentPlaceHolder1_Label5')

    # Output results
    print("Searched Employee Code: 66170010344")
    print("Unpaid Cases:", unpaid_cases)
    print("Unpaid Total Amount:", unpaid_amount)
    print("Total Paid Cases:", paid_cases)
    print("Total Paid Amount:", paid_amount)

    browser.close()
