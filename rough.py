from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        request_context = p.request.new_context(
            extra_http_headers={
                "authorization": "Bearer eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4R0NNIiwidHlwIjoiSldUIiwiY3R5IjoiSldUIiwiemlwIjoiREVGIiwia2lkIjoiNSJ9.ouaJEwFXH4Ngr19pilCInXECTyw33mpM.-U0xy7No2at1HTA6.Qhm5p1JNSy-VTMp7m7KNcCAThwkL0YH9ZTrGodswlsz_4Xz_rI0_2r7z1iA2KdWOru4M_Yog_GM2WjACv4QoB6qDCw0boIU_qLfbedBrUbhY9t2ODFTsz1fXbpch4-mVcw6Gjjc-W1_lWxkb-U6jfd2OWfKJ1u0ouI5HERY9ppaSYfHJUvxdr7CgTR6CYlAnSmkrTU2h9gNgtpB94kp-N8Q8cA6Ct7wd86Up09TutHdf0niNS6ebtTrBUhATU3GypSsKaZ7KL5mzdEcq2b6zrhHfSp-ORxWWhOFXwRJs1XQF430r9fbH-RgZpkm1lfhz1MpKt858QuNc6Clh1h5-gYU0cDGlP6scQL9Xuchb2InqMvXVLqQnvW0bHGSRuJtQ0thihgr6u-xhERgMrpxuH11A9LcXdF9ri4OxPo3cAT04ZmtAJdAvo06xCe7s0fa9V2Q4_Ew42RI7cnDpQriGe1qEWafq4GWrcE2466ae2Y2oidSOlOgQ47i3HaVpWT3V24Yc4byDyKjbPE9vMHmmE_v6U05204IO60e-JX93uAsBb9XwQ5EEb0MAm6DsX1fWJ8ybsQKiEqzDIOLbhA3yjDGiD9WCRjU4A2t-k3AXqylVYYS342SHAP15pbfGftqhnwgm6yngfmFD_7mD854D68dTItTH_79g9RxG3vXE9p1EWT454Q5-GGFL18OyWwRHRoxVwfva4SB4hMS_Ogqmkg7-BUQJM9lfkAZhMjBoaYHe6vSPJjt_QVUYUAXUUhisI4TVLQ89QTQGv4ApnUmTW2Mxlm0cYaStxfOSgkuweoKiRXtNnD6aDm3Pgg-LBXZvCRP_4tFjs2aCcooYgofHdDHBxoT7ON7km5ZTmGwpKhTqNcf4ta8rf6YOzJ9p08kf8fWtKV3CBQLQjnZSZEzMy8YqsnqW2JEo05DSwtZj63KRMcoEHrzXVqfnnfmIPLsj-9lWtYpIDDiL_Tvy_DiIRUQceFIS1FOub_sVh6S_QHpFXLmtzUAwBY664ArdJo0jZRWTE6yzj2kTZArK4U0yff1LUyXQ8evysJvpEC-HpLGZe7TDR6w6VK7OJOKq4EuHwLzdDYR_l6kwapG5mLAMfw1Kaflgw6ArubAYOzIFq84Q8W5T3eGG_Wer0hevy9bbxdKEODSX2oHuMyPW1QGRAUgYOWc968z9SMR_wQ-8XTFa5IjUOsfh_qugbWGx667uYJzE_qa908tiZ6whcPxOKNqDSdvnHty7FzC7Cyouk6z_l_k24ISGIN64iMsZ5DK6xM7q8zQ133OrIukAbKqcTfCXZSvKpeopw7lOqIXPkvExHad-W2g0ZKUYbrHHEFZMSffS2uj0uZ7YOZafOmbtXOoG-AJKy03Xz083n5tX2t_uQb_tXm7AYf4.nhVR0UilktVVVoQsWwpP0A",
                "uauthorization": "Bearer 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",
                "accept": "application/json",
                "content-type": "application/json; charset=UTF-8",
                "appname": "TMS-Provider",
                "Referer": "https://provider.nha.gov.in/",
                "hid": "3649",
                "scode": "22",
                "uname": "Rakesh Kumar Verma",
                "tid": "NHA:7c3d23e8-b696-4655-832f-a9aafaa60147",
                "uid": "USER684607",
                "urole": "MEDCO",
                "ustate": "1935",
                "pid": "1935",
                "cid": "0"
            }
        )

        payload = {
            "hospitalid": "3649",
            "pagenumber": "1",
            "pagesize": "10",
            "searchcriteria": [
                {"key": "status", "value": "11", "operation": "Equal"}
            ],
            "searchvalue": None
        }

        response = request_context.post(
            "https://apisprod.nha.gov.in/pmjay/provider/nproviderdashboard/V3/beneficiary/list",
            data=payload
        )

        print("Status:", response.status)
        print("Response:", response.text())

import requests

url = "https://apisprod.nha.gov.in/pmjay/provider/nproviderdashboard/V3/beneficiary/list"

headers = {
     "authorization": "Bearer eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4R0NNIiwidHlwIjoiSldUIiwiY3R5IjoiSldUIiwiemlwIjoiREVGIiwia2lkIjoiNSJ9.ouaJEwFXH4Ngr19pilCInXECTyw33mpM.-U0xy7No2at1HTA6.Qhm5p1JNSy-VTMp7m7KNcCAThwkL0YH9ZTrGodswlsz_4Xz_rI0_2r7z1iA2KdWOru4M_Yog_GM2WjACv4QoB6qDCw0boIU_qLfbedBrUbhY9t2ODFTsz1fXbpch4-mVcw6Gjjc-W1_lWxkb-U6jfd2OWfKJ1u0ouI5HERY9ppaSYfHJUvxdr7CgTR6CYlAnSmkrTU2h9gNgtpB94kp-N8Q8cA6Ct7wd86Up09TutHdf0niNS6ebtTrBUhATU3GypSsKaZ7KL5mzdEcq2b6zrhHfSp-ORxWWhOFXwRJs1XQF430r9fbH-RgZpkm1lfhz1MpKt858QuNc6Clh1h5-gYU0cDGlP6scQL9Xuchb2InqMvXVLqQnvW0bHGSRuJtQ0thihgr6u-xhERgMrpxuH11A9LcXdF9ri4OxPo3cAT04ZmtAJdAvo06xCe7s0fa9V2Q4_Ew42RI7cnDpQriGe1qEWafq4GWrcE2466ae2Y2oidSOlOgQ47i3HaVpWT3V24Yc4byDyKjbPE9vMHmmE_v6U05204IO60e-JX93uAsBb9XwQ5EEb0MAm6DsX1fWJ8ybsQKiEqzDIOLbhA3yjDGiD9WCRjU4A2t-k3AXqylVYYS342SHAP15pbfGftqhnwgm6yngfmFD_7mD854D68dTItTH_79g9RxG3vXE9p1EWT454Q5-GGFL18OyWwRHRoxVwfva4SB4hMS_Ogqmkg7-BUQJM9lfkAZhMjBoaYHe6vSPJjt_QVUYUAXUUhisI4TVLQ89QTQGv4ApnUmTW2Mxlm0cYaStxfOSgkuweoKiRXtNnD6aDm3Pgg-LBXZvCRP_4tFjs2aCcooYgofHdDHBxoT7ON7km5ZTmGwpKhTqNcf4ta8rf6YOzJ9p08kf8fWtKV3CBQLQjnZSZEzMy8YqsnqW2JEo05DSwtZj63KRMcoEHrzXVqfnnfmIPLsj-9lWtYpIDDiL_Tvy_DiIRUQceFIS1FOub_sVh6S_QHpFXLmtzUAwBY664ArdJo0jZRWTE6yzj2kTZArK4U0yff1LUyXQ8evysJvpEC-HpLGZe7TDR6w6VK7OJOKq4EuHwLzdDYR_l6kwapG5mLAMfw1Kaflgw6ArubAYOzIFq84Q8W5T3eGG_Wer0hevy9bbxdKEODSX2oHuMyPW1QGRAUgYOWc968z9SMR_wQ-8XTFa5IjUOsfh_qugbWGx667uYJzE_qa908tiZ6whcPxOKNqDSdvnHty7FzC7Cyouk6z_l_k24ISGIN64iMsZ5DK6xM7q8zQ133OrIukAbKqcTfCXZSvKpeopw7lOqIXPkvExHad-W2g0ZKUYbrHHEFZMSffS2uj0uZ7YOZafOmbtXOoG-AJKy03Xz083n5tX2t_uQb_tXm7AYf4.nhVR0UilktVVVoQsWwpP0A",
                "uauthorization": "Bearer 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",
                "accept": "application/json",
                "content-type": "application/json; charset=UTF-8",
                "appname": "TMS-Provider",
                "Referer": "https://provider.nha.gov.in/",
                "hid": "3649",
                "scode": "22",
                "uname": "Rakesh Kumar Verma",
                "tid": "NHA:7c3d23e8-b696-4655-832f-a9aafaa60147",
                "uid": "USER684607",
                "urole": "MEDCO",
                "ustate": "1935",
                "pid": "1935",
                "cid": "0"
}

payload = {
    "hospitalid": "3649",
    "pagenumber": "1",
    "pagesize": "10",
    "searchcriteria": [
        {"key": "status", "value": "11", "operation": "Equal"}
    ],
    "searchvalue": None
}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response Body:\n", response.text)

# if __name__ == "__main__":
#     main()
