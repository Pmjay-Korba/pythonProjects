import time

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from dkbssy.utils.colour_prints import ColourPrint


class Page:
    _first_page_url_xpath = 'https://tms.pmjay.gov.in/OneTMS/loginnew.htm'
    _username_xpath = '//*[@id="username"]'
    _proceed_button_xpath = '//*[@id="proceed"]'
    _password_xp = '//*[@id="password"]'
    _captcha_xp = '//*[@id="reqCaptcha"]'
    _checkbox = '//*[@id="checkSubmit"]'
    _login_button_xp = '//button[@id="login-submit"]'

    _AFTER_PROCEED_MODAL_BODY_TEXT = 'Please continue with existing User-id and Password'
    _modal_ok_xpath = '//button[text()="OK"]'  # ALREADY INSERTED IN modal_box()
    _modal_body_text_xpath = ('//button[text()="OK"]/ancestor::div[@class="modal-content"]/descendant::div['
                              '@class="bootbox-body"]')

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def load_url(self, _url):
        self.driver.get(_url)

    def find_wait_by_presence(self, xpath):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def find_wait_by_clickable(self, xpath):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def find_wait_by_visible(self, xpath):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def modal_box(self, partial_body_text,
                  modal_start_xpath='//div[contains(@class,"bootbox") and contains(@class,"show")]',
                  modal_confirm_button_text="OK"):
        # Wait for the modal to be visible and get the modal element
        web_ele_modal_start: WebElement = self.wait.until(EC.presence_of_element_located((By.XPATH, modal_start_xpath)))
        print(1, web_ele_modal_start.text)
        exle = './/div[contains(@class,"bootbox-body")]'
        xx = web_ele_modal_start.find_element(By.XPATH, exle)
        print(xx.text)


    def modal_box_2(self, partial_body_text,
                    body_text_xpath='//div[contains(@class,"bootbox") and contains(@class,"show")]/descendant::div['
                                    '@class="bootbox-body"]',
                    _modal_ok_xpath='//div[contains(@class,"bootbox") and contains(@class,"show")]/descendant::button['
                                    'text()="OK"]'):
        web_modal_body_text = self.find_wait_by_visible(body_text_xpath).text
        # print(self.find_wait_by_presence())
        # print(self.find_wait_by_presence(_modal_ok_xpath).text)
        if partial_body_text in web_modal_body_text:
            ok_button = self.find_wait_by_clickable(_modal_ok_xpath)
            ColourPrint.print_green(web_modal_body_text, "-> Done Till Here")
            return ok_button
        else:
            ColourPrint.print_bg_red(f'No button containing "{partial_body_text}"')
            return None

    def switch_frames(self, frame_name):
        if frame_name == 'default':
            self.driver.switch_to.default_content()
        if frame_name == "middleFrame":
            self.driver.switch_to.frame("middleFrame")
        if frame_name == 'bottomFrame':
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame("middleFrame")
            self.driver.switch_to.frame('bottomFrame')
        if frame_name == 'modalattDivIframe':
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame("middleFrame")
            self.driver.switch_to.frame('bottomFrame')
            self.driver.switch_to.frame('modalattDivIframe')

    def drop_down_load_and_select(self, dd_locator_xpath, option_wait_xp, selection_value):
        self.find_wait_by_presence(option_wait_xp)
        options = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, dd_locator_xpath + '/option')))
        # print(list(o.text for o in options))
        select_element = self.find_wait_by_presence(xpath=dd_locator_xpath)
        select_dd = Select(select_element)
        select_dd.select_by_value(selection_value)

    def button_click(self, xpath):
        self.find_wait_by_clickable(xpath=xpath).click()

    def radio_click(self, xpath):
        is_enabled = self.find_wait_by_presence(xpath=xpath).is_enabled()
        if is_enabled:
            self.find_wait_by_clickable(xpath=xpath).click()
        else:
            ColourPrint.print_green('Radio button disabled')
            pass


class FirstPage(Page):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def first_page_main(self, _user_id, _password):
        self.load_url(self._first_page_url_xpath)
        self.find_wait_by_clickable(self._username_xpath).send_keys(_user_id)
        self.find_wait_by_clickable(self._proceed_button_xpath).click()
        proceed_clicking = self.modal_box(self._AFTER_PROCEED_MODAL_BODY_TEXT, self._modal_body_text_xpath)
        proceed_clicking.click()
        self.find_wait_by_clickable(self._password_xp).send_keys(_password)
        self.find_wait_by_presence(self._captcha_xp).click()
        time.sleep(10)
        self.find_wait_by_clickable(self._checkbox).click()
        self.find_wait_by_clickable(self._login_button_xp).click()
