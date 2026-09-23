from collections import deque

import pyautogui as pag
from rich import print as rprint

IMG_PATH = "screenshots/"

# Launching the game
firefox = pag.getWindowsWithTitle("Firefox")[0]  # pyright: ignore[reportAttributeAccessIssue]
firefox.activate()
firefox.maximize()
pag.sleep(1)

while True:
    pag.keyDown("shiftleft")
    pag.click(f"{IMG_PATH}firefox-reload.png")
    pag.keyUp("shiftleft")
    pag.sleep(1)

    pag.click(f"{IMG_PATH}play-game.png")
    pag.sleep(2.5)

    try:
        pag.click(f"{IMG_PATH}play-error.png")
    except pag.ImageNotFoundException:
        rprint("[green]Game loaded fine")
        break
    else:
        rprint("[red]Error loading, trying again")

pag.sleep(5)


pag.click(f"{IMG_PATH}sound.png")

play = pag.locateOnScreen(f"{IMG_PATH}purple-play.png", minSearchTime=2)
pag.click(play)

skip = pag.locateOnScreen(f"{IMG_PATH}yellow-skip.png", minSearchTime=2)
pag.click(skip)
pag.sleep(0.5)

pag.click(f"{IMG_PATH}continue.png")
pag.sleep(0.5)

# Game loop
customers = deque()
foods = {
    "california",
    "gunkan",
    "onigiri",
}
while True:
    pag.sleep(1)

    for food in foods:
        try:
            for customer in pag.locateAllOnScreen(f"{IMG_PATH}{food}.png"):
                # if customer not in customers:
                # customers.append(f"{food}: {customer}")
                rprint(f"{food}: {customer=}")
        except:
            rprint(f"[blue]No {food} found.")

    rprint(f"{customers=}")
