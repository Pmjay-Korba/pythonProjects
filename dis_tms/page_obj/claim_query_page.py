from dis_tms.main_webdriver.create_driver_modu import create_driver
from dis_tms.page_obj.first_page import FirstPage

username = 'CHH009264'
password = 'Gmc@12345'


def main():
    driver, wait = create_driver(10)
    fp = FirstPage(driver, wait)
    fp.first_page_main(username, password)
    # clicking claim tab
    fp.find_wait_by_visible('//span[normalize-space()="Claims"]').click()
    return driver, wait


def sub_main(case_number, driver, wait):
    fp = FirstPage(driver, wait)
    # clicking under claim tab - query
    fp.find_wait_by_visible('//span[normalize-space()="Claim Query Reply"]').click()

    fp.switch_frames('middleFrame')
    fp.find_wait_by_presence('//*[@id="caseNum"]').send_keys(case_number)
    fp.button_click('//*[normalize-space()="Search"]')
    # getting table and click
    fp.find_wait_by_clickable('//*[@id="no-more-tables"]/table/tbody/tr/td[2]/a').click()
    # waiting x path below
    fp.find_wait_by_presence('//div//b[contains(text(),"Case Status")]')
    fp.switch_frames('bottomFrame')
    data = fp.find_wait_by_visible('//*[@id="collapseWrkflw"]//table[@id="testtable"]')
    print(data.text.split('\n')[-1])
    fp.switch_frames('defalut')


def cycle():
    driver, wait = main()
    for c in ['CASE/PS7/HOSP22G146659/CK8092960', 'CASE/PS7/HOSP22G146659/CK8475798']:
        sub_main(c, driver, wait)


if __name__ == "__main__":
    cycle()
