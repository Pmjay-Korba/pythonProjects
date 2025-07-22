import requests

def actions(c_nums):
    # url = "https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleInitiatedcasesdme.aspx"
    url = "https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleViewDME.aspx?chps=g0tp53Ym7xe/GDAXoipiHaawERduF+/4vOS8caIkiNkfLOUtqewza/yO0hRsqvtiRZWl0EDm1iFLVaMpRSDFtT3JmCGgNQfkfSdnFqt+hD4="

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "ASP.NET_SessionId=ad0om0c20fqx34edmj244lgc",  # Update with your session cookie
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }

    response = requests.get(url, headers=headers)

    # ✅ Automatically detect encoding
    encoding = response.encoding if response.encoding else "utf-8"
    decoded_content = response.content.decode(encoding, errors="replace")

    print(decoded_content)  # Should print the correct HTML content

actions('')
'''
CASE/PS6/HOSP22G146659/CB7026938
CASE/PS6/HOSP22G146659/CK6995895
CASE/PS6/HOSP22G146659/CK6995257
CASE/PS6/HOSP22G146659/CK7005028
CASE/PS6/HOSP22G146659/CK7009485
'''