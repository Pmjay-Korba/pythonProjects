import datetime
import json
import math
import time

from playwright.sync_api import Page, sync_playwright

from dkbssy.utils.colour_prints import ColourPrint
from tms_playwright.discharge_to_be_done.detail_list_getter_all import AllListGenerator as AllListGeneratorOld
from TMS_new.details_list_dis_query_NEW import AllListGenerator
from TMS_new.sync_tms import selector_xp

class TmsProvider:

    @staticmethod
    def get_desired_page(target_title)-> tuple|None:
        """
        get the desired opened page title and its context
        :param target_title:
        :return: tuple of page, context
        """
        playwright =  sync_playwright().start()
        browser =  playwright.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts
        # print('Context length', len(context))
        # print(context)
        if not browser.contexts:
            print("No active contexts found.")
            playwright.stop()
            return None

        context = browser.contexts[0]

        # Ensure there's at least one active page
        pages = context.pages if context.pages else [ context.new_page()]

        # Search for the page by title
        matched_page = None
        for page in pages:
            title =  page.title()
            print(f"Checking Page: {title} | URL: {page.url}")

            if target_title.lower() in title.lower():  # Case-insensitive search
                matched_page = page
                break

        if matched_page:
            page = matched_page
            ColourPrint.print_yellow(f"Matched Page Found: { page.title()} ({page.url})")
            print("Now working with this page...")
            page.set_default_timeout(30000)
            # page.goto()
            return page, context

        print("No matching page found.")
        playwright.stop()
        return None

    @staticmethod
    def refresh_pending_lists(page)->tuple[list,list,list]:

        all_list_gen_obj = AllListGenerator()

        ColourPrint.print_yellow('Start Treatment')
        under_treatment_list_generated = all_list_gen_obj.type_list_generate(page,
                                                                             current_status='Under Treatment',
                                                                             patient_status_field_xpath="underTreatmentWith_(",
                                                                             case_type_button="underTreatmentOnly")
        ColourPrint.print_pink('End Treatment')
        #
        ColourPrint.print_yellow('Start Pre-auth')

        pre_auth_query_list_generated = all_list_gen_obj.type_list_generate(page,
                                                                current_status="Preauthorization Queried",
                                                                patient_status_field_xpath="PreauthorizationQueried_(",
                                                                case_type_button='PreauthorizationQueriedOnly')
        ColourPrint.print_pink('End Pre-auth')
        #
        ColourPrint.print_yellow('Start Claim')
        claim_query_list_generated = all_list_gen_obj.type_list_generate(page,
                                                                         current_status="Claims Queried",
                                                                         patient_status_field_xpath="ClaimsQueried_(",
                                                                         case_type_button="ClaimsQueriedOnly")
        ColourPrint.print_pink('End Claim')

        return pre_auth_query_list_generated, claim_query_list_generated, under_treatment_list_generated
        # return pre_auth_query_list_generated

    def wait_for_updated_content_direct(self, page, xpath, placeholder="NA", timeout=60):
        """
        Waits for the text content of an element to change from a placeholder value using polling.

        Args:
            page: The Playwright page instance.
            xpath: The XPath of the target element.
            placeholder: The placeholder value to wait for change (default is 'NA').
            timeout: The maximum time to wait in seconds (default is 60).

        Returns:
            str: The updated text content of the element.

        Raises:
            TimeoutError: If the text content does not change within the timeout.
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                # Retrieve the text content of the element
                element = page.query_selector(xpath)
                if element:
                    text_content = element.text_content().strip()
                    if text_content != placeholder:  # Check if it's updated
                        return text_content
            except Exception as e:
                pass  # Ignore errors and keep polling
            time.sleep(0.5)  # Wait for 500ms before retrying

        raise TimeoutError(f"Timeout: Element with XPath '{xpath}' did not update within {timeout} seconds.")



    def retrieve_data_from_new_site(self, page: Page, case_number: str, is_query_question_required=False) -> tuple:
        """
        Retrieving scrapping the data from web
        :param is_query_question_required: is query question is required
        :param page: Playwright Page
        :param case_number: case number
        :return: list
        """


        # Load the JSON Selector file
        selector_file = r"C:\WebstormProjects\TMS_new\selectors.json"
        with open(selector_file, 'r') as file:
            selector = json.load(file)

        page.wait_for_load_state("networkidle")
        # page.wait_for_selector(selector["patientStatusInput"]).fill('')
        page.wait_for_selector(selector["patientStatusInput"]).fill('All')
        page.keyboard.press('Enter')
        time.sleep(0.25)
        page.wait_for_load_state("networkidle")
        page.wait_for_selector(selector["searchBox"]).fill("")
        page.wait_for_selector(selector["searchBox"]).fill(case_number)
        page.wait_for_load_state("networkidle")

        page.wait_for_selector(selector["searchIcon"]).click()
        page.wait_for_selector(selector["searchIcon"]).click()
        time.sleep(0.25)
        page.wait_for_selector(selector["searchIcon"]).click()
        # clicking to proceed for patient details
        page.wait_for_selector(
            f"//strong[text()='{case_number}']/parent::p/parent::div/parent::div//*[name()='path' and @id='Path_98789']").click()

        # print('case number', case_number)
        # getting the type of status
        current_status = \
        page.wait_for_selector("//a[normalize-space()='Home']/ancestor::ol//li[2]").inner_text().split("(")[
            0].strip()  # Under Treatment (1002902644)
        # print(current_status)

        page.wait_for_load_state("networkidle")
        card = page.wait_for_selector("//div[text()=' ID']/following-sibling::div").text_content()
        # print(card)
        name = page.wait_for_selector("//img[@alt='image']/parent::div/following-sibling::div/div").text_content()
        # print(name)
        # age/sex
        # status_xp = "//img[@alt='image']/parent::div/following-sibling::div/following-sibling::div/div"
        # self.wait_for_updated_content_direct(page, status_xp)
        # page.wait_for_load_state("networkidle")
        # status_element = page.wait_for_selector("//img[@alt='image']/parent::div/following-sibling::div/following-sibling::div/div")
        #
        # status = status_element.text_content()
        # # print(status)

        locator = page.locator(".qpz9NG90l1gorDZORgIn.OSVhhsHh74o0GLnLTmrt")
        # Wait for the element to appear (short timeout for presence check)
        locator.wait_for(timeout=3000, state="attached")

        # Get the initial text of the element
        initial_text = locator.inner_text()
        # print(f"Initial Text: {initial_text}")

        # Check for 'New Born' using a browser JavaScript function
        status = page.evaluate(
            """
            ({ locatorSelector, timeout }) => {
                const start = performance.now();
                return new Promise(resolve => {
                    const checkText = () => {
                        const element = document.querySelector(locatorSelector);
                        if (element) {
                            const text = element.innerText || element.textContent;
                            if (text.includes('New Born') || performance.now() - start > timeout) {
                                resolve(text); // Resolve with the current text
                            } else {
                                requestAnimationFrame(checkText); // Recheck on the next frame
                            }
                        } else {
                            resolve('<-->'); // Resolve with placeholder if element disappears
                        }
                    };
                    checkText(); // Start checking
                });
            }
            """,
            {"locatorSelector": ".qpz9NG90l1gorDZORgIn.OSVhhsHh74o0GLnLTmrt", "timeout": 1000}
        )
        # print(status)

        date_xp = "//div[text()='Registration Date']/following-sibling::div"
        self.wait_for_updated_content_direct(page, date_xp)
        date = \
        page.wait_for_selector("//div[text()='Registration Date']/following-sibling::div").text_content().split()[0]

        date_str = date + "a"  # to convert to string

        if current_status == 'Preauthorization Queried' or current_status == 'Pre-Authorization Queried':
            time.sleep(1)
            amount = page.wait_for_selector(
                "//div[p[normalize-space()='Total payable amount (after incentives) :']]/following-sibling::div/p").text_content()
            # main treatment already opened clicking treatment plan
            page.wait_for_selector(
                "//div[contains(text(),'Treatment Plan')]/parent::div/following-sibling::div//button").click()
            # print("clicked treat plan")
            # show more click
            page.wait_for_selector("//span[contains(text(),'Show More')]").click()
            # depart
            depart = page.wait_for_selector(
                "//span[contains(text(),'Show Less')]/parent::p/parent::td/preceding-sibling::td[1]").text_content()
            # procedure SAME FOR BOTH
            procedure = page.wait_for_selector("//span[contains(text(),'Show Less')]/parent::p").text_content()
            # print(procedure)
            # click Finance to close it which is already open
            page.wait_for_selector("//h4[normalize-space()='Finance']/parent::button").click()

        elif current_status == 'Claim Queried':
            time.sleep(1)
            amount = page.wait_for_selector(
                "//div[p[normalize-space()='Total payable amount (after incentives) :']]/following-sibling::div/p").text_content()
            # main treatment
            page.wait_for_selector("//h4[normalize-space()='Treatment']/parent::button").click()
            # treatment detail
            page.wait_for_selector("//span[contains(text(),'Treatment Details')]/parent::button").click()
            # show more click
            page.wait_for_selector("//span[contains(text(),'Show More')]").click()
            # department
            depart = page.wait_for_selector(
                "//span[contains(text(),'Show Less')]/parent::p/parent::div/parent::div/preceding-sibling::div/div").text_content()
            # print(depart)
            depart = depart.split(".")[1]  # 1.Obstetrics & Gynaecology
            # print(depart)
            # procedure SAME FOR BOTH
            procedure = page.wait_for_selector("//span[contains(text(),'Show Less')]/parent::p").text_content()
            # print(procedure)

        elif current_status == 'Under Treatment':
            # wait for amount to load
            amount_xp = "//div[normalize-space()='Total Preauth Approved Amount']/following-sibling::div"
            self.wait_for_updated_content_direct(page, amount_xp)
            amount = page.wait_for_selector(
                "//div[normalize-space()='Total Preauth Approved Amount']/following-sibling::div").text_content()
            # main treatment
            page.wait_for_selector("//h4[normalize-space()='Treatment']/parent::button").click()
            # treatment detail
            page.wait_for_selector("//span[contains(text(),'Treatment Plan')]/parent::button").click()
            # show more click
            page.wait_for_selector("//span[contains(text(),'Show More')]").click()
            # depart
            depart = page.wait_for_selector(
                "//span[contains(text(),'Show Less')]/parent::p/parent::td/preceding-sibling::td[2]").text_content()
            # procedure SAME FOR BOTH
            procedure = page.wait_for_selector("//span[contains(text(),'Show Less')]/parent::p").text_content()
            # print("Under treat ", procedure)
            # going homepage
            page.wait_for_selector("//p[contains(text(),'Home')]/preceding-sibling::*[name()='svg']").click()
            page.wait_for_load_state("networkidle")
            time.sleep(2)

        page.wait_for_load_state("networkidle")
        time.sleep(1.5)
        # print(card, name, case_number, date, depart, procedure, status)
        # day, mon, year = date.split('/')
        date_by_datetime = datetime.datetime.strptime(date,'%d/%m/%Y').date()
        today_by_datetime = datetime.datetime.today().date()
        days_diff = today_by_datetime - date_by_datetime
        pending_days = days_diff.days
        pending_days = str(pending_days)

        # modifying / renaming for the explanation, simplicity and understanding
        age_and_sex = status
        remark = "Discharge Pending"


        if is_query_question_required:

            # click CASE LOG button side panel
            page.wait_for_selector("//button[normalize-space()='Case log']").click()

            # TRYING TO GET THE QUERY FROM HERE - CASE LOG
            try:
                try:  # clicking SHOW MORE
                    page.wait_for_selector(
                        "//*[name()='circle' and @id='bg-icon']/ancestor::something/parent::div/parent::div/parent::div/div[2]/div[last()]/div[2]/div[3]//span[contains(text(),'...Show More')]").click()
                    # last_query_question_xp containing SHOW LESS
                    last_query_question_xp = "//*[name()='circle' and @id='bg-icon']/ancestor::something/parent::div/parent::div/parent::div/div[2]/div[last()]/div[2]/div[3]"

                    # question = "this is demo test"
                    question = page.wait_for_selector(last_query_question_xp).text_content()
                    # print(question)
                    # close cross button
                except TimeoutError as err:
                    print(err)
                finally:
                    page.wait_for_selector("//*[name()='path' and @id='cross-icon']").click()

            except TimeoutError as err:
                # click Finance
                page.wait_for_selector("//h4[normalize-space()='Finance']/parent::button").click()
                # select the query chat option and click it to open chat window
                page.wait_for_selector("(//img[@data-tip='Chat'])[last()]").click()
                # getting question - last question
                question = page.wait_for_selector(
                    "(//div[contains(@class,'react-draggable')]//strong)[last()]").text_content()
                # print(question)
                # close button
                page.wait_for_selector("(//div[contains(@class,'react-draggable')]//img)[2]").click()

            page.wait_for_load_state("networkidle")
            time.sleep(2)
            # going homepage
            page.wait_for_selector("//p[contains(text(),'Home')]/preceding-sibling::*[name()='svg']").click()
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            remark = question
        return card, name, case_number, date_str, depart, procedure, age_and_sex, current_status, amount, pending_days, remark





