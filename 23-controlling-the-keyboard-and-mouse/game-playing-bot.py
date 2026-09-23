import pyautogui as pag

IMG_PATH = "screenshots/"

# Launching the game
firefox = pag.getWindowsWithTitle("Firefox")[0]  # pyright: ignore[reportAttributeAccessIssue]
firefox.activate()
firefox.maximize()
pag.sleep(1)

pag.keyDown("shiftleft")
pag.click(f"{IMG_PATH}firefox-reload.png")
pag.keyUp("shiftleft")
pag.sleep(1.5)

pag.click(f"{IMG_PATH}play-game.png")
pag.sleep(7.5)

pag.click(f"{IMG_PATH}sound.png")

play = pag.locateOnScreen(f"{IMG_PATH}purple-play.png", minSearchTime=2)
pag.click(play)

skip = pag.locateOnScreen(f"{IMG_PATH}yellow-skip.png", minSearchTime=2)
pag.click(skip)
pag.sleep(0.5)

pag.click(f"{IMG_PATH}continue.png")
