
from playwright.async_api import async_playwright, Page, expect
import pyautogui
import asyncio
import json
from dkbssy.utils.colour_prints import ColourPrint


async def updating_discharge_type(context, ward_id, ipd_number: str, discharge_type_code:int):

    page1 = context.pages[0]
    print("✅ Page 1: manual login session preserved.")

    if len(context.pages) > 1:
        page2 = context.pages[1]
        print("🔁 Reusing existing automation tab (Page 2).")
    else:
        page2 = await context.new_page()
        print("🆕 Opened fresh automation tab (Page 2).")
        await page2.goto("https://nextgen.ehospital.gov.in/login")


    token = "Bearer cinnJRZ1gxUTH9YvFc2kh7HXskB6vAiO"
    if not token or "your_token_here" in token:
        print("❌ No token provided. Please paste your Bearer token.")
        return

    print("🔑 Using Bearer Token:", token[:50] + "...")

    request = context.request

    headers = {
        "Authorization": token,
        "usertype": "5",
    }

    discharge_types_resp = await request.get(
        "https://nextgen.ehospital.gov.in/api/ipd/doc/dischargetype",
        headers=headers
    )
    if discharge_types_resp.ok:
        discharge_types = await discharge_types_resp.json()
    else:
        print("❌ Error fetching discharge types:", discharge_types_resp.status)

    ward_names_resp = await request.get(
        "https://nextgen.ehospital.gov.in/api/ipd/common/wardMaster/7013",
        headers=headers
    )
    if ward_names_resp.ok:
        ward_json = await ward_names_resp.json()
        ColourPrint.print_yellow('='*25)
        print(ward_json['metadata'])

    patient_list_resp = await request.get(
        f'https://nextgen.ehospital.gov.in/api/ipd/common/patientByWard/7013/{ward_id}',
        headers=headers
    )

    if patient_list_resp.ok:
        patient_details = (await patient_list_resp.json())['result']

        ColourPrint.print_pink('-=' * 25)
        print('Count of Names:-', len(patient_details))
        ColourPrint.print_pink('-=' * 25)

        for each_patient_details in patient_details:
            if ipd_number.strip() in each_patient_details["admno"]:
                ipd_id_web = each_patient_details["ipd_id"]
                ColourPrint.print_pink('='*50)
                ColourPrint.print_pink('Patient IPD WEB ID')
                print(ipd_id_web)
                ColourPrint.print_pink('='*50)

                ColourPrint.print_turquoise('-'*50)
                ColourPrint.print_turquoise("Each Patient Data")
                x = dict(sorted(each_patient_details.items(), key=lambda xx: xx[0]))
                print(x)
                ColourPrint.print_turquoise('-'*50)

                get_patient_status = await request.get(
                    f'https://nextgen.ehospital.gov.in/api/ipd/doc/patientInitStatus/7013/{ipd_id_web}',
                    headers=headers
                )
                if get_patient_status.ok:
                    patient_data = await get_patient_status.json()
                    ColourPrint.print_yellow('.'*50)
                    ColourPrint.print_yellow('Patient Initiation Status')
                    print(patient_data)
                    ColourPrint.print_yellow('.'*50)

                    if not patient_data['result']:
                        payload = {
                            "uhid": each_patient_details['uhid'],
                            "ipd_id": each_patient_details['ipd_id'],
                            "health_facility_id": each_patient_details["health_facility_id"],
                            "ward_id": each_patient_details["ward_id"],
                            "bed_id": each_patient_details["bed_id"],
                            "dis_initiated_by": "Neha_701336",
                            "dis_type": discharge_type_code,
                            "ipd_doc": each_patient_details["ipd_doctor_id"]
                        }
                        print('Payload = ', payload)

                        post_headers = {
                            "Authorization": token,
                            "Content-Type": "application/json",
                            "usertype": "5",
                            "userdepartmentarray": ""
                        }

                        resp = await request.post(
                            "https://nextgen.ehospital.gov.in/api/ipd/doc/saveDischargeInit",
                            headers=post_headers,
                            data=json.dumps(payload)
                        )

                        if resp.ok:
                            ColourPrint.print_green("Discharge initiated successfully")
                            print(await resp.json())
                        else:
                            print("❌ Failed to initiate discharge")
                            print(resp.status, await resp.json())
