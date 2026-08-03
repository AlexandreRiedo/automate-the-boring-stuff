import shutil
import sys
import urllib.parse as urlp
from pathlib import Path

import bs4
import requests
from rich import print as rprint

DOWNLOAD_DIR = Path.cwd() / "imageDownloader-images"
if DOWNLOAD_DIR.exists():
    shutil.rmtree(DOWNLOAD_DIR)
DOWNLOAD_DIR.mkdir()


def download_images_from(url: str):
    res = requests.get(url)
    res.raise_for_status()

    parsed_url = urlp.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    parsed_html = bs4.BeautifulSoup(res.text, "html.parser")
    img_links = [
        urlp.urljoin(base_url, x.get("src"))  # type: ignore
        for x in parsed_html.select("img")
    ]
    for img_link in img_links:
        try:
            img_res = requests.get(img_link)
            img_res.raise_for_status()
            with open(DOWNLOAD_DIR / Path(img_link).name, "wb") as fout:
                fout.write(img_res.content)
        except requests.RequestException as e:
            rprint(f"{e}")


download_images_from(sys.argv[1])
