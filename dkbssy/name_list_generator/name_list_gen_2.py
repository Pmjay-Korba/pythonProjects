from pathlib import Path
from dkbssy.name_list_generator.name_list_gen import IncentiveNameGenerator
from dkbssy.utils.colour_prints import ColourPrint


def _main(DEPARTMENT_FOLDER_PATH, INCENTIVE_CATEGORY_NUMS):
    # converting to Path object
    DEPARTMENT_FOLDER_PATH = Path(DEPARTMENT_FOLDER_PATH)

    # getting the department name for entry
    auto_3_excel = Path(r"G:\My Drive\GdrivePC\Hospital\RSBY\New\Incentive_auto_ver_3.xlsx")
    incen_obj = IncentiveNameGenerator(auto_3_excel)
    depart_name_for_generated = incen_obj.depart_name_for_entry('Sheet1', 'B5')

    ColourPrint.print_pink(f'Confirm the Department of Entry in Excel B5. Department Name is: {depart_name_for_generated}')
    input("Press Enter to continue")
    ColourPrint.print_yellow(f"Confirm all REQUIRED CATEGORY are present. Category nums are: {INCENTIVE_CATEGORY_NUMS}")
    input("Press Enter to continue")
    print()

    departmental_entry_folder_excels = list(DEPARTMENT_FOLDER_PATH.glob('*.xlsx'))
    # ENTRY OF AL EXCEL STEPWISE
    for excel_sheet in departmental_entry_folder_excels:
        print(excel_sheet)






