from tms_playwright.discharge_to_be_done.detail_list_getter_all import AllListGenerator

if __name__ == "__main__":
    AllListGenerator().main_all_list_getter_tms(user_id='CHH008134',
                                                is_pre_auth_list=True,
                                                is_claim_list=True,
                                                is_dis_list=True)
