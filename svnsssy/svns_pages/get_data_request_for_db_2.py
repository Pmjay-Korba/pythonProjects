import requests
import json
from concurrent.futures import ThreadPoolExecutor
import threading

# Input data
cases_text = """
CASE/PS5/HOSP22G146659/CK5284763	4080
CASE/PS5/HOSP22G146659/CK5318131	5440
CASE/PS5/HOSP22G146659/CK5354324	4080
CASE/PS5/HOSP22G146659/CK5372687	1999.88
CASE/PS5/HOSP22G146659/CK5373576	10506
CASE/PS5/HOSP22G146659/CK5381910	5440
CASE/PS5/HOSP22G146659/CK5472373	1938
CASE/PS5/HOSP22G146659/CK5533331	510
CASE/PS5/HOSP22G146659/CK5533346	5440
CASE/PS5/HOSP22G146659/CK5554124	5440
CASE/PS5/HOSP22G146659/CK5561427	3570
CASE/PS5/HOSP22G146659/CK5567179	3570
CASE/PS5/HOSP22G146659/CK5604038	5440
CASE/PS5/HOSP22G146659/CK5609762	10880
CASE/PS5/HOSP22G146659/CK5626569	5440
CASE/PS5/HOSP22G146659/CK5630272	5440
CASE/PS5/HOSP22G146659/CK5640108	5440
CASE/PS5/HOSP22G146659/CK5640843	5440
CASE/PS5/HOSP22G146659/CK5649256	714
CASE/PS5/HOSP22G146659/CK5706059	5440
CASE/PS5/HOSP22G146659/CK5736096	5440
CASE/PS5/HOSP22G146659/CK5749005	2890
CASE/PS5/HOSP22G146659/CK5749222	5440
CASE/PS5/HOSP22G146659/CK5749733	3070.2
CASE/PS5/HOSP22G146659/CK5811757	714
CASE/PS5/HOSP22G146659/CK5813462	5440
CASE/PS5/HOSP22G146659/CK5874695	1309
CASE/PS5/HOSP22G146659/CK5880877	1309
CASE/PS5/HOSP22G146659/CK5905794	3927
CASE/PS5/HOSP22G146659/CB5651541	5440

""".strip().splitlines()

# Constants
URL = "https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleViewDME.aspx/getData"
HOSP_CODE = "HOSP22G146659"

HEADERS = {
    "Content-Type": "application/json; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Referer": "https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleViewDME.aspx"
}

# Shared result list and lock
all_results = []
lock = threading.Lock()

# Function to send request and store result
def send_request(case_line):
    try:
        case_no, amount = case_line.strip().split()
        payload = {
            "caseNoReqR": case_no,
            "incentiveAmtText": amount,
            "hosp_code": HOSP_CODE
        }

        response = requests.post(URL, headers=HEADERS, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            with lock:
                all_results.append({
                    "case_no": case_no,
                    "amount": amount,
                    "response": data
                })
            print(f"✅ {case_no} | {amount}")
        else:
            print(f"❌ {case_no} | HTTP {response.status_code}")

    except Exception as e:
        print(f"❌ {case_line.strip()} ➤ Error: {e}")

# Run in threads
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(send_request, cases_text)

    # Save to JSON file
    with open("incentive_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved {len(all_results)} results to 'incentive_results.json'")
