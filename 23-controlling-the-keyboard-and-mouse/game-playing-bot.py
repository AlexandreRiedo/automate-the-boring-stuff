import time
from collections import deque
from dataclasses import dataclass

import pyautogui as pag
import pyscreeze
from pyautogui import locateAllOnScreen as loas
from rich import print as rprint


@dataclass
class Customer:
    box: pyscreeze.Box
    food: str
    handled_time: float | None
    is_handled: bool = False


CONF = 0.8
CONF_COOKING = 0.95
CONF_DISHES = 0.70
CONF_INGREDIENTS = 0.95
CONF_RELAXED = 0.6
PATH_COOKING = "screenshots/cooking"
PATH_FOOD = "screenshots/food"
PATH_LAUNCH = "screenshots/launch"
PATH_ORDER = "screenshots/order"
POLL = 0.5
TIME_HANDLE = 25
TIME_DELIVERY = 3


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

play_game = pag.locateOnScreen(f"{PATH_LAUNCH}/play-game.png", confidence=CONF)
pag.click(play_game)
pag.sleep(5)
pag.click(play_game)
pag.sleep(2.5)

sound = pag.locateOnScreen(f"{PATH_LAUNCH}/sound.png", confidence=CONF)
pag.click(sound)

play = pag.locateOnScreen(f"{PATH_LAUNCH}/purple-play.png", confidence=CONF)
pag.click(play)

skip = pag.locateOnScreen(
    f"{PATH_LAUNCH}/yellow-skip.png", confidence=CONF, minSearchTime=2
)
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
ingredients = {"shrimp": 5, "rice": 10, "nori": 10, "roe": 10, "salmon": 5, "unagi": 5}
bubbles = pag.locateOnScreen(f"{PATH_COOKING}/bubbles.png", confidence=CONF)
belt = pag.locateOnScreen(f"{PATH_COOKING}/belt.png", confidence=CONF)
deck = pag.locateOnScreen(f"{PATH_COOKING}/deck.png", confidence=CONF)
panel = pag.locateOnScreen(f"{PATH_COOKING}/panel.png", confidence=CONF)
phone = pag.locateOnScreen(f"{PATH_ORDER}/phone.png", confidence=CONF)
makisu = pag.locateOnScreen(f"{PATH_COOKING}/makisu.png", confidence=CONF)
nori = pag.locateOnScreen(f"{PATH_COOKING}/nori.png", confidence=CONF_COOKING)
rice = pag.locateOnScreen(f"{PATH_COOKING}/rice.png", confidence=CONF_COOKING)
roe = pag.locateOnScreen(f"{PATH_COOKING}/roe.png", confidence=CONF_COOKING)


frame = 0
while True:
    rprint(f"\n=====[orange]Frame {frame}=====")
    for c in customers:
        rprint(f"{c}")

    # Poll for any new customers
    pag.sleep(POLL)
    frame += 1
    for food in foods:
        try:
            for box in loas(
                f"{PATH_FOOD}/{food}.png", confidence=CONF_RELAXED, region=bubbles
            ):
                if not any(
                    box.left - 25 < c.box.left < box.left + 25 for c in customers
                ):
                    customers.append(Customer(box, food, None))
                    rprint(f"[blue]{food} found.")
        except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            pass

    # TODO: assure that there's enough ingredients before cooking
    if any(qty < 2 for qty in ingredients.values()):
        for ingredient, qty in [(i, q) for i, q in ingredients.items() if q < 2]:
            rprint(f"[red]No more {ingredient}")
            pag.click(phone)
            pag.sleep(1)
            if ingredient == "rice":
                rice_menu = pag.locateOnScreen(
                    f"{PATH_ORDER}/rice-menu.png", confidence=CONF, minSearchTime=2
                )
                pag.click(rice_menu)
                rice_order = pag.locateOnScreen(
                    f"{PATH_ORDER}/rice-order.png", confidence=CONF, minSearchTime=2
                )
                pag.click(rice_order)
                delivery = pag.locateOnScreen(
                    f"{PATH_ORDER}/delivery.png", confidence=CONF, minSearchTime=2
                )
                pag.click(delivery)
                ingredients["rice"] += 10
            elif ingredient == "nori":
                nori_menu = pag.locateOnScreen(
                    f"{PATH_ORDER}/topping-menu.png", confidence=CONF, minSearchTime=2
                )
                pag.click(nori_menu)
                nori_order = pag.locateOnScreen(
                    f"{PATH_ORDER}/nori-order.png", confidence=CONF, minSearchTime=2
                )
                pag.click(nori_order)
                delivery = pag.locateOnScreen(
                    f"{PATH_ORDER}/delivery.png", confidence=CONF, minSearchTime=2
                )
                pag.click(delivery)
                ingredients["nori"] += 10
            elif ingredient == "roe":
                roe_menu = pag.locateOnScreen(
                    f"{PATH_ORDER}/topping-menu.png", confidence=CONF, minSearchTime=2
                )
                pag.click(roe_menu)
                roe_order = pag.locateOnScreen(
                    f"{PATH_ORDER}/roe-order.png", confidence=CONF, minSearchTime=2
                )
                pag.click(roe_order)
                delivery = pag.locateOnScreen(
                    f"{PATH_ORDER}/delivery.png", confidence=CONF, minSearchTime=2
                )
                pag.click(delivery)
                ingredients["roe"] += 10

        pag.sleep(TIME_DELIVERY)

    # Cook for a customer
    if any(not customer.is_handled for customer in customers):
        customer = next(c for c in customers if not c.is_handled)
        match customer.food:
            case "california":
                pag.click(rice)
                pag.click(nori)
                pag.click(roe)

                ingredients["rice"] -= 1
                ingredients["nori"] -= 1
                ingredients["roe"] -= 1
            case "onigiri":
                pag.click(rice)
                pag.click(rice)
                pag.click(nori)

                ingredients["rice"] -= 2
                ingredients["nori"] -= 1
            case "gunkan":
                pag.click(rice)
                pag.click(nori)
                pag.click(roe)
                pag.click(roe)

                ingredients["rice"] -= 1
                ingredients["nori"] -= 1
                ingredients["roe"] -= 2
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
        for dish in loas(
            f"{PATH_COOKING}/dish.png", confidence=CONF_DISHES, region=deck
        ):
            pag.click(dish)
        for turd in loas(
            f"{PATH_COOKING}/turd.png", confidence=CONF_DISHES, region=belt
        ):
            pag.click(turd)
        rprint("[blue]Dishes or turds found.")
    except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
        pass
