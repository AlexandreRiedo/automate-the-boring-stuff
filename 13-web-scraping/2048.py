import random
import re

from playwright.sync_api import sync_playwright
from rich import print as rprint

SLOW_MO_MS = 100
PLAY_MS = 10 * 1_000

with sync_playwright() as playwright:
    browser = playwright.firefox.launch(headless=False, slow_mo=SLOW_MO_MS)
    page = browser.new_page()
    page.goto("https://play2048.co/")
    page.get_by_role("banner").get_by_role("button").filter(
        has_text=re.compile(r"^$")
    ).click()

    html_locator = page.locator("html")
    for _ in range(0, PLAY_MS, SLOW_MO_MS):
        html_locator.press(
            random.choice(["ArrowRight", "ArrowLeft", "ArrowUp", "ArrowDown"])
        )

    rprint(
        f"{page.locator('div.min-w-0:nth-child(1) > span:nth-child(3)').inner_text()}"
    )
