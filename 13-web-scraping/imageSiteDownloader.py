import time
from pathlib import Path

from rich import print as rprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW

SEARCH_TERM = "Monet"

# Setup
rprint("")

Path.mkdir(Path.cwd() / "artvee-images", exist_ok=True)

download_dir = Path.cwd() / "artvee-images"
options = webdriver.FirefoxOptions()
options.set_preference(
    "browser.download.folderList", 2
)  # 2 = use the custom dir below.
options.set_preference("browser.download.dir", str(download_dir))
options.set_preference("browser.download.useDownloadDir", True)

browser = webdriver.Firefox(options=options)
browser.maximize_window()

# Search
browser.get("https://artvee.com/")
search = WDW(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".rsdfm > input:nth-child(1)"))
)
search.send_keys(SEARCH_TERM)
search.send_keys(Keys.ENTER)

# Download a page of images
time.sleep(10)
img_divs = WDW(browser, 10).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div:has(> img.lazy)"))
)
img_page_urls = [
    rf"https://artvee.com{img_div.get_attribute('data-url')}" for img_div in img_divs
]
for img_page_url in img_page_urls:
    browser.get(img_page_url)
    img_download = WDW(browser, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".snax-action-add-to-collection")
        )
    )
    img_download.click()
