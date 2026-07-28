from pathlib import Path

import bs4
import requests
from rich import print as rprint

NUM_IMG = 10
IMG_SELECTOR = "#comic img"
LINK_SELECTOR = 'a[rel="prev"]'
i = 1
link = "https://xkcd.com"

try:
    while i <= NUM_IMG:
        page_res = requests.get(link)
        page_res.raise_for_status()
        parsed = bs4.BeautifulSoup(page_res.text, features="html.parser")

        if not parsed.select(IMG_SELECTOR):
            rprint(f"[red]No image found on {link}")
        else:
            img_src = f"https:{parsed.select(IMG_SELECTOR)[0].get('src')}"
            img_title = Path(img_src).name
            img_res = requests.get(img_src)
            img_res.raise_for_status()
            with open(f"xkcd/{img_title}", "wb") as f:
                f.write(img_res.content)
                rprint(
                    f"[red]{i:0>4} [blue]Downloaded [green]{img_title} [blue]into ./xkcd"
                )

        link = f"https://xkcd.com{parsed.select(LINK_SELECTOR)[0].get('href')}"

        i += 1
except requests.RequestException as exc:
    print(f"There was a problem: {exc}")
