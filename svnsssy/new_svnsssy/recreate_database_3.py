# recreate database 3 by csv saves

import sqlite3
import time, datetime
import openpyxl
from svnsssy.new_svnsssy.async_dkbssy import indent_json_print


def load_sql():
    conn = sqlite3.connect(r"G:\My Drive\GdrivePC\Hospital\RSBY\New\incentiveDatabase_3.db")
    cursor =conn.cursor()
    cursor.execute('SELECT id_emp, name_emp FROM emp_detail_table')
    data = cursor.fetchall()
    # print(data)
    mapper = {j:i for i,j in data}

    # print(mapper)
    # indent_json_print(mapper)

    cursor.execute('SELECT id_case_num, case_number FROM case_num_table')
    c_data = cursor.fetchall()
    c_data_dict = {j:i for i, j in c_data}
    # print(c_data_dict)

    return mapper, c_data_dict




def each_row_process(row, name_map, case_num_map):
    # ['CK7330927.csv', 'CASE/PS6/HOSP22G146659/CK7330927', 2655, 'General Medicine', 'Acute excaberation of COPD', datetime.datetime(2023, 12, 19, 0, 0), 'Savresh Kumar', 'Dr. Gopal Singh Kanwer@3.7934285714285716#1', 'Dr. Durga Shankar Patel@3.7934285714285716#1', 'DR.ANMOL MADHUR MINZ@3.7934285714285716#1', 'Dr. Aditya Siodiya@3.7934285714285716#1', 'Dr. Rakesh Kumar Verma@3.7934285714285716#1', 'RAVIKANT JATWAR@3.7934285714285716#1', 'AVINASH MESHRAM@3.7934285714285716#1', 'GHANSHYAM SINGH JATRA@26.554000000000002#2', 'DR RAKESH KUMAR AGRAWAL@26.554000000000002#2', 'Dr. Awadh Sahu@26.554000000000002#2', 'Dr. Deepa Janghel@26.554000000000002#2', 'Dushyant Chandra@26.554000000000002#2', 'Rajesh Kumar@26.554000000000002#2', 'Dr. Veenapani Mire@26.554000000000002#2', 'Reena Nayak@26.554000000000002#2', 'HANISH KUMAR CHOWDA@26.554000000000002#2', 'Vibha Tandon@26.554000000000002#2', 'Shende Pranali kisandas@26.554000000000002#2', 'Dr. Ashutosh Kumar@26.554000000000002#2', 'Dr. Sumit Gupta@26.554000000000002#2', 'Dr. manoj Kumar@26.554000000000002#2', 'ACHCHHE KUMAR PATLEY@10.6216#3', 'Geeta patel@10.6216#3', 'Pratima Sahu@10.6216#3', 'Haricharan Jangde@10.6216#3', 'Shri Dildar Sahish@10.6216#3', 'Smt. Reena Verma@10.6216#3', 'Santosh Kumar Singh@10.6216#3', 'Shri Sushil kumar miri@10.6216#3', 'Shri C.L. Dixena@10.6216#3', 'SHIVSHANKAR SINGH KANWAR@10.6216#3', 'SMT DURGESHWARI KARSH@10.6216#3', 'ARUN KUMAR KANWAR@10.6216#3', 'Smt.Bhagwati Koshle@10.6216#3', 'dinesh kumar patel@10.6216#3', 'MAHENDRA KUMAR@10.6216#3', 'Shashikant Bhaskar@1194.93#4', 'Dr. Anshul lal@265.54#5', 'Smt. Varnita Zilkar@6.927130434782609#7', 'Amarjeet Kour@6.927130434782609#7', 'SMT. KAVITA KOSHLE@6.927130434782609#7', 'chandrakanta kashyap@6.927130434782609#7', 'Sushma Singh@6.927130434782609#7', 'Shri D.R. Bhaskar@6.927130434782609#7', 'Shri Santo Mitra@6.927130434782609#7', 'Kiran Lahre@6.927130434782609#7', 'Smt. Anita David@6.927130434782609#7', 'Smt. Nageshwari Ogre@6.927130434782609#7', 'Ku. Sandhya Nair@6.927130434782609#7', 'Smt.Seema Patel@6.927130434782609#7', 'Ku.Jyoti Gual@6.927130434782609#7', 'Martina Vishwas@6.927130434782609#7', 'ku Kiran Sahu@6.927130434782609#7', 'KU ARCHANA TOPPO@6.927130434782609#7', 'Neelam Kanwar@6.927130434782609#7', 'SAROJ RATHOR@6.927130434782609#7', 'Anita Yadav@6.927130434782609#7', 'ANJU JAISWAL@6.927130434782609#7', 'Bhanu Priya Chauhan@6.927130434782609#7', 'Jyoti Porte@6.927130434782609#7', 'Narendra Kumar Kanwar@6.927130434782609#7', 'RAJESH@7.966200000000001#8', 'RAMANAND@7.966200000000001#8', 'KUMARI SHREMATI@7.966200000000001#8', 'Mr. MONESHWAR CHANDRA RATHIYA@7.966200000000001#8', 'Mr .AVINASH KUMAR BANJARE@7.966200000000001#8', 'KU. PRIYA@7.966200000000001#8', 'Mrs. BASANTI RATHIYA@7.966200000000001#8', 'Mrs. ANAMIKA@7.966200000000001#8', 'BUDHAN SINGH UIKEY@7.966200000000001#8', 'K. Damodar@7.966200000000001#8', 'Mr. Kiran Kumar Sahu@26.554000000000002#9', 'SUMITRA KURREY@26.554000000000002#9', 'KUMARI JYOTI LAHRE@26.554000000000002#9', 'SANGEETA@26.554000000000002#9', 'Yamini Verma@26.554000000000002#9', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', None]


    collected = []
    case_number = row[1]
    staff_names = row [7:]
    staff_names = [names for names in staff_names if names is not None and names.strip() !='']
    # print(staff_names)

    count = 0
    name_is, cat_is, case_num_id, amount_is= None, None, None, None
    for each_name in staff_names:
        if '@' in each_name:
            # print()
            # print(each_name)
            if '@' in each_name and '#' not in each_name:
                name_split = each_name.split('@')  #AVINASH MESHRAM@2.9142857142857146'
                name_is = name_split[0]
                amount_is = round(float(name_split[1]), 2)


            if '@' in each_name and '#' in each_name:
                at_split = each_name.split('@')  # AVINASH MESHRAM@2.9142857142857146#1'
                name_is =at_split[0]
                amount_cat = at_split[1].split('#')  # = 2.9142857142857146#1
                amount_is = round(float(amount_cat[0]),2)
                cat_is = int(amount_cat[1])
            count += 1

            # print(name_is, cat_is, case_number, amount_is)
            # print('type of cat', type(cat_is))


            ''' database 3
            74	MAHENDRA KUMAR	N55171003 hk 8
            75	MAHENDRA KUMAR	05170011797 ey 3
            '''
            if name_is.strip() == 'MAHENDRA KUMAR' and cat_is == 3:
                name_id = 75
            elif name_is.strip() == 'MAHENDRA KUMAR' and cat_is == 8:
                name_id = 74
            else:
                name_id = name_map[name_is]
            cat_id = cat_is
            case_num_id = case_num_map[case_number]
            amount_is = amount_is
            # print(name_id, cat_id, case_num_id, amount_is)
            # print()
            collected.append((name_id, cat_id, case_num_id, amount_is))
    return collected


def sql_insertion(datas):
    # Path to your SQLite database file
    # db_path = 'distributionDatabase.db'  # Change to your actual database path

    # SQL Insert query
    insert_query = """
    INSERT INTO distribution_table (distri_name_id, distri_cat_id, distri_case_num_id, distri_amount)
    VALUES (?, ?, ?, ?)
    """

    # Connect to SQLite and insert the data
    try:
        conn = sqlite3.connect(r"G:\My Drive\GdrivePC\Hospital\RSBY\New\incentiveDatabase_3.db")
        cursor = conn.cursor()

        cursor.executemany(insert_query, datas)  # Batch insert all rows at once

        conn.commit()
        print(f"[INFO] Successfully inserted {len(datas)} records into distribution_table.")
    except Exception as e:
        print(f"[ERROR] Failed to insert data: {e}")
    finally:
        conn.close()



def main():
    name_map, case_num_map = load_sql()
    wb = openpyxl.load_workbook(r"G:\My Drive\GdrivePC\Hospital\RSBY\New\ujj.xlsx", read_only=True)
    ws = wb['Incentive_Entered_New']

    t = time.perf_counter()
    rows_data = ws.iter_rows(min_row=2, values_only=True    )

    distibution_data = []
    for i, data in enumerate(rows_data):
        if i == 2022222222222222222222222222:
            break
        # print(list(data))
        # # each_row_process(data, name_map=name_map, case_num_map=case_num_map)
        #
        # if i != 2347:
        #     continue
        # print(i, '--. .', list(data))
        collected = each_row_process(data, name_map=name_map, case_num_map=case_num_map)
        # print(collected)
        print(f'{i} len', len(collected))
        distibution_data.extend(collected)
        # print('distrib', distibution_data)
        print(f'{i} len distri', len(distibution_data))


    t2 =time.perf_counter()
    sql_insertion(distibution_data)
    print(t2-t, 'seconds')


if __name__ == '__main__':
    # load_sql()
    main()
