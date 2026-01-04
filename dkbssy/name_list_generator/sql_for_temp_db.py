import datetime
import sqlite3
import sys
# from pypdf.constants import ColorSpaces

from dkbssy.utils.colour_prints import ColourPrint


# data = [
#     ['CASE/PS6/HOSP22G146659/CK7130670', ('DR.ANMOL MADHUR MINZ', '04170140656', 1, 3.1571), ('AVINASH MESHRAM', 66170010023, 1, 3.1571), ('RAVIKANT JATWAR', '04170140099', 1, 3.1571), ('Dr. Durga Shankar Patel', 66170010344, 1, 3.1571), ('Dr. Rakesh Kumar Verma', '02530010055', 1, 3.1571), ('Dr. Gopal Singh Kanwer', 11170010478, 1, 3.1571), ('Dr. Aditya Siodiya', '09530010327', 1, 3.1571), ('Dr. Ashutosh Kumar', 'DME55173188', 2, 22.1), ('DR RAKESH KUMAR AGRAWAL', '05170040053', 2, 22.1), ('Reena Nayak', 'DME55172439', 2, 22.1), ('Rajesh Kumar', '05530010065', 2, 22.1), ('Dushyant Chandra', '05530010031', 2, 22.1), ('Dr. Sumit Gupta', 'DME55173185', 2, 22.1), ('Shende Pranali kisandas', 'DME55172441', 2, 22.1), ('HANISH KUMAR CHOWDA', '04170140518', 2, 22.1), ('Dr. Awadh Sahu', 'DME55173201', 2, 22.1), ('Dr. Deepa Janghel', '05530010026', 2, 22.1), ('Dr. Veenapani Mire', '05530010079', 2, 22.1), ('GHANSHYAM SINGH JATRA', '05170011289', 2, 22.1), ('Vibha Tandon', '05530010013', 2, 22.1), ('Dr. manoj Kumar', '05530010029', 2, 22.1), ('MAHENDRA KUMAR EYE', '05170011797', 3, 7.8), ('DINESHWAR DINKAR', '05170020193', 3, 7.8), ('ACHCHHE KUMAR PATLEY', '04170150173', 3, 7.8), ('Smt. Pinky Singh', '06170100054', 3, 7.8), ('dinesh kumar patel', '09530010377', 3, 7.8), ('Haricharan Jangde', '05170010396', 3, 7.8), ('Smt. Reena Verma', 'AI55170024', 3, 7.8), ('Santosh Kumar Singh', 'AI55170030', 3, 7.8), ('SMT DURGESHWARI KARSH', '06170050083', 3, 7.8), ('Geeta patel', 'J55172863', 3, 7.8), ('Pratima Sahu', 'N5517593', 3, 7.8), ('Shri Dildar Sahish', '05170020054', 3, 7.8), ('ARUN KUMAR KANWAR', '07170021387', 3, 7.8), ('Smt.Bhagwati Koshle', '09170010257', 3, 7.8), ('Shri Sushil kumar miri', '03170010366', 3, 7.8), ('SHIVSHANKAR SINGH KANWAR', '05170060099', 3, 7.8), ('Shri C.L. Dixena', '05170020117', 3, 7.8), ('Dr. Priyanka Ekka', '05530010030', 4, 198.9), ('Dr Ankita Kapoor', '05530010028', 4, 198.9), ('Dr. V.Agrawal', '05170020043', 4, 198.9), ('DR ARUNIKA SISODIYA', '05170020182', 4, 198.9), ('Dr.Sumit Gupta', '05170020187', 4, 198.9), ('ARTI AGRAWAL', 66170020533, 7, 5.304), ('OM KUMARI', 'N5517024', 7, 5.304), ('AMRAN TINA', 'N5517039', 7, 5.304), ('Sanjay Das Manikpuri', 'N5517599', 7, 5.304), ('Sanjaya Kumar Tiwari', 'N5517515', 7, 5.304), ('Radhe Shyam Kashyap', 'AI55170022', 7, 5.304), ('Ku.Jyoti Gual', '05170020143', 7, 5.304), ('ku Kiran Sahu', '05170020161', 7, 5.304), ('Smt. Varnita Zilkar', 15170200084, 7, 5.304), ('Narendra Kumar Kanwar', '04170140534', 7, 5.304), ('Martina Vishwas', '05170020150', 7, 5.304), ('Neelam Kanwar', '08170040064', 7, 5.304), ('Ku. Sandhya Nair', '05170020124', 7, 5.304), ('SAROJ RATHOR', '09170160077', 7, 5.304), ('Amarjeet Kour', 19170040056, 7, 5.304), ('Anita Yadav', 22170040038, 7, 5.304), ('NEELIMA NISHAD', '05170050074', 7, 5.304), ('Ku.Marget Bishwash', '05170020153', 7, 5.304), ('Smt.Seema Rani Lajras', '05170020063', 7, 5.304), ('Smt.DIVYA ALKA TOPPO', '04170060068', 7, 5.304), ('Rajni Kiran Kispotta', 11170010433, 7, 5.304), ('vinita tigga', 12170050188, 7, 5.304), ('rajendra kumar', '04170120033', 7, 5.304), ('Shri Santo Mitra', '05170020133', 7, 5.304), ('kirti', 'N5517866', 7, 5.304), ('Mr. BALDEV SINGH', 'N5517085', 8, 2.652), ('MAHENDRA KUMAR HOUSE', 'N55171003', 8, 2.652), ('mohendra kumar janardan', '04170150084', 8, 2.652), ('RAJESH', 'N5517032', 8, 2.652), ('RAMANAND', 'N5517042', 8, 2.652), ('KUMARI SHREMATI', 'N5517056', 8, 2.652), ('Mr. MONESHWAR CHANDRA RATHIYA', 'N5517083', 8, 2.652), ('Mr .AVINASH KUMAR BANJARE', 'N5517084', 8, 2.652), ('KU. PRIYA', 'N5517136', 8, 2.652), ('BUDHAN SINGH UIKEY', 'N5517073', 8, 2.652), ('Mrs. ANAMIKA', 'N5517055', 8, 2.652), ('Mrs. BASANTI RATHIYA', 'N5517028', 8, 2.652), ('MONGARA TANDAN', '04170150044', 8, 2.652), ('L.Kondiya', '05170020107', 8, 2.652), ('Smt. Achamma Bai', '05170020090', 8, 2.652), ('PUSHPENDRA KUMAR', '05170020184', 8, 2.652), ('K. Damodar', '05170020110', 8, 2.652), ('Panch Ram Nirmalkar', '05170020091', 8, 2.652), ('Bal Chainya', '05170020105', 8, 2.652), ('AAKANKSHA', 'N5517610', 8, 2.652), ('SUNITA RATHORE', 'N5517613', 8, 2.652), ('V. Kondiya', '05170020092', 8, 2.652), ('Shri S.N.Shriwas', '05170020100', 8, 2.652), ('Shri Shiv Kumar Sarthi', '05170020084', 8, 2.652), ('Komal Dewangan', 'N5517589', 8, 2.652), ('Ashok Kumar Lakhera', 'N5517569', 9, 15.7857), ('YOGESH KUMAR THAWAIT', '05170020166', 9, 15.7857), ('Yamini Verma', 'DME55173200', 9, 15.7857), ('SANGEETA', 'DME55173037', 9, 15.7857), ('KUMARI JYOTI LAHRE', 'DME55173036', 9, 15.7857), ('SUMITRA KURREY', 'J55173309', 9, 15.7857), ('Mr. Kiran Kumar Sahu', 'J55172798', 9, 15.7857)], ['CASE/PS6/HOSP22G146659/CK7130699', ('DR.ANMOL MADHUR MINZ', '04170140656', 1, 3.1571), ('AVINASH MESHRAM', 66170010023, 1, 3.1571), ('RAVIKANT JATWAR', '04170140099', 1, 3.1571), ('Dr. Durga Shankar Patel', 66170010344, 1, 3.1571), ('Dr. Rakesh Kumar Verma', '02530010055', 1, 3.1571), ('Dr. Gopal Singh Kanwer', 11170010478, 1, 3.1571), ('Dr. Aditya Siodiya', '09530010327', 1, 3.1571), ('Dr. Ashutosh Kumar', 'DME55173188', 2, 22.1), ('DR RAKESH KUMAR AGRAWAL', '05170040053', 2, 22.1), ('Reena Nayak', 'DME55172439', 2, 22.1), ('Rajesh Kumar', '05530010065', 2, 22.1), ('Dushyant Chandra', '05530010031', 2, 22.1), ('Dr. Sumit Gupta', 'DME55173185', 2, 22.1), ('Shende Pranali kisandas', 'DME55172441', 2, 22.1), ('HANISH KUMAR CHOWDA', '04170140518', 2, 22.1), ('Dr. Awadh Sahu', 'DME55173201', 2, 22.1), ('Dr. Deepa Janghel', '05530010026', 2, 22.1), ('Dr. Veenapani Mire', '05530010079', 2, 22.1), ('GHANSHYAM SINGH JATRA', '05170011289', 2, 22.1), ('Vibha Tandon', '05530010013', 2, 22.1), ('Dr. manoj Kumar', '05530010029', 2, 22.1), ('MAHENDRA KUMAR EYE', '05170011797', 3, 7.8), ('DINESHWAR DINKAR', '05170020193', 3, 7.8), ('ACHCHHE KUMAR PATLEY', '04170150173', 3, 7.8), ('Smt. Pinky Singh', '06170100054', 3, 7.8), ('dinesh kumar patel', '09530010377', 3, 7.8), ('Haricharan Jangde', '05170010396', 3, 7.8), ('Smt. Reena Verma', 'AI55170024', 3, 7.8), ('Santosh Kumar Singh', 'AI55170030', 3, 7.8), ('SMT DURGESHWARI KARSH', '06170050083', 3, 7.8), ('Geeta patel', 'J55172863', 3, 7.8), ('Pratima Sahu', 'N5517593', 3, 7.8), ('Shri Dildar Sahish', '05170020054', 3, 7.8), ('ARUN KUMAR KANWAR', '07170021387', 3, 7.8), ('Smt.Bhagwati Koshle', '09170010257', 3, 7.8), ('Shri Sushil kumar miri', '03170010366', 3, 7.8), ('SHIVSHANKAR SINGH KANWAR', '05170060099', 3, 7.8), ('Shri C.L. Dixena', '05170020117', 3, 7.8), ('Dr. Priyanka Ekka', '05530010030', 4, 198.9), ('Dr Ankita Kapoor', '05530010028', 4, 198.9), ('Dr. V.Agrawal', '05170020043', 4, 198.9), ('DR ARUNIKA SISODIYA', '05170020182', 4, 198.9), ('Dr.Sumit Gupta', '05170020187', 4, 198.9), ('ARTI AGRAWAL', 66170020533, 7, 5.304), ('OM KUMARI', 'N5517024', 7, 5.304), ('AMRAN TINA', 'N5517039', 7, 5.304), ('Sanjay Das Manikpuri', 'N5517599', 7, 5.304), ('Sanjaya Kumar Tiwari', 'N5517515', 7, 5.304), ('Radhe Shyam Kashyap', 'AI55170022', 7, 5.304), ('Ku.Jyoti Gual', '05170020143', 7, 5.304), ('ku Kiran Sahu', '05170020161', 7, 5.304), ('Smt. Varnita Zilkar', 15170200084, 7, 5.304), ('Narendra Kumar Kanwar', '04170140534', 7, 5.304), ('Martina Vishwas', '05170020150', 7, 5.304), ('Neelam Kanwar', '08170040064', 7, 5.304), ('Ku. Sandhya Nair', '05170020124', 7, 5.304), ('SAROJ RATHOR', '09170160077', 7, 5.304), ('Amarjeet Kour', 19170040056, 7, 5.304), ('Anita Yadav', 22170040038, 7, 5.304), ('NEELIMA NISHAD', '05170050074', 7, 5.304), ('Ku.Marget Bishwash', '05170020153', 7, 5.304), ('Smt.Seema Rani Lajras', '05170020063', 7, 5.304), ('Smt.DIVYA ALKA TOPPO', '04170060068', 7, 5.304), ('Rajni Kiran Kispotta', 11170010433, 7, 5.304), ('vinita tigga', 12170050188, 7, 5.304), ('rajendra kumar', '04170120033', 7, 5.304), ('Shri Santo Mitra', '05170020133', 7, 5.304), ('kirti', 'N5517866', 7, 5.304), ('Mr. BALDEV SINGH', 'N5517085', 8, 2.652), ('MAHENDRA KUMAR HOUSE', 'N55171003', 8, 2.652), ('mohendra kumar janardan', '04170150084', 8, 2.652), ('RAJESH', 'N5517032', 8, 2.652), ('RAMANAND', 'N5517042', 8, 2.652), ('KUMARI SHREMATI', 'N5517056', 8, 2.652), ('Mr. MONESHWAR CHANDRA RATHIYA', 'N5517083', 8, 2.652), ('Mr .AVINASH KUMAR BANJARE', 'N5517084', 8, 2.652), ('KU. PRIYA', 'N5517136', 8, 2.652), ('BUDHAN SINGH UIKEY', 'N5517073', 8, 2.652), ('Mrs. ANAMIKA', 'N5517055', 8, 2.652), ('Mrs. BASANTI RATHIYA', 'N5517028', 8, 2.652), ('MONGARA TANDAN', '04170150044', 8, 2.652), ('L.Kondiya', '05170020107', 8, 2.652), ('Smt. Achamma Bai', '05170020090', 8, 2.652), ('PUSHPENDRA KUMAR', '05170020184', 8, 2.652), ('K. Damodar', '05170020110', 8, 2.652), ('Panch Ram Nirmalkar', '05170020091', 8, 2.652), ('Bal Chainya', '05170020105', 8, 2.652), ('AAKANKSHA', 'N5517610', 8, 2.652), ('SUNITA RATHORE', 'N5517613', 8, 2.652), ('V. Kondiya', '05170020092', 8, 2.652), ('Shri S.N.Shriwas', '05170020100', 8, 2.652), ('Shri Shiv Kumar Sarthi', '05170020084', 8, 2.652), ('Komal Dewangan', 'N5517589', 8, 2.652), ('Ashok Kumar Lakhera', 'N5517569', 9, 15.7857), ('YOGESH KUMAR THAWAIT', '05170020166', 9, 15.7857), ('Yamini Verma', 'DME55173200', 9, 15.7857), ('SANGEETA', 'DME55173037', 9, 15.7857), ('KUMARI JYOTI LAHRE', 'DME55173036', 9, 15.7857), ('SUMITRA KURREY', 'J55173309', 9, 15.7857), ('Mr. Kiran Kumar Sahu', 'J55172798', 9, 15.7857)]
# ]
#
#
# temp_db = r"G:\My Drive\GdrivePC\Hospital\RSBY\New\down\temp_incen.db"

class SqlForTemp:
    def __init__(self, temp_db_path):
        self.temp_db_path = temp_db_path
        self.conn = sqlite3.connect(temp_db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def insert_each_case_num_data (self, each_data:list) -> None:  # each data = ['CASE/PS6/HOSP22G146659/CK7130670', ('DR.ANMOL MADHUR MINZ', '04170140656', 1, 3.1571), ('AVINASH MESHRAM', 66170010023, 1, 3.1571), ('RAVIKANT JATWAR', '04170140099', 1, 3.1571), ('Dr. Durga Shankar Patel'...]
        """
        inserting the data to database
        :param each_data: incentive details of each case number with each  employee amount data
        :return: None
        """
        case_number = each_data[0]

        modified_date = datetime.datetime.now().isoformat()

        self.cursor.execute(
            """
            INSERT INTO case_num_table (cnt_case_number, cnt_modified_date)
            VALUES (?, ?)
            ON CONFLICT(cnt_case_number)
            DO UPDATE SET cnt_modified_date = excluded.cnt_modified_date
            """,
            (case_number, modified_date)
        )

    def insert_all_case_num_data(self, all_data):

        all_case_number_distribution_data = []
        counting = 0
        for each_data in all_data:
            # step 1 adding the case number

            # print(each_data)
            self.insert_each_case_num_data(each_data=each_data)
            self.conn.commit()

            # step 2 fetching the case number id
            'fetching the id of case number'
            _id_of_case_in_db = self.fetch_the_case_num_id_from_db(each_data=each_data)
            ColourPrint.print_pink(f'id of the {_id_of_case_in_db}')

            # # --- BEFORE DELETE: Print matching rows ---
            # self.cursor.execute('''
            #     SELECT * FROM distri_table WHERE d_case_num_id = ?
            # ''', (_id_of_case_in_db,))
            # rows_before = self.cursor.fetchall()
            # ColourPrint.print_yellow(f'Rows before deletion:\n{rows_before}')

            # step 3 deleting the old record of same case number
            self.cursor.execute(
                '''
                DELETE FROM distri_table WHERE d_case_num_id = ?
                ''', (_id_of_case_in_db,)
            )
            # self.conn.commit()


            # # --- AFTER DELETE: Confirm deletion ---
            # self.cursor.execute('''
            #     SELECT * FROM distri_table WHERE d_case_num_id = ?
            # ''', (_id_of_case_in_db,))
            # rows_after = self.cursor.fetchall()
            # ColourPrint.print_green(f'Rows after deletion (should be empty):\n{rows_after}')


            # STEP 4 updating the record again after deleting

            # each data = ['CASE/PS6/HOSP22G146659/CK7130670', ('DR.ANMOL MADHUR MINZ', '04170140656', 1, 3.1571), ('AVINASH MESHRAM', 66170010023, 1, 3.1571), ('RAVIKANT JATWAR', '04170140099', 1, 3.1571), ('Dr. Durga Shankar Patel'...]
            # each_employee_data = ('DR.ANMOL MADHUR MINZ', '04170140656', 1, 3.1571)

            for each_employee_data in each_data[1:]:  # skipping case number
                counting+=1
                # print('Counting of entry: ', counting)
                'fetching the id of each employee'
                id_of_emp_in_db = self.fetch_id_of_employee_from_db(each_emp_data=each_employee_data)
                # print('-------------')
                _emp_category = each_employee_data[2]
                _emp_amount = each_employee_data[3]
                all_case_number_distribution_data.append((_id_of_case_in_db,id_of_emp_in_db,_emp_category,_emp_amount))

        # print(f'{all_case_number_distribution_data=}')

        seen = set()
        dupes = []

        for row in all_case_number_distribution_data:
            key = (row[0], row[1], row[2])
            if key in seen:
                dupes.append(key)
            else:
                seen.add(key)

        if dupes:
            print("⚠️ Duplicate entries within the data being inserted:")
            for d in dupes[:10]:
                print(d)

        # # Step 5.0 to check errors when there occurs in executemany
        # for row in all_case_number_distribution_data:
        #     try:
        #         self.cursor.execute(
        #             "INSERT INTO distri_table (d_case_num_id, d_emp_id, d_category, d_amount) VALUES (?, ?, ?, ?)", row)
        #     except Exception as e:
        #         print(f"Error with row: {row}")
        #         print(f"Exception: {e}")

        # STEP 5 Insert in batch insertion
        self.cursor.executemany(
            '''INSERT INTO distri_table (d_case_num_id, d_emp_id, d_category, d_amount)
            VALUES (?,?,?,?)
            ''', all_case_number_distribution_data
        )

        # sys.exit("Manually stop")
        self.conn.commit()




    def fetch_the_case_num_id_from_db(self, each_data:list):
        """
        getting the case number ID in the database
        :param each_data: incentive details of each case nu,ber with each  employee amount data
        :return: integer ID
        """
        case_number = each_data[0]
        self.cursor.execute('''
            SELECT id_case_num FROM case_num_table
            WHERE cnt_case_number = ?            
            ''', (case_number,))
        result = self.cursor.fetchone()
        id_of_case_num = result[0]
        # print(result, id_of_case_num)
        return id_of_case_num

    def fetch_id_of_employee_from_db(self, each_emp_data):
        """
        getting the ID of the employee in the database
        :param each_emp_data: incentive details of each case nu,ber with each  employee amount data
        :return: integer ID
        """
        # each data = ['CASE/PS6/HOSP22G146659/CK7130670', ('DR.ANMOL MADHUR MINZ', '04170140656', 1, 3.1571), ('AVINASH MESHRAM', 66170010023, 1, 3.1571), ('RAVIKANT JATWAR', '04170140099', 1, 3.1571), ('Dr. Durga Shankar Patel'...]
        # each_emp_data = ('DR.ANMOL MADHUR MINZ', '04170140656', 1, 3.1571)
        _employee_name = each_emp_data[0]
        _employee_code = each_emp_data[1]
        # print(_employee_name,_employee_code)
        self.cursor.execute(
            ''' SELECT id_emp_table FROM emp_table
            WHERE emp_tab_emp_code = ?
            ''', (_employee_code,)
        )

        result = self.cursor.fetchone()
        if not result:
            raise ValueError(f"Employee with code {_employee_name}, {_employee_code} not found in emp_detail_t.\ntemp_db_path = {self.temp_db_path}")

        _id_of_emp= result[0]
        # print(f'{_id_of_emp=}')
        return _id_of_emp

    def fetch_updated_amount(self):
        query = """
            SELECT 
                e.emp_tab_emp_code AS emp_code,
                e.emp_tab_db1_amount + COALESCE(SUM(d.d_amount), 0) AS new_amount
            FROM emp_table e
            LEFT JOIN distri_table d ON d.d_emp_id = e.id_emp_table
            GROUP BY e.id_emp_table, e.emp_tab_emp_name, e.emp_tab_emp_code;
            """

        self.cursor.execute(query)
        results = self.cursor.fetchall()

        # Returns a list of tuples: [(emp_code, new_amount), ...]
        return results




# sql_temp_object = SqlForTemp(temp_db_path=temp_db)
# sql_temp_object.insert_all_case_num_data(data)
#
#
# sql_temp_object.close()
