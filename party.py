#!/usr/bin/env python

import os
import sys
import json
import fileinput
from itertools import combinations

usage = """
    Usage: party.py [company data JSON filename]

           party.py<ret>
           [paste company data as JSON]
           <EOF>
"""

if sys.argv[1].startswith("-h"):
    print usage
    exit(1)

def party_score(invitees):
    return sum(p['score'] for p in invitees)

"""
Use fileinput so we can input from a file or paste json.
"""
json_doc = ''
for line in fileinput.input():
    json_doc += line

party_co = json.loads(json_doc)

def test_list(invitees):
    """
    Validate an invite list.
    """
    for in1 in invitees:
        if next((True for in2 in invitees if in2['name'] == in1['boss']), None):
            return None
    return invitees

def allowed_lists(party_co):
    """
    Generate all allowed guest lists for parties of two and greater.
    """
    for n in range(1, len(party_co) + 1):
        n_combos = combinations(party_co, n)
        for guest_list in n_combos:
            if test_list(guest_list):
                yield guest_list

def score(guest_list):
    return sum(guest['party-animal-score'] for guest in guest_list)

"""
Guest list party scores and guest lists saved as tuples: (party-score, guest-list).
"""
guest_lists = []
for guest_list in allowed_lists(party_co):
    guest_lists.append((score(guest_list), guest_list))

guest_lists.sort(reverse=True)

print 'CEO not necessarily invited, best party (animal score %s):' % str(guest_lists[0][0]).rstrip('0')
for party in guest_lists:
    """May have tie high score."""
    if party[0] == guest_lists[0][0]:
        print '\n'.join([person['name'] for person in party[1]])
        print
    else:
        break

for party in guest_lists:
    if any([guest for guest in party[1] if not guest['boss']]):
        print 'CEO definitely on the list (animal score %s):' % str(party[0]).rstrip('0')
        print '\n'.join([person['name'] for person in party[1]])
        break
