from selenium import webdriver
import datetime, sqlite3, sys, time, openpyxl, os
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import platform
from pathlib import Path
import winreg

# Function to rename the file
def rename_file(original_name, new_name, directory):
    original_file = os.path.join(directory, original_name)
    new_file = os.path.join(directory, new_name)

    if os.path.exists(new_file):
        os.remove(new_file)  # Remove the existing file if it exists

    while not os.path.exists(original_file):
        time.sleep(1)  # Wait until the file is downloaded

    os.rename(original_file, new_file)

def wait_for_download(filename, download_dir, timeout=30):
    file_path = os.path.join(download_dir, filename)
    temp_file_path = file_path + ".crdownload"  # Chrome uses .crdownload during downloads

    elapsed = 0
    while elapsed < timeout:
        if os.path.exists(file_path) and not os.path.exists(temp_file_path):
            return True  # File is fully downloaded
        time.sleep(1)
        elapsed += 1

    raise TimeoutError(f"Download of {filename} did not complete within {timeout} seconds.")


def wait_for_download_by_prefix(prefix, extension=".xlsx", timeout=30):
    download_dir = get_default_download_dir()
    print(download_dir)
    elapsed = 0
    poll_interval = 1

    while elapsed < timeout:
        matching_files = [
            f for f in os.listdir(download_dir)
            if f.lower().replace('\xa0', ' ').strip().startswith(prefix.lower()) and f.endswith(extension)
        ]

        print("Matching files:", os.listdir(download_dir))

        if matching_files:
            # Sort by last modified
            matching_files.sort(
                key=lambda f: os.path.getmtime(os.path.join(download_dir, f)), reverse=True
            )
            latest_file = matching_files[0]
            # print('latest', latest_file)
            full_path = os.path.join(download_dir, latest_file)
            temp_path = full_path + ".crdownload"

            if not os.path.exists(temp_path):
                return full_path  # Download completed

        time.sleep(poll_interval)
        elapsed += poll_interval

    raise TimeoutError(f"No completed download with prefix '{prefix}' found in {timeout} seconds.")


def download_and_rename_file(driver, wait, download_dir):
    # Open the webpage
    driver.get("https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleInitiatedcasesdme.aspx")

    pagination_xp = "//div[contains(text(),'Showing 1 to') and contains(text(),'entries')] "
    wait.until(EC.presence_of_element_located((By.XPATH, pagination_xp)))

    # Find the download link and click it
    download_link = driver.find_element(By.XPATH,
                                        '//*[@id="ctl00_ContentPlaceHolder1_GridView1_wrapper"]/div[1]/button[3]')  # Change this to the correct XPath
    download_link.click()
    time.sleep(5)

    # Wait for download to finish
    prefix = "Shaheed Veer Narayan Singh Ayushman Swasthya Yojna"
    # Finding the latest file by prefix
    latest_svsn_excel = wait_for_download_by_prefix(prefix=prefix)
    print("Latest Excel Downoladed: ", latest_svsn_excel)

    # Rename the file after downloading
    rename_file(latest_svsn_excel, "bb.xlsx", download_dir)

    # Close the browser
    # driver.quit()

def get_default_download_dir():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
        value, _ = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")
        downloads_path = os.path.expandvars(value)
        print(f"Downloads folder is: {downloads_path}")
        return downloads_path
    except Exception as e:
        return f"Error: {e}"



if __name__ =='__main__':
    # p = wait_for_download_by_prefix("Shaheed Veer Narayan Singh Ayushman Swasthya Yojna",)
    # print(p)
    get_default_download_dir()