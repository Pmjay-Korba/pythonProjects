import os
import random
import datetime
import subprocess
from playwright.async_api import Page, TimeoutError
from dkbssy.utils.colour_prints import ColourPrint


def doctor_name():
    doctor_name_by_visible_text = random.choice(
        ["DR ADITI SINGH PARIHAR (CGMC10585/2020)", "dr a sisodiya (3775)", "DR. BHARTI PATEL (CGMC 9308/2019)",
         "DR JYOTI SAHU (CGMC12299)", "dr m kujur (3077)", "DR NIKITA SHRIVASTAVA (1349734)"])

    doctor_name_by_value = random.choice(
        ['DR ADITI SINGH PARIHAR', 'dr a sisodiya', 'DR. BHARTI PATEL', 'DR JYOTI SAHU',
         'dr m kujur', 'DR NIKITA SHRIVASTAVA'])
    return doctor_name_by_value


def date_insert(date_value, follow_up_days=0):
    if "/" in date_value:
        str_day, str_mon, str_year = date_value.split("/")
    if "-" in date_value:
        str_day, str_mon, str_year = date_value.split("-")
    if len(str_day) != 2:
        str_day = "0" + str_day
    if len(str_mon) != 2:
        str_mon = '0' + str_mon
    if len(str_year) != 4:
        str_year = '20' + str_year
    dat_tim_obj = datetime.date(day=int(str_day), month=int(str_mon), year=int(str_year))
    follow_up_days = datetime.timedelta(follow_up_days)
    dat_tim_obj += follow_up_days
    return datetime.date.strftime(dat_tim_obj, "%d-%m-%Y")


def upload_files(location_0, starts_with):
    extensions = ['jpg', 'jpeg', 'pdf']
    full_path = location_0.strip('"')
    directory = os.path.dirname(full_path)

    matched_files = []
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().startswith(starts_with):
                # Check if the name (excluding extension) is alphabetic and allowed extension
                if filename.split('.')[0].isalnum() and filename.split('.')[1] in extensions:
                    matched_files.append(os.path.join(root, filename))
    # print(matched_files)
    if matched_files:
        return matched_files[0]


def check_files_existence(location_0) -> dict:
    files_to_upload_dict = {'pp': ('//td[contains(text(),"After Discharge Photo")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"After Discharge Photo")]/parent::tr//select',
                                   'After Discharge Photo'),  # after disc photo
                            'dd': ('//td[contains(text(),"Discharge summary documents")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"Discharge summary documents")]/parent::tr//select',
                                   'Discharge summary documents'),  # discharge
                            'aa': ('//td[contains(text(),"OperationDocuments")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"OperationDocuments")]/parent::tr//select',
                                   'OperationDocuments'),  # anaesthesia
                            'oo': ('//td[contains(text(),"Operative notes")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"Operative notes")]/parent::tr//select',
                                   'Operative notes'),  # operation notes
                            'bb': ('//td[contains(text(),"new born child")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"new born child")]/parent::tr//select',
                                   'Detailed status of the new born child'),  # baby notes
                            'll': ('//td[contains(text(),"Labour charting")]/parent::tr//input[@onchange]',
                                   '//td[contains(text(),"Labour charting")]/parent::tr//select',
                                   'Labour charting (Only in case of Elective Caesarean Delivery)'),  # labour charting
                            }
    all_files_dict = {}

    for k, v in files_to_upload_dict.items():
        # function ran
        present_file = upload_files(location_0, k)
        if present_file:
            all_files_dict[k] = present_file
        else:
            ColourPrint.print_bg_red(f'No matching Name file for "{v[2]}". Name as "{k.upper()}"')
    return all_files_dict


def check_files_in_folder_before_tms_start(location):
    directory = os.path.dirname(location.strip('"'))
    all_files_dict = check_files_existence(location)
    while True:
        if len(all_files_dict) != 6:
            ColourPrint.print_yellow('Folder location:', directory)
            ColourPrint.print_blue("Correctly Name the file in folder")
            subprocess.Popen(f'explorer "{directory}"')
            ColourPrint.print_pink('-------------------- Press Enter to Continue after naming file ------------------')
            input()
            all_files_dict = check_files_existence(location)
        else:
            break
    return all_files_dict


# print(check_files_existence(input('fileloc')))
# recheck_files(r"G:\My Drive\GdrivePC\2024\AUGUST 2024\03.08.2024\ARTI PATEL 25\AAAA.jpeg")  # case_number_details)


async def date_entry_in_tt_dd_follow(page, date, display_year_month_xpath, arrow_xpath, date_only_xp, follow_up_days=0):
    month_num_dict = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }
    num_month_dict = {
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
    }
    # getting class attribute
    discharge_display_text_month_year_get_class_xp = ('//th[contains(@class,"switch")]/ancestor::div[contains('
                                                      '@class,"picker") and contains(@style,"display: '
                                                      'block;")]/ancestor::div[contains(@class,"picker") and '
                                                      'contains(@style,"display: block;")and contains(@class,'
                                                      '"dropdown-menu")]')

    calender_class_attr = await page.wait_for_selector(discharge_display_text_month_year_get_class_xp)
    calender_class_attr_text = await calender_class_attr.get_attribute('class')
    print(calender_class_attr_text)
    print(11)
    month_year_displayed = await page.wait_for_selector(display_year_month_xpath)  # August 2024
    print(22)
    month_year_display_text = await month_year_displayed.inner_text()
    print(33)
    month_year_display_str = str(month_year_display_text)
    month_display = month_year_display_str.split()[0]  # August
    year_display = int(month_year_display_str.split()[1])  # str:2024 -> int:2024
    # modifying input date
    discharge_date_str_datetime = date_insert(date, follow_up_days)  # 01-01-2024
    # ColourPrint.print_blue('follow up', follow_up_days)
    print('date is', discharge_date_str_datetime)
    discharge_date_str_datetime_year = int(discharge_date_str_datetime.split("-")[2])  # str:2024 -> int:2024
    discharge_date_str_datetime_month = int(discharge_date_str_datetime.split("-")[1])  # str:01 -> int:1
    discharge_date_str_datetime_date = int(discharge_date_str_datetime.split("-")[0])  # str:01 -> int:1
    print(44)
    # year comparison
    if year_display == discharge_date_str_datetime_year:
        print(type(year_display), year_display, type(discharge_date_str_datetime_year),
              discharge_date_str_datetime_year)
        pass
    else:
        pass

    # month comparison
    # if month_display == 123456:  # num_month_dict[discharge_date_str_datetime_month]:
    #     print(month_display, num_month_dict[discharge_date_str_datetime_month])
    #     pass
    # else:

    times_click_back_arrow = month_num_dict[month_display] - discharge_date_str_datetime_month
    print('count click back arrow', times_click_back_arrow)
    for i in range(times_click_back_arrow):
        back_arrow = await page.wait_for_selector(arrow_xpath)
        print('Month back arrow Clicked= ', i+1)
        await back_arrow.click()
    # function run required
    click_date = await page.wait_for_selector(date_only_xp)
    await click_date.click()
    print(55)
    # clicking the hour
    dis_hour = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    dis_minute = random.choice(['00', '10', '20', '25', '30', '35', '40', '45', '50', '55'])
    current_time = datetime.datetime.now()  # 2024-08-12 01:42:40.387130
    time_delta = datetime.timedelta(hours=1)
    differ_time = current_time - time_delta  # 2024-08-12 00:42:40.387130
    differ_time = str(differ_time)
    differ_hour = str(differ_time.split()[1].split(":")[0])  # 00

    if differ_hour in dis_hour:
        differ_hour = differ_hour
    else:
        differ_hour = "20"

    time_hr_min_xp = (f'//div[contains(@class,"picker") and contains(@style,"display: block;") and contains('
                      f'@class,"dropdown-menu")]//div[contains(@class,"picker") and contains(@style,'
                      f'"display: block;")]//tbody//span[contains(text(),"{differ_hour}")]')
    print(66)
    if 'datetimepicker' in calender_class_attr_text:  # datetimepicker datetimepicker-dropdown-top-left dropdown-menu
        hour_to_click = await page.wait_for_selector(time_hr_min_xp)
        await hour_to_click.click()
        print(77)
        # clicking the minute
        time_hr_min_xp = (f'//div[contains(@class,"picker") and contains(@style,"display: block;") and contains('
                          f'@class,"dropdown-menu")]//div[contains(@class,"picker") and contains(@style,'
                          f'"display: block;")]//tbody//span[contains(text(),"{dis_minute}")]')
        min_to_click = await page.wait_for_selector(time_hr_min_xp)
        await min_to_click.click()
        print(88)
    else:
        print("NO datetimepicker")
        pass
        # try:
        #     hour_to_click = await page.wait_for_selector(time_hr_min_xp)
        #     await hour_to_click.click()
        #     # clicking the minute
        #     time_hr_min_xp = (f'//div[contains(@class,"picker") and contains(@style,"display: block;") and contains('
        #                       f'@class,"dropdown-menu")]//div[contains(@class,"picker") and contains(@style,'
        #                       f'"display: block;")]//tbody//span[contains(text(),"{dis_minute}")]')
        #     min_to_click = await page.wait_for_selector(time_hr_min_xp)
        #     await min_to_click.click()
        #
        # except TimeoutError:
        #     pass
