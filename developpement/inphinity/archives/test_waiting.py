#!/usr/bin/env bash

import sys
import time

print ("processing..."),
animation = "|/-\\"
idx = 0

for _ in range(10):
        sys.stdout.write(animation[idx % len(animation)] + "\r")
        sys.stdout.flush()
        time.sleep(.5)
        idx += 1