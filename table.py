#!/usr/bin/env python

usage = """
    Usage: table.py input-string

    input-string - All-letter string to verify.
"""

import sys

def canBeRepresentedByPeriodicTable(input, table):
    """ This will match character patterns of arbitrarty length.
    """
    if not input:
        return True
    for elem in table:
        if input.startswith(elem):
            ret = canBeRepresentedByPeriodicTable(input.replace(elem, "", 1), table)
            if ret:
                return ret
    return False

 
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print usage
        exit(1) 
    input = sys.argv[1].lower()
    if not input.isalpha():
        print usage
        exit(1)

    table = [ "H", "L", "Li", "N" ]
    table = [elem.lower() for elem in table]
    print canBeRepresentedByPeriodicTable(input, table)
