from ehospital_proper.colour_print_ehosp import ColourPrint
from svnsssy.svns_pages.first_page_svsn import AyushmanApp

def main_app ():
    app = AyushmanApp()

    page = app.get_desired_page('Shaheed Veer Narayan Singh Ayushman Swasthya Yojna')

    all_name_and_id_dict = app.get_emp_data_from_excel(
                            r"G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto_ver_3.xlsx",
                            'Sheet3')
    try:

    # '''
        all_emp_retrieved_data = []
        for each_name, each_id in all_name_and_id_dict.items():  # retrieve_incentive_data_from_dk(page,'N55171003')
            data = dict()
            data['name_emp'] = each_name
            data2 = app.retrieve_incentive_data_from_dk(page, employees_data_emp_ip=each_id)
            print(each_name, data2)
            data.update(data2)
            all_emp_retrieved_data.append(data)

            print(all_emp_retrieved_data)
            # '''
        # inserting all the data to sql
        # app.temp_inc_data_sql(all_emp_retrieved_data)
    except Exception as e:
        print(ColourPrint.print_bg_red('Error'))
        print(e)
        print(ColourPrint.print_bg_red('Error'))
        print("UPDATING THE THE DATABASE")
        app.temp_inc_data_sql(all_emp_retrieved_data)

        # for single person details retrieve
        # app.retrieve_incentive_data_from_dk(page,'nnnnnn')

main_app()