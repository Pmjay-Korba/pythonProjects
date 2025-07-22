from dis_tms.page_obj.first_page import Page


class FourthPage(Page):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def initiate(self):
        self.switch_frames("middleFrame")
        self.find_wait_by_visible('//*[@id="Questionaire"]').click()
        self.switch_frames('bottomFrame')
        self.radio_click('(//span[@class="checkmark"])[1]')
        self.radio_click('(//span[@class="checkmark"])[3]')
        self.button_click("//button[@id='btnSubmit']")
        self.switch_frames("middleFrame")
        self.find_wait_by_visible('//*[@id="claims"]').click()
        self.switch_frames('bottomFrame')
        # checkbox 1
        self.find_wait_by_clickable("//div[@id='collaspeClaimInitDtls']//input[@id='claimDisClaimer']").click()
        self.drop_down_load_and_select("//select[@id='actionType']", "//select[@id='actionType']/option[2]", "20")
        # checkbox 2
        self.find_wait_by_clickable("//div[@class='row']//input[@id='claimDisClaimer']").click()
        # click submit button
        self.find_wait_by_visible("//button[@id='submitclaim']").click()
        self.modal_box('Do you want to Initiate?').click()


