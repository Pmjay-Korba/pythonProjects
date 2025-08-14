import tkinter as tk
from tkinter import messagebox

def _tk_box(error_message, error_title="ERROR"):
    root = tk.Tk()
    # root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Make sure it stays on top
    # messagebox.showerror(error_title, error_message, parent=root)

    # root.destroy()

    root.mainloop()





if __name__ == "__main__":
    _tk_box('kkkkkk')