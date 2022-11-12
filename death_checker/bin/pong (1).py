#!/usr/bin/env python3

import sys
from datetime import datetime
import time

while True:
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string + " PONG!")
    sys.stdout.flush()
    time.sleep(10)

