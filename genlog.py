#!/usr/bin/env python

import time
import random

JITTER = 275 
TICKS = 1000
LINES_PER_TICK = 1000

def log_line(now):
    timestamp = now - (random.random() * JITTER)
    return "%f   City %d" % (timestamp, random.randint(0,10000))

if __name__ == '__main__':
    """
    Run as script to spew events to stdout to redirect to a file.
    """
    start = time.time()
    for tick in xrange(TICKS):
        now = start + tick
        for num_line in xrange(LINES_PER_TICK):
            print(log_line(now))
else:
    """
    import to instantiate an event generator without need for a log file.
    """
    def event_stream(event_count=TICKS*LINES_PER_TICK):
        start = time.time()
        for tick in xrange(TICKS):
            now = start + tick
            for num_line in xrange(LINES_PER_TICK):
                yield log_line(now)
