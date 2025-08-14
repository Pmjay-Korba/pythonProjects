import requests
import gspread

def g_sheet_download(sheet_id, file_name, download_dir=None):
    # sheet_id = "YOUR_SHEET_ID"  # From the sheet URL
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

    response = requests.get(url)
    save_dir = r"./downloads"
    # file_name = 'Ayushman_2025_enhancement.xlsx'
    filepath = f"{save_dir}\\{file_name}"
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"✅ File downloaded successfully! - {file_name}")
    else:
        print("❌ Download failed:", response.status_code)

def col_letter_to_index(letter):
    """Convert column letter(s) like 'A', 'B', 'AA' to number."""
    letter = letter.upper()
    result = 0
    for char in letter:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result

class GSheetHandle:
    def __init__(self, g_workbook_id, auth_file_path):
        self.g_workbook_id = g_workbook_id
        self.auth_file_path = auth_file_path

        # Authenticate using service account file
        gc = gspread.service_account(self.auth_file_path)
        # Open the gsheet
        self.workbook = gc.open_by_key(self.g_workbook_id)


    def g_single_col_data(self, worksheet_name, col_index_start_at_1)->list:
        """
        Used for getting the single column data
        :param worksheet_name: worksheet name of workbook initialised at start
        :param col_index_start_at_1: Index - NON-ZERO
        :return: list of column data
        """
        worksheet = self.workbook.worksheet(worksheet_name)
        col_data = worksheet.col_values(col_index_start_at_1)
        return col_data



    def get_enhance_req_or_not(self, column_index):
        pass


def main():
    # wb_id ='1vhjV0rcODJ4lGYJBHENMnHFvqHgK25dQRt9SVpr_9N4'
    # auth_file_name = r"./downloads/sodium-cat-452017-h0-9d08be057d0e.json"
    #
    # g_wb = GSheetHandle(g_workbook_id=wb_id, auth_file_path=auth_file_name)
    #
    # col_data_a =  g_wb.g_single_col_data(worksheet_name='ENHAN', col_index_start_at_1=1)
    # print(col_data_a)
    print(col_letter_to_index('z'))
    print(col_letter_to_index('ac'))

if __name__ == '__main__':
    main()