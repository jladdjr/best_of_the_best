#!/usr/bin/env python

import argparse
from math import ceil, log2
import os
from pathlib import Path, PurePath
from random import sample
import sys

import yaml

current_dir = Path()  # current dir

parser = argparse.ArgumentParser(description='Best of the best!')
args = parser.parse_args()

path = PurePath(current_dir, 'options.yml')

options = None
with open(path, 'r') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    options = list(option for option in data)

def get_preference(first, second):
    pref = None
    while pref not in (1, 2):
        pref = int(input(f'"{first}" or "{second}"?\n'))
    return pref

grand_results = {o: 0 for o in options}

# most preffered results at end
sorted_results = []

round_count = 1
def round():
    global options, round_count

    winners = []

    if len(options) == 1:
        print(f'{options[0]} wins!')
        winner = options[0]
        sorted_results.append(winner)
        grand_results[winner] += round_count
        return False # this was the final round

    print(f'Round: {round_count}')

    for i in range(len(options) // 2):
        pref = get_preference(options[2 * i], options[2 * i + 1])
        if pref == 1:
            winner = options[2 * i]
            loser = options[2 * i + 1]
        else:
            winner = options[2 * i + 1]
            loser = options[2 * i]

        sorted_results.append(loser)
        grand_results[loser] += round_count
        winners.append(winner)

    if len(options) % 2 == 1:
        print(f'{options[-1]} gets a by.')
        winners.append(options[-1])

    print('')
    round_count += 1
    options = winners
    return True

# Double elimination!

for i in range(2):
    print(f'\n*** Iteration {i + 1} of the tournament ***')
    # shuffle options
    options = sample(grand_results.keys(), k=len(grand_results))
    round_count = 1
    while round():
        pass

print('\n**** Winners! ****\n')
for option, weight in sorted(grand_results.items(), key=lambda x: x[1], reverse=True):
    print(f'- {option} ({weight})')
