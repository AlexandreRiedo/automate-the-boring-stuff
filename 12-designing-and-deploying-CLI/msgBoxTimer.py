import sys
import time

import pymsgbox

usr_time = int(pymsgbox.prompt("How long should the timer be?") or sys.exit())
time.sleep(usr_time)
pymsgbox.alert("Time's up!")
