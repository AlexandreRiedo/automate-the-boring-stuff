import shutil
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW

SEARCH_TERM = "Monet"
MAX_IMAGES_PER_PAGINATION = 5
MAX_PAGINATIONS = 1_000_000


def search(term, browser):
    browser.get("https://artvee.com/")
    search = WDW(browser, 0.5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".rsdfm > input:nth-child(1)"))
    )
    search.send_keys(term)
    search.send_keys(Keys.ENTER)


def get_image_page_urls(browser):
    time.sleep(0.5)
    img_divs = WDW(browser, 0.5).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div:has(> img.lazy)"))
    )
    img_page_urls = [
        rf"https://artvee.com{img_div.get_attribute('data-url')}"
        for img_div in img_divs
    ]
    return img_page_urls[:MAX_IMAGES_PER_PAGINATION]


def extract_image_slugs(image_page_urls: list[str]):
    return [Path(x).name for x in image_page_urls]  # type: ignore


def download_pagination_images(browser, img_page_urls: list):
    for img_page_url in img_page_urls:
        browser.get(img_page_url)
        img_download = WDW(browser, 0.5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".snax-action-add-to-collection")
            )
        )
        img_download.click()


def get_pagination_urls(browser):
    pagination_size = max(
        int(
            x.get_attribute("href")
            .removeprefix("https://artvee.com/main/page/")  # type: ignore
            .removesuffix(f"/?s={SEARCH_TERM}")
        )
        for x in WDW(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.page-numbers"))
        )
    )
    pagination_urls = [
        f"https://artvee.com/main/page/{x}/?s={SEARCH_TERM}"
        for x in range(2, pagination_size + 1)
    ]

    return pagination_urls[:MAX_PAGINATIONS]


# Setup - download paths, browser setup
shutil.rmtree(Path.cwd() / "artvee-images", ignore_errors=True)
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

# Searching for the term
search(SEARCH_TERM, browser)

# Get the pagination URLs
pagination_urls = get_pagination_urls(browser)

# Download all images and extract slugs
img_page_urls = get_image_page_urls(browser)
img_names = extract_image_slugs(img_page_urls)

download_pagination_images(browser, img_page_urls)  # page 1
for pagination_url in pagination_urls:  # the other pages
    browser.get(pagination_url)
    img_page_urls = get_image_page_urls(browser)
    img_names.extend(extract_image_slugs(img_page_urls))
    download_pagination_images(browser, img_page_urls)

# Rename the images by download order
img_order = sorted(
    (Path.cwd() / "artvee-images").iterdir(), key=lambda x: x.stat().st_birthtime
)
for img_path, img_name in zip(img_order, img_names):
    img_path.rename(f"./artvee-images/{img_name}.png")

# Done
browser.close()
