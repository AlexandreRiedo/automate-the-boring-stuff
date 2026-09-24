import time
from collections import deque
from dataclasses import dataclass

import pyautogui as pag
import pyscreeze
from rich import print as rprint


@dataclass
class Customer:
    box: pyscreeze.Box
    food: str
    handled_time: float | None
    is_handled: bool = False


CONF = 0.8
CONF_FOOD = 0.6
CONF_INGREDIENTS = 0.95
PATH_FOOD = "screenshots/food"
PATH_LAUNCH = "screenshots/launch"
PATH_INGREDIENTS = "screenshots/ingredients"
POLL = 1
TIME_HANDLE = 22

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

pag.click(f"{PATH_LAUNCH}/play-game.png")
pag.sleep(7.5)

sound = pag.locateOnScreen(f"{PATH_LAUNCH}/sound.png", confidence=CONF)
pag.click(sound)

play = pag.locateOnScreen(f"{PATH_LAUNCH}/purple-play.png", confidence=CONF)
pag.click(play)

skip = pag.locateOnScreen(f"{PATH_LAUNCH}/yellow-skip.png", confidence=CONF)
pag.click(skip)
pag.sleep(0.5)

start_game = pag.locateOnScreen(f"{PATH_LAUNCH}/start-game.png", confidence=CONF)
pag.click(start_game)
pag.sleep(1)


# Game loop
customers: deque[Customer] = deque()
foods = {
    "california",
    "onigiri",
    "gunkan",
}
cook = pag.locateOnScreen(f"{PATH_INGREDIENTS}/cook.png", confidence=CONF_INGREDIENTS)
nori = pag.locateOnScreen(f"{PATH_INGREDIENTS}/nori.png", confidence=CONF_INGREDIENTS)
rice = pag.locateOnScreen(f"{PATH_INGREDIENTS}/rice.png", confidence=CONF_INGREDIENTS)
roe = pag.locateOnScreen(f"{PATH_INGREDIENTS}/roe.png", confidence=CONF_INGREDIENTS)


while True:
    # Poll for any new customers
    pag.sleep(POLL)
    for food in foods:
        try:
            for new_box in pag.locateAllOnScreen(
                f"{PATH_FOOD}/{food}.png", confidence=CONF_FOOD
            ):
                if not any(
                    new_box.left - 25 < customer.box.left < new_box.left + 25
                    for customer in customers
                ):
                    customers.append(Customer(new_box, food, None))
        except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            rprint(f"[blue]No {food} found.")

    # Deal with a customer
    if any(not customer.is_handled for customer in customers):
        customer = next(c for c in customers if not c.is_handled)
        match customer.food:
            case "california":
                pag.click(rice)
                pag.click(nori)
                pag.click(roe)
                pag.sleep(0.5)

                pag.click(cook)
                customer.is_handled = True
                customer.handled_time = time.time()
            case "onigiri":
                pag.click(rice)
                pag.click(rice)
                pag.click(nori)
                pag.sleep(0.5)

                pag.click(cook)
                customer.is_handled = True
                customer.handled_time = time.time()
            case "gunkan":
                pag.click(rice)
                pag.click(nori)
                pag.click(roe)
                pag.click(roe)
                pag.sleep(0.5)

                pag.click(cook)
                customer.is_handled = True
                customer.handled_time = time.time()

    # Remove stale served customers
    while (
        customers
        and customers[0].handled_time
        and abs(time.time() - customers[0].handled_time) > TIME_HANDLE
    ):
        customers.popleft()

    rprint()
    for c in customers:
        rprint(f"{c}")
