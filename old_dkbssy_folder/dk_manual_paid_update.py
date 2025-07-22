import os, csv
import sqlite3

import openpyxl

class ManualUpdate:
    list_of_payment_done = '''


    '''.split('\n')

    def extract_excel(self):
        wb = openpyxl.load_workbook(r"G:\My Drive\GdrivePC\Hospital\RSBY\New\down\bb.xlsx")
        ws = wb.active
        row_data = ws.iter_rows(min_col=2, max_col=4, min_row=3)
        all_row_values = []
        for row in row_data:
            row_values = [cell_value.value for cell_value in row]
            # print(row_values)
            all_row_values.append(row_values)
        # print(all_row_values)
        # listoflist
        return all_row_values

    def status_and_update_date(self, pay_done_case_numbers):
        require_incentive_data_lol = []
        excel_datas = self.extract_excel()  # ['CASE/PS5/HOSP22G146659/CB5780624', 'ACO Approved', '11/07/2024 12:58:17'],]
        for each_paid in pay_done_case_numbers:
            for each_row_values in excel_datas:
                if each_paid in each_row_values:
                    case_num = each_row_values[0]
                    status_is = each_row_values[1]
                    time_is = each_row_values[2]
                    # print(case_num, status_is, time_is)

            procedure, list_of_list = self.get_file_details(each_paid)
            # case_number_text, status_text, last_updated_text, procedure_text, list_of_list
            # print(case_num, status_is, time_is, procedure, list_of_list)
            require_incentive_data_lol.append([case_num, status_is, procedure, time_is, list_of_list])
        # print(require_incentive_data_lol)
        return require_incentive_data_lol

    def get_file_details(self, case_number):
        file_last_name = case_number.split('/')[-1]
        # print(file_last_name)
        original_path = r"G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_Entered_New\CK6333177.csv"
        directory = os.path.dirname(original_path)
        new_file_last_name = f'{file_last_name}.csv'
        new_file_name_path = os.path.join(directory, new_file_last_name)
        # print(new_file_name_path)
        with open(new_file_name_path, 'r', newline='') as reading_file:
            entry_values = list(csv.reader(reading_file, delimiter=",", quotechar='"'))
            # print(entry_values)
            # print(entry_values[0], 'Payment Done', "last_updated_text", entry_values[3], entry_values[6:])
            return entry_values[0][3], entry_values[0][6:]

    def sql_insert_payment_done(self, case_number_text, status_text, procedure_text, last_updated_text, list_of_list):
        # Connect to SQLite database
        conn = sqlite3.connect(r'G:\My Drive\GdrivePC\Hospital\RSBY\New\incentiveDatabase_2.db')
        cursor = conn.cursor()
        # Step 1: Insert case number and retrieve its ID
        cursor.execute('''
                INSERT INTO case_num_t (case_number, updated_time, inc_procedure, inc_status)
                SELECT ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT 1 FROM case_num_t WHERE case_number = ?)
                ''', (case_number_text, last_updated_text, procedure_text, status_text, case_number_text))
        conn.commit()

        cursor.execute('SELECT id_case_num, updated_time FROM case_num_t WHERE case_number = ?', (case_number_text,))
        result = cursor.fetchone()
        case_num_id = result[0]

        # Step 3: Prepare to insert new records
        distribution_data = []
        for entry in list_of_list:
            category_number = None
            employee_code = entry.split('@')[0]  # # it is name
            print(employee_code)
            incentive_amount = entry.split('@')[1]

            # Retrieve employee ID from emp_detail_t using employee_code
            cursor.execute('SELECT SN FROM emp_detail_t WHERE name_emp = ?', (employee_code,))
            emp_id = cursor.fetchone()
            if not emp_id:
                raise ValueError(f"Employee with code {employee_code} not found in emp_detail_t.")
            emp_id = emp_id[0]

            # Prepare data for batch insertion
            distribution_data.append((case_num_id, category_number, emp_id, incentive_amount))

        # Insert data into distribution_t in a single transaction
        cursor.executemany('''
            INSERT INTO distribution_t (d_case_num, d_emp_categ, d_emp_code, d_inc_amt)
            VALUES (?, ?, ?, ?)
            ''', distribution_data)
        conn.commit()

        # Close the connection
        conn.close()


test = ManualUpdate()
pay_done_case_numbers = '''CASE/PS5/HOSP22G146659/CKAAAAAA'''.split('\n')
data_to_add = test.status_and_update_date(pay_done_case_numbers)
for i in data_to_add:
    case_number_text, status_text, procedure_text, last_updated_text, list_of_list = i
    test.sql_insert_payment_done(case_number_text, status_text, procedure_text, last_updated_text, list_of_list)
    print('====================================================')

