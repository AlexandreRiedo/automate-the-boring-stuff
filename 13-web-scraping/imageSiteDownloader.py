from pathlib import Path

import requests
from rich import print as rprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW

SEARCH_TERM = "Monet"

# Setup
rprint("")
browser = webdriver.Firefox()
browser.maximize_window()
Path.mkdir(Path.cwd() / "artvee-images", exist_ok=True)

# Search
browser.get("https://artvee.com/")
search = WDW(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".rsdfm > input:nth-child(1)"))
)
search.send_keys(SEARCH_TERM)
search.send_keys(Keys.ENTER)

# Download a page of images
images = WDW(browser, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img[class="lazy"]'))
)
for img_num, img in enumerate(images, 1):
    img_src = img.get_attribute("src")
    if img_src:
        img_res = requests.get(img_src)
        img_res.raise_for_status()
        with open(f"./artvee-images/img{img_num:0>3}.png", "wb") as img_file:
            img_file.write(img_res.content)
