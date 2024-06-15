from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


# DRS Config
drs_base_url = "https://drs.faa.gov/browse/excelExternalWindow"

#Selenium Config
chrome_driver_path = "/Users/josh.mac/Downloads/chromedriver-mac-arm64/chromedriver"
chrome_options = Options()
chrome_options.add_argument("--headless")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


def build_drs_request_url(ad_unid):
    return f"{drs_base_url}/{ad_unid}.0001"


def download_ad_content(drs_url):
    driver.get(drs_url)
    time.sleep(5)

    try:
        print(f"Downloading AD Data")
        wait = WebDriverWait(driver, 3)
        print_button = wait.until(EC.element_to_be_clickable(
            (By.ID, "printButton")
        ))
        print_button.click()

        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        ad_content = driver.page_source
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        exit()
    finally:
        driver.quit()

    return ad_content


def save_ad_content(ad_content, ad_number, download_path):
    if not ad_content:
        print("No AD content was available")
        return None

    file_path = os.path.join(download_path, f"{ad_number}.html")
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ad_content)

    print(f"AD HTML content saved to {file_path}")
    
    return file_path
