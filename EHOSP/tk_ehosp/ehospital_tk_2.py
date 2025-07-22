import tkinter as tk
from tkinter import ttk, messagebox, Entry
import sqlite3
from sqlite3 import OperationalError
from functools import partial


# for creating the ward database - NO LONGER NEEDED
def ward_database():
    ward_dict = {
        'New Ward (General ward)': 'New',
        'LOT (General ward)': 'LOT',
        'EYE Ward (General ward)': 'EYE',
        'NRC, (General ward)': 'NRC',
        'SNCU., (General ward)': 'SNCU',
        'Female Ward (General ward)': 'Female',
        'Male Ward (General ward)': 'Male',
        'ISOLATION WARD (General ward)': 'ISOLATION',
        'Emergency Ward (General ward)': 'Emergency',
        'Darmatology Ward (General ward)': 'Darmatology',
        'Orthopedic ward (General ward)': 'Orthopedic',
        'psychiatric ward (General ward)': 'psychiatric',
        'ENT ward (General ward)': 'ENT',
        'Oncology (General ward)': 'Oncology',
        'Paediatrics (General ward)': 'Paediatrics',
        'Burn Ward (General ward)': 'Burn',
        'Surgical Ward (General ward)': 'Surgical',
    }

    conn =  sqlite3.connect('ward_database_file.db')
    cursor = conn.cursor()
    for k,v in ward_dict.items():
        cursor.execute(f''' CREATE TABLE "{v}"(
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "title" TEXT,
            "admission"	TEXT,
            "treatment"	TEXT,
            "discharge"	TEXT,
            "summary"	TEXT)
            ''')

    conn.commit()
    conn.close()


# ward_database()

def proper_2():
    head_label =ttk.Label(master=root, )

def proper():
    # head_label = print(ttk.Label())
    head_label = ttk.Label(root, text='Welcome to the database management', font=("Arial", 18, "bold"))
    head_label.grid(row=0, column=0, columnspan=3, padx=250, pady=20)

    ward_dict = {
        'New Ward (General ward)': 'New',
        'LOT (General ward)': 'LOT',
        'EYE Ward (General ward)': 'EYE',
        'NRC, (General ward)': 'NRC',
        'SNCU., (General ward)': 'SNCU',
        'Female Ward (General ward)': 'Female',
        'Male Ward (General ward)': 'Male',
        'ISOLATION WARD (General ward)': 'ISOLATION',
        'Emergency Ward (General ward)': 'Emergency',
        'Darmatology Ward (General ward)': 'Darmatology',
        'Orthopedic ward (General ward)': 'Orthopedic',
        'psychiatric ward (General ward)': 'psychiatric',
        'ENT ward (General ward)': 'ENT',
        'Oncology (General ward)': 'Oncology',
        'Paediatrics (General ward)': 'Paediatrics',
        'Burn Ward (General ward)': 'Burn',
        'Surgical Ward (General ward)': 'Surgical'
     }

    # creating label for ward dropdown
    wards_dd_label = tk.Label(root, text='Select Ward', font='bold')
    wards_dd_label.grid(padx=25, row=1,column=0, sticky='w')

    dropdown_wards = ttk.Combobox(root, values=[v for k,v in ward_dict.items()], state='readonly')
    dropdown_wards.grid(row=1,column=1, sticky='w', ipadx=50, pady=10)

    # creating the data label and field for filling the records
    title_for_entry = tk.Label(root, text='Title for the entry(DIAGNOSIS)', padx=25 , font=("Arial", 11))
    condition_on_admission = tk.Label(root, text='Condition on admission', padx=25, font=("Arial", 11))
    treatment_given = tk.Label(root, text='Treatment given', padx=25, font=("Arial", 11))
    condition_on_discharge = tk.Label(root, text='Condition on discharge', padx=25, font=("Arial", 11))
    summary = tk.Label(root, text='Summary', padx=25, font=("Arial", 11))

    # griding the data labels in column 2
    title_for_entry.grid(row=2,column=0, sticky='w', pady=5)
    condition_on_admission.grid(row=3,column=0, sticky='w', pady=5)
    treatment_given.grid(row=4,column=0, sticky='w', pady=5)
    condition_on_discharge.grid(row=5,column=0, sticky='w', pady=5)
    summary.grid(row=6,column=0, sticky='w', pady=5)

    # creating entry form
    title_for_entry_entry = tk.Entry(root, width=67)
    condition_on_admission_entry = tk.Text(root,height=5, width=50)
    treatment_given_entry = tk.Text(root,height=5, width=50)
    condition_on_discharge_entry = tk.Text(root,height=5, width=50)
    summary_entry = tk.Text(root,height=5, width=50)

    # griding the forms in column 1
    title_for_entry_entry.grid(row=2,column=1,ipadx=35, sticky='w', pady=5)
    condition_on_admission_entry.grid(row=3,column=1,ipadx=35, sticky='w', pady=5)
    treatment_given_entry.grid(row=4,column=1,ipadx=35, sticky='w', pady=5)
    condition_on_discharge_entry.grid(row=5,column=1,ipadx=35, sticky='w', pady=5)
    summary_entry.grid(row=6,column=1,ipadx=35, sticky='w', pady=15)

    # getting the data
    def retrieve_data():
        dropdown_wards_to_entry = dropdown_wards.get()
        title_to_entry = title_for_entry_entry.get()
        admission_to_entry = condition_on_admission_entry.get("1.0", "end-1c")
        treatment_to_entry = treatment_given_entry.get("1.0", "end-1c")
        discharge_to_entry = condition_on_discharge_entry.get("1.0", "end-1c")
        summary_to_entry = summary_entry.get("1.0", "end-1c")

        print(dropdown_wards_to_entry,
          title_to_entry,
          admission_to_entry,
          treatment_to_entry,
          discharge_to_entry,
          summary_to_entry)

        # clearing the fields
        dropdown_wards.set("")
        title_for_entry_entry.delete(0,"end")
        condition_on_admission_entry.delete(1.0, "end-1c")
        treatment_given_entry.delete(1.0, "end-1c")
        condition_on_discharge_entry.delete(1.0,"end-1c")
        summary_entry.delete(1.0,"end-1c")

        return dropdown_wards_to_entry, title_to_entry,admission_to_entry, treatment_to_entry, discharge_to_entry, summary_to_entry

    # def update_function():


    # button creation
    but_update = tk.Button(root, text="Show Data", padx=25, command=lambda:show_data_function(dropdown_wards.get()))
    but_update.config(bg='yellow')
    but_update.grid(row=7,column=0, sticky='w', padx=120)

    # button_2
    but_submit = tk.Button(root, text='Submit', padx=25, command=lambda: sqlite_submit(retrieve_data()))

    but_submit.config(bg='green')
    but_submit.grid(row=7, column=1, sticky='w', padx=120)

    # button_3
    but_exit = tk.Button(root, text='Exit', padx=25, command=lambda:exit())
    but_exit.config(bg='red')
    but_exit.grid(row=7, column=2, sticky='w', padx=50)

    notes_entry = tk.Label(root, wraplength=900, fg='red',padx=50, justify='left', pady=20, font=("Arial", 12),
                           text='''Note :
1. Write diagnosis present only on website with EXACT same spelling,\n    if multiple diagnosis separate them by "COMMA only."
2. DO NOT use Tab and Enter buttons inside writing texts.
3. ONLY ALLOWED special characters  & @ % . ( ) _ - / | inside writing texts.
    ''')
    notes_entry.grid(row=8, column=0, sticky='w', columnspan=3)

def set_root_state(states):
    """Enable or disable all widgets in the root window."""
    for widget in root.winfo_children():
        widget.configure(state=states)

def show_data_function(ward_name=""):
    print(ward_name)

    if ward_name == "":
        tk.messagebox.showwarning('Ward Name Error', 'Select Ward to Proceed')

    else:
        ''' opening the tip window and disabling the root window'''
        if ward_name is None:
            tk.messagebox.showerror("Warning", "Select the ward first")

        # Disable all widgets in the root window
        set_root_state("disabled")

        show_frame = tk.Toplevel(root)
        show_frame.geometry('1200x600')

        def on_close():
            show_frame.destroy()
            set_root_state("normal")

        show_frame.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close event

        '''generating the function to display info'''
        show_data_window(show_frame, ward_name)

def adjust_row_heights(frame, labels, row_indices):
    """Adjust row height dynamically based on text content."""
    frame.update_idletasks()  # Ensure all widgets are rendered before measuring
    for label, row in zip(labels, row_indices):
        height = label.winfo_reqheight()  # Get actual height of the label
        frame.grid_rowconfigure(row, minsize=height)  # Set row height dynamically

def show_data_window(frame: tk.Toplevel, ward_name):
    frame.title('Ward Data')

    # Create a canvas and add a scrollbar
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the content
    content_frame = tk.Frame(canvas)

    # Create window in canvas and attach content_frame
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Place the canvas and scrollbar in the main window
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Set row configuration for resizing
    frame.grid_rowconfigure(0, weight=1, minsize=500)
    frame.grid_columnconfigure(0, weight=1)

    # Headers and ward labels
    wards_dd_label = tk.Label(content_frame, text='Selected Ward', font='bold')
    wards_dd_label.grid(padx=25, row=1, column=0, sticky='w', pady=10)

    wards_name_label = tk.Label(content_frame, text=ward_name, font='bold')
    wards_name_label.grid(padx=25, row=1, column=1, sticky='w', pady=10)

    delete_button = tk.Button(content_frame, text='Delete by ID -->', bg='red', command=lambda:delete_function())
    delete_button.grid(padx=25, row=1, column=3, sticky='w', pady=10, ipadx=20)

    delete_entry_field = tk.Entry(content_frame)
    # delete_entry_field.insert(0,'Type Data ID to delete')
    delete_entry_field.grid(padx=25, row=1, column=4, sticky='w', pady=10, ipadx=20)

    # deleting_id_int = delete_entry_field.get()

    # Creating headers
    headers = ["Data ID", "Title", "Condition on Admission", "Treatment Given", "Condition on Discharge", "Summary"]
    for col, text in enumerate(headers):
        tk.Label(content_frame, text=text, padx=25, font=("Arial", 12, "bold")).grid(row=2, column=col, sticky='w', pady=5)

    # Getting all data of a ward (list of tuples)
    each_ward_data = get_data_from_sqlite(ward_name)

    labels = []  # Store labels for height adjustment
    row_indices = []  # Store row numbers

    for idx, each_procedure_data in enumerate(each_ward_data):
        idx += 3  # Start from the third row
        wrap_width = 150  # Adjust the width for better word wrapping

        # Creating labels with proper wrapping and no fixed height
        data_id_entry = tk.Label(content_frame, text=each_procedure_data[0], wraplength=wrap_width, justify="center", anchor="center")
        title_for_entry_entry = tk.Label(content_frame, text=each_procedure_data[1], wraplength=wrap_width, justify="left", anchor="w")
        condition_on_admission_entry = tk.Label(content_frame, text=each_procedure_data[2], wraplength=wrap_width, justify="left", anchor="w")
        treatment_given_entry = tk.Label(content_frame, text=each_procedure_data[3], wraplength=wrap_width, justify="left", anchor="w")
        condition_on_discharge_entry = tk.Label(content_frame, text=each_procedure_data[4], wraplength=wrap_width, justify="left", anchor="w")
        summary_entry = tk.Label(content_frame, text=each_procedure_data[5], wraplength=wrap_width, justify="left", anchor="w")


        # Grid placement
        data_id_entry.grid(row=idx, column=0, ipadx=10, sticky='w', pady=5, padx=15)
        title_for_entry_entry.grid(row=idx, column=1, ipadx=10, sticky='w', pady=5)
        condition_on_admission_entry.grid(row=idx, column=2, ipadx=10, sticky='w', pady=5)
        treatment_given_entry.grid(row=idx, column=3, ipadx=10, sticky='w', pady=5)
        condition_on_discharge_entry.grid(row=idx, column=4, ipadx=10, sticky='w', pady=5)
        summary_entry.grid(row=idx, column=5, ipadx=10, sticky='w', pady=5)


        # Store labels and row indices for height adjustment
        labels.extend([title_for_entry_entry, condition_on_admission_entry, treatment_given_entry,
                       condition_on_discharge_entry, summary_entry, data_id_entry])
        row_indices.extend([idx] * 6)  # Same row for all columns

    # Adjust row heights dynamically after layout is updated
    frame.after(100, partial(adjust_row_heights, frame, labels, row_indices))

    # Update scroll region after the frame content is placed
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))  # Make sure scroll region includes all content



    def delete_function():
        data_id_to_delete = delete_entry_field.get().strip()
        print (data_id_to_delete, type(data_id_to_delete))
        # deleting the item by id
        res = messagebox.askokcancel('Confirm Delete', 'Do you want to delete this entry?')
        if res:
            try:
                deleting_id_int = int(data_id_to_delete)
                conn = sqlite3.connect('ward_database_file.db')
                cursor = conn.cursor()
                cursor.execute(f'DELETE FROM "{ward_name}" WHERE id = ?', (deleting_id_int,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Entry with ID {deleting_id_int} deleted successfully.")
                frame.destroy()  # Close the window after deletion
                set_root_state('normal')
            except ValueError:
                messagebox.showerror("Error", "Invalid ID entered. Please enter a number.")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error deleting record: {e}")

# def get_data_from_sqlite(ward_name)->list[tuple]:
#     conn = sqlite3.connect('ward_database_file.db')
#     cursor = conn.cursor()
#     table_data = cursor.execute(f'''
#         SELECT * FROM {ward_name}
#     ''')
#     table_data = list(table_data)
#     print(table_data)
#     return table_data

def get_data_from_sqlite(ward_name:str, db_path:str='ward_database_file.db')->list[tuple]:

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    table_data = cursor.execute(f'''
        SELECT * FROM {ward_name}
    ''')
    table_data = list(table_data)
    print(table_data)
    return table_data

def sqlite_submit(retrieved_data):
#                   table_name,
#                   title_to_entry,
#                   admission_to_entry,
#                   treatment_to_entry,
#                   discharge_to_entry,
#                   summary_to_entry):
    try:
        conn= sqlite3.connect('ward_database_file.db')

        cursor = conn.cursor()

        #  query = 'INSERT INTO "{}" (name, age) VALUES (?, ?)' .format(table_name)

        query = '''
            INSERT INTO "{}" (title, admission, treatment, discharge, summary)
            VALUES (?,?,?,?,?)
            '''.format(retrieved_data[0])

        cursor.execute(
            query,(
                retrieved_data[1],
                retrieved_data[2],
                retrieved_data[3],
                retrieved_data[4],
                retrieved_data[5])
            )

        conn.commit()
        conn.close()
    except OperationalError:
        tk.messagebox.showerror("Operation Error", 'Enter data for Entry')


# def main_func():
#     proper()

def create_gui():
    """Initialize the main application window."""
    global root
    root = tk.Tk()
    root.geometry('1000x700')
    root.title("E-Hospital Database")

    proper_2()

    root.mainloop()


if __name__ =='__main__':
    # root = tk.Tk()
    # root.geometry('1000x600')
    # root.title("E-Hospital Database")
    #
    # main_func()
    # # get_data_from_sqlite("NRC")
    #
    # root.mainloop()

    create_gui()