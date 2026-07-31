import shutil
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE = "https://artvee.com"
SEARCH_TERM = "Monet"
MAX_IMAGES_PER_PAGE = 5
MAX_PAGES = 1_000_000
DOWNLOAD_DIR = Path.cwd() / "artvee-images"


def make_browser():
    options = webdriver.FirefoxOptions()
    options.set_preference("browser.download.folderList", 2)  # 2 = use custom dir
    options.set_preference("browser.download.dir", str(DOWNLOAD_DIR))
    options.set_preference("browser.download.useDownloadDir", True)
    browser = webdriver.Firefox(options=options)
    browser.maximize_window()
    return browser


def wait_for(browser, selector, condition=EC.presence_of_element_located, timeout=0.5):
    return WebDriverWait(browser, timeout).until(condition((By.CSS_SELECTOR, selector)))


def search(browser, term):
    browser.get(BASE)
    wait_for(browser, ".rsdfm > input:nth-child(1)").send_keys(term + Keys.ENTER)


def result_page_urls(browser):
    """URLs of result pages 2..N, read from the pagination links on page 1."""
    links = wait_for(browser, "a.page-numbers", EC.presence_of_all_elements_located, 10)
    last = max(int(a.get_attribute("href").split("/page/")[1].split("/")[0]) for a in links)
    urls = [f"{BASE}/main/page/{n}/?s={SEARCH_TERM}" for n in range(2, last + 1)]
    return urls[:MAX_PAGES]


def scrape_current_page(browser):
    """Trigger the download for each artwork on the current result page, return slugs."""
    time.sleep(0.5)
    divs = wait_for(browser, "div:has(> img.lazy)", EC.visibility_of_all_elements_located)
    art_urls = [BASE + d.get_attribute("data-url") for d in divs][:MAX_IMAGES_PER_PAGE]

    for url in art_urls:
        browser.get(url)
        wait_for(browser, ".snax-action-add-to-collection", EC.visibility_of_element_located).click()

    return [Path(url).name for url in art_urls]


def main():
    shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)
    DOWNLOAD_DIR.mkdir()

    with make_browser() as browser:
        search(browser, SEARCH_TERM)
        page_urls = result_page_urls(browser)

        names = scrape_current_page(browser)
        for page_url in page_urls:
            browser.get(page_url)
            names.extend(scrape_current_page(browser))

    downloads = sorted(DOWNLOAD_DIR.iterdir(), key=lambda p: p.stat().st_birthtime)
    for path, name in zip(downloads, names):
        path.rename(DOWNLOAD_DIR / f"{name}.png")


if __name__ == "__main__":
    main()
