from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import pickle
# Define the download directory
download_dir = r"G:\My Drive\GdrivePC\Hospital\RSBY\New\down"  # Use raw string notation for Windows paths


def create_driver_old(timeout=10):
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("detach", True)
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, timeout)
    driver.maximize_window()
    return driver, wait

def create_driver(title_given, port_value,timeout=10):
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    options.add_experimental_option("prefs", prefs)
    options.debugger_address = f'localhost:{port_value}'

    try:
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, timeout)

        "Checking the DK page open or not"
        title = driver.title.strip()
        # print(title, title_given)
        # print(title==title_given)

        # Check for specific title match
        if title_given.strip() in title:
            driver.maximize_window()
            return driver, wait
        else:
            print(f"Unexpected page title: {title}")
            driver.quit()
            return None, None

    except Exception as e:
        print(f"Error connecting to Chrome on port {port_value}: {e}")
        return None, None


def create_firefox_driver(timeout=10):
    options = FirefoxOptions()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.download.useDownloadDir", True)
    options.set_preference("browser.download.viewableInternally.enabledTypes", "")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           "application/octet-stream, application/pdf, application/x-pdf, application/vnd.pdf")
    options.set_preference("pdfjs.disabled", True)
    options.add_argument("--start-maximized")

    # Set up the driver with WebDriverManager
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, timeout)
    driver.maximize_window()
    return driver, wait
