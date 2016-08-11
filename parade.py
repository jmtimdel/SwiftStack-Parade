#!/usr/bin/env python

import os
import sys

usage = """
    parade.py [-dh] [input-file]

    Determines non-contentious orderings for parade participants based
    on constraints in an input file.

    -d         - Prints debug output.
    -h         - Prints this usage info.
    input-file - Name of constraints text file.  Defaults to 'parade_data'.
"""

debug = False
def dprint(s):
    if debug:
        print s

num_tries = 0       # Count of attempts to build valid list.

input_file = 'parade_data'
for arg in sys.argv[1:]:
    if arg.startswith('-'):
        if arg.startswith('-d'):
            debug = not debug
        else:
            print usage
            exit(1)
    else:
        input_file = arg
if not os.path.exists(input_file):
    print "No input file!"
    exit(1)

dprint("Reading constraints from input file...")
with open(input_file) as input:
    consts = [l.split() for l in input if l]

rules = []
for const in consts:
    """ joins are done to accommodate multi-word names.
    The rules are just before/after 2-tuples.
    """
    dprint("constraint %s" %str(const))
    if 'comes' not in const:
        print "Illegal request file!"
        exit(1)
    comes = const.index('comes')
    if 'before' == const[comes+1]:
        rule = (' '.join(const[:comes]), ' '.join(const[comes+2:]))
    elif 'after' == const[comes+1]:
        rule = (' '.join(const[comes+2:]), ' '.join(const[:comes]))
    else:
        print "Illegal request file!"
        exit(1)
    rules.append(rule)

rules.sort()
dprint("Sorted rules...\n%s" % '\n'.join((str(rule) for rule in rules)))


def validate(tree):
    for rule in rules:
        if rule[0] in tree and rule[1] in tree:
            if tree.index(rule[0]) > tree.index(rule[1]):
                return None
    return tree


dprint("Check rules...")
for rule in rules:
    if not validate(rule):
        dprint("%s...not ok." % str(rule))
        print "Illegal request file!"
        exit(1)
    dprint("%s...ok." % str(rule))


def grow_one(tree, values):
    global num_tries
    num_tries += 1
    if not values:
        return validate(tree)
    for i in range(len(values)):
        dprint("i: %i values: %s" % (i, str(values)))
        out = values.pop(i)
        tree.append(out)
        valid = validate(tree)
        if valid:
            rvalue = grow_one(tree, values)
            if rvalue:
                return rvalue
        dprint("Dead end: %s" % str(tree))
        values.insert(i, out)
        tree.pop()
    return None
    

def grow_all(tree, values, results):
    dprint("grow_all")
    dprint(str(tree))
    dprint(str(values))
    global num_tries
    num_tries += 1
    if not values:
        tree = validate(tree)
        if tree:
            dprint("GOT ONE: %s" % str(tree))
            results.append(list(tree))
            dprint(str(results))
        return results
    for i in range(len(values)):
        out = values.pop(i)
        tree.append(out)
        valid = validate(tree)
        if valid:
            results = grow_all(tree, values, results)
        else:
            dprint("Dead end: %s" % str(tree))
        values.insert(i, out)
        tree.pop()
    return results


valSet = set([val for rule in rules for val in rule])
values = list(valSet)
dprint("Value set:")
dprint(str(values))
tree = grow_one([], values)
print "\ngrow_one() took %i tries to grow a list:" % num_tries
print str(tree)

values = list(valSet)
dprint("Value set:")
dprint(str(values))
num_tries = 0
allTrees = grow_all([], values, [])
print "\ngrowAll() took %i tries to grow %i list(s):" % (num_tries, len(allTrees))
print "\n".join((str(tree) for tree in allTrees))
