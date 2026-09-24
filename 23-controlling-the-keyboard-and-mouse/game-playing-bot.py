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
CONF_COOKING = 0.95
CONF_DISHES = 0.55
CONF_RELAXED = 0.6
PATH_COOKING = "screenshots/cooking"
PATH_FOOD = "screenshots/food"
PATH_LAUNCH = "screenshots/launch"
POLL = 0.5
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

makisu = pag.locateOnScreen(f"{PATH_COOKING}/makisu.png", confidence=CONF_COOKING)

nori = pag.locateOnScreen(f"{PATH_COOKING}/nori.png", confidence=CONF_COOKING)
rice = pag.locateOnScreen(f"{PATH_COOKING}/rice.png", confidence=CONF_COOKING)
roe = pag.locateOnScreen(f"{PATH_COOKING}/roe.png", confidence=CONF_COOKING)

frame = 0

while True:
    rprint(f"\n=====[orange]Frame {frame}=====")
    frame += 1

    # Poll for any new customers
    pag.sleep(POLL)
    for food in foods:
        try:
            for new_box in pag.locateAllOnScreen(
                f"{PATH_FOOD}/{food}.png", confidence=CONF_RELAXED
            ):
                if not any(
                    new_box.left - 25 < c.box.left < new_box.left + 25
                    for c in customers
                ):
                    customers.append(Customer(new_box, food, None))
        except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            rprint(f"[blue]No {food} found.")

    # TODO: assure that there's enough ingredients before cooking

    # Serve a customer
    if any(not customer.is_handled for customer in customers):
        customer = next(c for c in customers if not c.is_handled)
        match customer.food:
            case "california":
                pag.click(rice)
                pag.click(nori)
                pag.click(roe)
            case "onigiri":
                pag.click(rice)
                pag.click(rice)
                pag.click(nori)
            case "gunkan":
                pag.click(rice)
                pag.click(nori)
                pag.click(roe)
                pag.click(roe)
        pag.sleep(0.5)
        pag.click(makisu)
        customer.is_handled = True
        customer.handled_time = time.time()

    # Remove stale served customers
    while (
        customers
        and customers[0].handled_time
        and abs(time.time() - customers[0].handled_time) > TIME_HANDLE
    ):
        customers.popleft()

    # Removing dishes and turds
    try:
        for dish in pag.locateAllOnScreen(
            f"{PATH_COOKING}/dish.png", confidence=CONF_DISHES
        ):
            pag.click(dish)
        for turd in pag.locateAllOnScreen(
            f"{PATH_COOKING}/turd.png", confidence=CONF_DISHES
        ):
            pag.click(turd)
    except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
        rprint("[blue]No dishes or turds found.")

    for c in customers:
        rprint(f"{c}")
