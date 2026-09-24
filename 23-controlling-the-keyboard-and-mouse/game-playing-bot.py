from collections import deque
from typing import NamedTuple

import pyautogui as pag
import pyscreeze
from rich import print as rprint

LAUNCH_PATH = "screenshots/launch"
FOOD_PATH = "screenshots/food"
CONF = 0.6

# Launching the game
firefox = pag.getWindowsWithTitle("Firefox")[0]  # pyright: ignore[reportAttributeAccessIssue]
firefox.activate()
firefox.maximize()
pag.sleep(1)

firefox_search = (893, 76)
pag.click(firefox_search)
pag.hotkey("ctrl", "a")
pag.press("del")
pag.write("https://armorgames.com/play/124/sushi-go-round")
pag.press("enter")
pag.sleep(1)

pag.click(f"{LAUNCH_PATH}/play-game.png")
pag.sleep(7.5)

sound = pag.locateOnScreen(f"{LAUNCH_PATH}/sound.png", confidence=CONF)
pag.click(sound)

play = pag.locateOnScreen(f"{LAUNCH_PATH}/purple-play.png", confidence=CONF)
pag.click(play)

skip = pag.locateOnScreen(f"{LAUNCH_PATH}/yellow-skip.png", confidence=CONF)
pag.click(skip)
pag.sleep(0.5)

start_game = pag.locateOnScreen(f"{LAUNCH_PATH}/start-game.png", confidence=CONF)
pag.click(start_game)
pag.sleep(0.5)


# Game loop
class Customer(NamedTuple):
    food: str
    box: pyscreeze.Box


POLL = 1
customers: deque[Customer] = deque()
foods = {
    "california",
    "gunkan",
    "onigiri",
}

while True:
    pag.sleep(POLL)
    for food in foods:
        try:
            for new_box in pag.locateAllOnScreen(
                f"{FOOD_PATH}/{food}.png", confidence=CONF
            ):
                if not any(
                    new_box.left - 25 < box.left < new_box.left + 25
                    for box in [customer.box for customer in customers]
                ):
                    customers.append(Customer(food, new_box))
        except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            rprint(f"[blue]No {food} found.")

    for customer in customers:
        rprint(f"{customer.food} {customer.box}")
    rprint("")
