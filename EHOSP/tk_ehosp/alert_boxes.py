import tkinter as tk
from tkinter import messagebox, simpledialog
import asyncio
import subprocess
import ctypes
import win32gui


def error_tk_box(error_message: object, error_title: object = "ERROR") -> None:
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Make sure it stays on top
    messagebox.showerror(error_title, error_message, parent=root)
    root.destroy()

def tk_ask_yes_no(question: str, title: str = "Confirm") -> bool:
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Keep dialog on top

    result = messagebox.askyesno(title, question, parent=root)

    root.destroy()
    return result



def tk_ask_input(question: str, title: str = "Input", default: str = "") -> str:
    """Ask user for a digit input between 1 and 5, default accepted if empty."""
    while True:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        answer = simpledialog.askstring(title, question, initialvalue=default, parent=root)
        root.destroy()

        # User pressed Cancel
        if answer is None:
            return None

        # User pressed Enter without typing → accept default
        if answer.strip() == "":
            return default

        # Validate input
        if answer.isdigit() and 1 <= int(answer) <= 5:
            return answer
        else:
            error_tk_box("Please enter a number between 1 and 5.")
            # Loop will repeat for re-entry


def select_ward(default="Routine Ward"):
    """
    Shows a centered dialog with selectable ward options.
    Returns the selected option as a string, or None if cancelled.
    """
    def on_submit(event=None):
        """Submit the selection. Accept default if empty or Enter pressed."""
        nonlocal selection
        selection = var.get() or default
        root.destroy()

    selection = None

    # Create main window
    root = tk.Tk()
    root.title("Ward Selection")
    root.attributes("-topmost", True)

    # Options
    options = [
        "HDU",
        "ICU - With Ventilator",
        "ICU - Without Ventilator",
        "ICU with Inotropes and Ventilator",
        "Routine Ward"
    ]

    # Tkinter variable to hold selection
    var = tk.StringVar(value=default)  # default selection

    # Title label
    tk.Label(root, text="Select Ward Type:", font=("Arial", 14, "bold")).pack(pady=10)

    # Radio buttons
    for option in options:
        tk.Radiobutton(
            root, text=option, variable=var, value=option,
            font=("Arial", 12), anchor="w", padx=20, pady=5
        ).pack(fill="x", padx=20, pady=2)

    # Submit button taller
    submit_btn = tk.Button(root, text="Submit", font=("Arial", 12, "bold"),
                           command=on_submit, height=2)
    submit_btn.pack(pady=15, ipadx=10)  # ipadx for horizontal padding inside button

    # Bind Enter key to submit
    root.bind("<Return>", on_submit)

    # Update geometry based on content and center the window
    root.update_idletasks()
    width = max(root.winfo_reqwidth(), 400)  # width based on content, min 400
    height = root.winfo_reqheight()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Force focus on the window and Submit button
    root.lift()             # Bring window to top
    root.focus_force()      # Focus on this window
    submit_btn.focus_set()  # Optional: focus on submit button

    # Start main loop
    root.mainloop()

    return selection



def discharge_type_selector_tk(default="Normal Discharge"):
    """
    Shows a centered dialog with selectable ward options.
    Returns the selected option as a string, or None if cancelled.
    """
    def on_submit(event=None):
        """Submit the selection. Accept default if empty or Enter pressed."""
        nonlocal selection
        selection = var.get() or default
        root.destroy()

    selection = None

    # Create main window
    root = tk.Tk()
    root.title("Ward Selection")
    root.attributes("-topmost", True)

    # Options
    options = [
        "Live Discharge",
        "Normal Discharge",
        "LAMA",
        "DAMA",
        "Death"
    ]

    # Tkinter variable to hold selection
    var = tk.StringVar(value=default)  # default selection

    # Title label
    tk.Label(root, text="Select Discharge Type:", font=("Arial", 14, "bold")).pack(pady=10)

    # Radio buttons
    for option in options:
        tk.Radiobutton(
            root, text=option, variable=var, value=option,
            font=("Arial", 12), anchor="w", padx=20, pady=5
        ).pack(fill="x", padx=20, pady=2)

    # Submit button taller
    submit_btn = tk.Button(root, text="Submit", font=("Arial", 12, "bold"),
                           command=on_submit, height=2)
    submit_btn.pack(pady=15, ipadx=10)  # ipadx for horizontal padding inside button

    # Bind Enter key to submit
    root.bind("<Return>", on_submit)

    # Update geometry based on content and center the window
    root.update_idletasks()
    width = max(root.winfo_reqwidth(), 400)  # width based on content, min 400
    height = root.winfo_reqheight()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Force focus on the window and Submit button
    root.lift()             # Bring window to top
    root.focus_force()      # Focus on this window
    submit_btn.focus_set()  # Optional: focus on submit button

    # Start main loop
    root.mainloop()

    return selection


# Example usage
if __name__ == "__main__":
    # user_input_days = tk_ask_input(
    #     question="How many days you want to take enhancement.\nType in below for desired days.\nPRESSING Enter without typing number of days\nwill automatically take 3 days",
    #     default="3")
    # print(user_input_days)
    # print(discharge_type_selector_tk())
    # select_ward()
    open_folder_topmost(r"I:\Other computers\MSW 2025\IPD2025 MSW\MONTH OF SEPTEMBER\11.09.2025\JAY PAL\WhatsApp Image 2025-09-11 at 13.14.39_b84d8db9.jpg")
