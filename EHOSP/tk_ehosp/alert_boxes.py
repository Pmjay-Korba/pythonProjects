import tkinter as tk
from tkinter import messagebox

def error_tk_box(error_message, error_title="ERROR"):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Make sure it stays on top
    messagebox.showerror(error_title, error_message, parent=root)
    root.destroy()

if __name__ == "__main__":
    error_tk_box('kkkkkk')