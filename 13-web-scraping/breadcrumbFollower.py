import re

from playwright.sync_api import sync_playwright
from rich import print as rprint

URL = "https://autbor.com/breadcrumbs/index.html"
NAV_URL = "https://autbor.com/breadcrumbs"

with sync_playwright() as playwright:
    browser = playwright.firefox.launch()
    page = browser.new_page()
    page.goto(URL)

    while True:
        div = page.locator("#hello")
        if (url_re := re.search(r"\b\w+\.html", div.inner_text())) is not None:
            next_url = url_re.group()
            page.goto(f"{NAV_URL}/{next_url}")
        else:
            rprint(f"[green]Secret is located at: {page.url}")
            rprint(f"[blue]The div displays: {div.inner_text()}")
            break