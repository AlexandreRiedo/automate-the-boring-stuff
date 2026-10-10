import itertools
import sys
import time
from collections import deque
from dataclasses import dataclass

import pyautogui as pag
import pyscreeze
from pyautogui import locateAllOnScreen as loas
from rich import print as rprint

COLOR_BROWN = (121, 60, 4)
COLOR_ORANGE = (255, 106, 12)
CONF = 0.8
CONF_COOKING = 0.95
CONF_DISHES = 0.70
CONF_INGREDIENTS = 0.95
CONF_ORDER = 0.9
CONF_RELAXED = 0.6
INF = 3
PATH_COOKING = "screenshots/cooking"
PATH_FOOD = "screenshots/food"
PATH_LAUNCH = "screenshots/launch"
PATH_ORDER = "screenshots/order"
POLL = 0.5
TIME_HANDLE = 22
TIME_DELIVERY = 6
TIME_COOK = 1


@dataclass
class Customer:
    box: pyscreeze.Box
    food: str
    handled_time: float | None
    is_handled: bool = False


@dataclass
class Delivery:
    ingredient: str
    quantity: int
    handled_time: float


def clickSafely(image: str, search_confidence=CONF):
    def x():
        try:
            box = pag.locateOnScreen(image, confidence=search_confidence)
            pag.click(box)
            return True
        except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            pag.sleep(1)
            return False

    while not x():
        pass


def reduced_loas(img_path, confidence, region):
    res = []
    for box in loas(img_path, confidence=confidence, region=region):
        if not any(abs(other.left - box.left) < 25 for other in res):
            res.append(box)
    return res


# Launching the game
def launch():
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
    pag.sleep(2.5)

    play_game = pag.locateOnScreen(f"{PATH_LAUNCH}/play-game.png", confidence=CONF)
    pag.click(play_game)
    pag.sleep(7.5)
    pag.click(play_game)
    pag.click(play_game)
    pag.sleep(2.5)

    skip = pag.locateOnScreen(
        f"{PATH_LAUNCH}/yellow-skip.png", confidence=CONF, minSearchTime=2
    )
    pag.click(skip)
    pag.sleep(0.5)

    start_game = pag.locateOnScreen(f"{PATH_LAUNCH}/start-game.png", confidence=CONF)
    pag.click(start_game)
    pag.sleep(1)


# pag.sleep(2)
launch()


# Game Setup
def order_ingredient(ingredient: str, deliveries: list[Delivery]):
    def x():
        try:
            pag.click(phone)

            if ingredient == "rice":
                menu = pag.locateOnScreen(
                    f"{PATH_ORDER}/rice-menu.png", confidence=CONF_INGREDIENTS
                )
            else:
                menu = pag.locateOnScreen(
                    f"{PATH_ORDER}/topping-menu.png", confidence=CONF_INGREDIENTS
                )
            pag.click(menu)
            order = pag.locateOnScreen(
                f"{PATH_ORDER}/{ingredient}-order.png", confidence=CONF_INGREDIENTS
            )
            pag.click(order)
            delivery = pag.locateOnScreen(
                f"{PATH_ORDER}/delivery-free.png", confidence=CONF_INGREDIENTS
            )
            pag.click(delivery)

            if ingredient in {"rice", "nori", "roe"}:
                deliveries.append(Delivery(ingredient, 10, time.time()))
            else:
                deliveries.append(Delivery(ingredient, 5, time.time()))
            return True
        except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            clickSafely(f"{PATH_ORDER}/close.png", search_confidence=CONF_RELAXED)
            pag.sleep(2)
            return False

    while not x():
        pass


def order(food: str, deliveries: list[Delivery], ingredients: dict[str, int]):
    def verify_backlog(ingredient, amount_needed):
        return (
            ingredients[ingredient]
            + sum(d.quantity for d in deliveries if d.ingredient == ingredient)
            >= amount_needed
        )

    match food:
        case "california":
            if not verify_backlog("rice", 1):
                order_ingredient("rice", deliveries)
            if not verify_backlog("roe", 1):
                order_ingredient("roe", deliveries)
            if not verify_backlog("nori", 1):
                order_ingredient("nori", deliveries)
        case "combo":
            if not verify_backlog("rice", 2):
                order_ingredient("rice", deliveries)
            if not verify_backlog("roe", 1):
                order_ingredient("roe", deliveries)
            if not verify_backlog("unagi", 1):
                order_ingredient("unagi", deliveries)
            if not verify_backlog("salmon", 1):
                order_ingredient("salmon", deliveries)
            if not verify_backlog("shrimp", 1):
                order_ingredient("shrimp", deliveries)
            if not verify_backlog("nori", 1):
                order_ingredient("nori", deliveries)
        case "dragon":
            if not verify_backlog("rice", 2):
                order_ingredient("rice", deliveries)
            if not verify_backlog("roe", 1):
                order_ingredient("roe", deliveries)
            if not verify_backlog("unagi", 2):
                order_ingredient("unagi", deliveries)
            if not verify_backlog("nori", 1):
                order_ingredient("nori", deliveries)
        case "gunkan":
            if not verify_backlog("rice", 1):
                order_ingredient("rice", deliveries)
            if not verify_backlog("roe", 2):
                order_ingredient("roe", deliveries)
            if not verify_backlog("nori", 1):
                order_ingredient("nori", deliveries)
        case "onigiri":
            if not verify_backlog("rice", 2):
                order_ingredient("rice", deliveries)
            if not verify_backlog("nori", 1):
                order_ingredient("nori", deliveries)
        case "salmon":
            if not verify_backlog("rice", 1):
                order_ingredient("rice", deliveries)
            if not verify_backlog("salmon", 2):
                order_ingredient("salmon", deliveries)
            if not verify_backlog("nori", 1):
                order_ingredient("nori", deliveries)
        case "shrimp":
            if not verify_backlog("rice", 1):
                order_ingredient("rice", deliveries)
            if not verify_backlog("shrimp", 2):
                order_ingredient("shrimp", deliveries)
            if not verify_backlog("nori", 1):
                order_ingredient("nori", deliveries)
        case "unagi":
            if not verify_backlog("rice", 1):
                order_ingredient("rice", deliveries)
            if not verify_backlog("unagi", 2):
                order_ingredient("unagi", deliveries)
            if not verify_backlog("nori", 1):
                order_ingredient("nori", deliveries)


def cook(customer, ingredients):
    match customer.food:
        case "california":
            pag.click(rice, duration=0.25)
            pag.click(nori)
            pag.click(roe)

            ingredients["rice"] -= 1
            ingredients["nori"] -= 1
            ingredients["roe"] -= 1
        case "combo":
            pag.click(rice, duration=0.25)
            pag.sleep(0.25)
            pag.click(rice)
            pag.click(nori)
            pag.click(roe)
            pag.click(salmon)
            pag.click(unagi)
            pag.click(shrimp)

            ingredients["rice"] -= 2
            ingredients["nori"] -= 1
            ingredients["roe"] -= 1
            ingredients["salmon"] -= 1
            ingredients["unagi"] -= 1
            ingredients["shrimp"] -= 1
        case "dragon":
            pag.click(rice, duration=0.25)
            pag.sleep(0.25)
            pag.click(rice)
            pag.click(nori)
            pag.click(roe)
            pag.click(unagi)
            pag.sleep(0.25)
            pag.click(unagi)

            ingredients["rice"] -= 2
            ingredients["nori"] -= 1
            ingredients["roe"] -= 1
            ingredients["unagi"] -= 2
        case "gunkan":
            pag.click(rice, duration=0.25)
            pag.click(nori)
            pag.click(roe)
            pag.sleep(0.25)
            pag.click(roe)

            ingredients["rice"] -= 1
            ingredients["nori"] -= 1
            ingredients["roe"] -= 2
        case "onigiri":
            pag.click(rice, duration=0.25)
            pag.sleep(0.25)
            pag.click(rice)
            pag.click(nori)

            ingredients["rice"] -= 2
            ingredients["nori"] -= 1
        case "salmon":
            pag.click(rice, duration=0.25)
            pag.click(nori)
            pag.click(salmon)
            pag.sleep(0.25)
            pag.click(salmon)

            ingredients["rice"] -= 1
            ingredients["nori"] -= 1
            ingredients["salmon"] -= 2
        case "shrimp":
            pag.click(rice, duration=0.25)
            pag.click(nori)
            pag.click(shrimp)
            pag.sleep(0.25)
            pag.click(shrimp)

            ingredients["rice"] -= 1
            ingredients["nori"] -= 1
            ingredients["shrimp"] -= 2
        case "unagi":
            pag.click(rice, duration=0.25)
            pag.click(nori)
            pag.click(unagi)
            pag.sleep(0.25)
            pag.click(unagi)

            ingredients["rice"] -= 1
            ingredients["nori"] -= 1
            ingredients["unagi"] -= 2
    pag.sleep(0.5)
    pag.click(makisu)
    pag.sleep(1)
    clickSafely(f"{PATH_COOKING}/makisu.png")
    customer.is_handled = True
    customer.handled_time = time.time()


def have_stock(food, ingredients):
    match food:
        case "california":
            return ingredients["rice"] and ingredients["nori"] and ingredients["roe"]
        case "combo":
            return (
                ingredients["rice"] >= 2
                and ingredients["nori"]
                and ingredients["roe"]
                and ingredients["unagi"]
                and ingredients["salmon"]
                and ingredients["shrimp"]
            )
        case "dragon":
            return (
                ingredients["rice"] >= 2
                and ingredients["nori"]
                and ingredients["roe"]
                and ingredients["unagi"] >= 2
            )
        case "gunkan":
            return (
                ingredients["rice"] and ingredients["nori"] and ingredients["roe"] >= 2
            )
        case "onigiri":
            return ingredients["rice"] >= 2 and ingredients["nori"]
        case "salmon":
            return (
                ingredients["rice"]
                and ingredients["nori"]
                and ingredients["salmon"] >= 2
            )
        case "shrimp":
            return (
                ingredients["rice"]
                and ingredients["nori"]
                and ingredients["shrimp"] >= 2
            )
        case "unagi":
            return (
                ingredients["rice"]
                and ingredients["nori"]
                and ingredients["unagi"] >= 2
            )


def clean_dishes(img_path, region):
    try:
        for item in reduced_loas(
            img_path=img_path, confidence=CONF_DISHES, region=region
        ):
            pag.click(item)
        rprint(f"[blue]{img_path.split('/')[-1]} dishes found.")
    except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
        pass


def contains_color(box, color):
    return any(
        pag.pixelMatchesColor(x, y, color)
        for x, y in itertools.product(
            range(box.left + 2, box.left + box.width // 4 + 1),
            range(box.top - 3 + box.height // 2, box.top + 3 + box.height // 2),
        )
    )


def next_level():
    global ingredients
    global frame
    global level

    try:
        next_level = pag.locateOnScreen(
            f"{PATH_LAUNCH}/next-level.png", confidence=CONF
        )
        pag.click(next_level)
        pag.sleep(0.25)
        if level < 7:
            pag.click(next_level)
            pag.sleep(0.25)
        else:
            rprint("[magenta]Sushi Go Round has been beaten !")
            sys.exit(0)

        # If the level has been failed, retry
        try:
            fail = pag.locateOnScreen(
                f"{PATH_LAUNCH}/fail-continue.png", confidence=CONF
            )
            pag.click(fail)
            pag.sleep(0.25)
            yes = pag.locateOnScreen(f"{PATH_LAUNCH}/yes.png", confidence=CONF)
            pag.click(yes)
            pag.sleep(0.25)
            pag.click(next_level)
        except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            level += 1

        ingredients = {
            "shrimp": 5,
            "rice": 10,
            "nori": 10,
            "roe": 10,
            "salmon": 5,
            "unagi": 5,
        }
        frame = 1
        customers.clear()
        deliveries.clear()
    except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
        pass


customers: deque[Customer] = deque()
deliveries: list[Delivery] = []
foods = {
    "california",
    "onigiri",
    "gunkan",
    "salmon",
    "shrimp",
    "unagi",
    "dragon",
    "combo",
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
salmon = pag.locateOnScreen(f"{PATH_COOKING}/salmon.png", confidence=CONF_COOKING)
shrimp = pag.locateOnScreen(f"{PATH_COOKING}/shrimp.png", confidence=CONF_COOKING)
unagi = pag.locateOnScreen(f"{PATH_COOKING}/unagi.png", confidence=CONF_COOKING)
assert deck is not None
frame = 1
level = 1


# Game loop
while True:
    # Advance to the next level if necessary
    next_level()

    # Debug
    rprint(f"\n=====[orange]Level {level} engine loop n°{frame}=====")
    rprint("Current customers:")
    for c in customers:
        rprint(f"{c}")
    rprint("\nCurrent deliveries:")
    for d in deliveries:
        rprint(f"{d}")
    rprint("")
    frame += 1

    # Poll for any new customers
    pag.sleep(POLL)
    for food in foods:
        try:
            for box in reduced_loas(
                img_path=f"{PATH_FOOD}/{food}.png", confidence=0.8, region=bubbles
            ):
                # Avoid collisions
                if not any(
                    box.left - 25 < c.box.left < box.left + 25 for c in customers
                ):
                    # Differentiate between shrimp and unagi
                    if food == "unagi" and contains_color(box, COLOR_ORANGE):
                        continue
                    if food == "shrimp" and contains_color(box, COLOR_BROWN):
                        continue

                    customers.append(Customer(box, food, None))
                    rprint(f"[blue]{food} found at {box=}")
        except (pag.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            pass

    # Cook for customers
    for customer in [c for c in customers if not c.is_handled]:
        # Check if deliveries have arrived
        for shipped_delivery in [
            d for d in deliveries if abs(time.time() - d.handled_time) > TIME_DELIVERY
        ]:
            ingredients[shipped_delivery.ingredient] += shipped_delivery.quantity
            deliveries.remove(shipped_delivery)

        # Cook if we have the ingredients, otherwise order some with the backlog in mind
        if have_stock(customer.food, ingredients):
            cook(customer, ingredients)
        else:
            order(customer.food, deliveries, ingredients)

    # Remove stale served customers
    while (
        customers
        and customers[0].handled_time
        and abs(time.time() - customers[0].handled_time) > TIME_HANDLE
    ):
        customers.popleft()

    # Removing dishes and turds
    clean_dishes(f"{PATH_COOKING}/dish-purple.png", deck)
    clean_dishes(f"{PATH_COOKING}/dish-blue-big.png", deck)
    clean_dishes(f"{PATH_COOKING}/dish-blue-small.png", deck)
    clean_dishes(f"{PATH_COOKING}/dish-red.png", deck)
    clean_dishes(f"{PATH_COOKING}/turd.png", belt)
