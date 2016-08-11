#!/usr/bin/env python

import os, sys

def event_stream(filename):
    with open(filename) as event_stream:
        for event in event_stream:
            yield event

def process_log(filename):
    count = 0
    for event in event_stream(filename):
        #update_model(event)
        if count % 20000 == 0:
            print count,event.strip()
        count += 1
    print count

if __name__ == '__main__':
    """
    Running as script for testing.
    """
    if len(sys.argv) != 2:
        print 'Usage: event.py [log filename]'
        exit(1)
    if os.path.exists(sys.argv[1]):
        process_log(sys.argv[1])
    else:
        print 'File does not exist!'
