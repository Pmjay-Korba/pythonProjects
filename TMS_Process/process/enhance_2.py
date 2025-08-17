from EHOSP.tk_ehosp.alert_boxes import error_tk_box


def headers_for_tms(session_storage):
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "access-control-allow-origin": "https://provider.nha.gov.in/",
        "appname": "TMS-Provider",
        "authorization": f"Bearer {session_storage['idmToken']}",
        "uauthorization": f"Bearer {session_storage['token']}",
        "cache-control": "no-cache",
        "cid": "0",
        "content-type": "application/json; charset=UTF-8",
        "hid": "3649",
        "origin": "https://provider.nha.gov.in",
        "pid": "1935",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://provider.nha.gov.in/",
        "scode": "22",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "tid": session_storage["transactionid"],
        "uid": session_storage["userid"],
        "uname": session_storage["username"],
        "urole": session_storage["userRole"],
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "ustate": "1935"
    }
    return headers



def validate_registration_no(worksheet_datas):
    # worksheet_data =
    # [
    #   {
    #     "REGISTRATION NO": 1012321947,
    #     "CARD": "",
    #     "NAME": "",
    #     "ADMISSION DATE": "",
    #     "Total Blocking days": "",
    #     "ENHANCE STATUS": "",
    #     "LAST ENHAN TAKEN DATE": "",
    #     "REMARK": "YES",
    #     "LOCATION": ""
    #   },
    #   {
    #     "REGISTRATION NO": 1012312274,
    #     "CARD": "",
    #     ...
    #   }
    # ]
    for data in worksheet_datas:
        reg_nos = data["REGISTRATION NO"]
        if not isinstance(reg_nos, int):
            print(type(reg_nos), reg_nos)
            error_tk_box(error_title='Wrong Data Type',
                         error_message=f'The registration number -> "{reg_nos}" is not correct format. Only numerical digits are allowed')
            raise ValueError(f'Incorrect data type -> {reg_nos}')
# async def verify_regis_no_in_tms(registration_no, context, headers):
