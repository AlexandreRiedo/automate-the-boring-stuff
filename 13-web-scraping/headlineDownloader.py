import logging

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright
from rich import print as rprint

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

with sync_playwright() as playwright:
    browser = playwright.firefox.launch()
    page = browser.new_page()
    page.goto("https://www.tdg.ch/")

    try:
        page.get_by_role("button", name="J'accepte").click()
    except PlaywrightTimeoutError as exc:
        logger.info("Cookie consent button not found or could not be clicked: %s", exc)

    titles = page.locator(".titlewrapper span.title")
    for title in sorted(titles.all(), key=lambda x: x.inner_text()):
        rprint(f"[blue]{title.inner_text()}")
        