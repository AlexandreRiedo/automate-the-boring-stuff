import sys
from urllib.parse import urlparse

import requests
from playwright.sync_api import sync_playwright
from rich import print as rprint


def main():
    if len(sys.argv) == 1:
        rprint("[blue]You must supply a URL as an argument to use this script.")
        return

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        page = browser.new_page()
        page.goto(sys.argv[1])

        anchors = page.locator("a")
        for url in [x.get_attribute("href") for x in anchors.all()]:
            if url is None:
                continue

            if url.startswith(("/", "./")):
                url = f"{urlparse(page.url).scheme}://{urlparse(page.url).netloc}" + url.removeprefix(".")

            try:
                requests.get(url).raise_for_status()
                rprint(f"[green]Valid URL: {url}")
            except requests.RequestException as e:
                rprint(f"[red]{e}")


if __name__ == "__main__":
    main()
