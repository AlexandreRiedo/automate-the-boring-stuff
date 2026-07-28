import sys
import webbrowser

import pyperclip

if len(sys.argv) > 1:
    # Get address from command line.
    address = " ".join(sys.argv[1:])
else:
    # Get address from clipboard.
    address = pyperclip.paste()

# Open the web browser.
webbrowser.open("https://www..openstreetmap.org/search?query=" + address)
