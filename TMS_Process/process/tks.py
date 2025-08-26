import tkinter as tk
from tkinter import messagebox
import os
import json
from tkinter import Tk, filedialog

from EHOSP.tk_ehosp.alert_boxes import error_tk_box


def _tk_box(error_message, error_title="ERROR"):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Make sure it stays on top
    messagebox.showerror(error_title, error_message, parent=root)

    root.destroy()


APP_NAME = "my_app"  # Change this to your project name

def get_config_path():
    """Get path to config.json stored in user home folder."""
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, f".{APP_NAME}")
    os.makedirs(config_dir, exist_ok=True)  # Create folder if missing
    return os.path.join(config_dir, "config.json")

def load_base_folder():
    """Load base folder path from config.json."""
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("BASE_FOLDER_PATH")
    return None

def save_base_folder(path):
    """Save base folder path to config.json."""
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump({"BASE_FOLDER_PATH": path}, f)

def select_base_folder():
    """Open Tkinter dialog to select a folder."""
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Base Folder")
    root.destroy()
    return folder_path if folder_path else None

def initial_setup_for_base_folder() -> bool:
    """Get base folder from config or ask user."""
    base_folder = load_base_folder()
    if not base_folder or not os.path.exists(base_folder):
        print("Base folder not set or invalid. Please select.")
        error_tk_box(error_title='SELECT BASE FOLDER', error_message='This step is one time setup.\n\nSelect your main folder like "OPD IPD".\n\nCare fully select otherwise difficult to reset.')
        folder = select_base_folder()
        if not folder:
            print("No folder selected. Exiting.")
            error_tk_box(error_message="YOU MUST SELECT BASE FOLDER. TRY BY RE-RUNNING IT.")
            raise FileNotFoundError("You must select folder to proceed")
            # return False
        save_base_folder(folder)
        base_folder = folder

    print(f"Using base folder: {base_folder}")
    return base_folder

if __name__ == "__main__":
    if initial_setup_for_base_folder():
        print("Setup complete.")



