#!/usr/bin/python3

import random

def roll(mod=0):
    return random.randint(1, 100)+mod

def rolls(m,mod=0):
    return [(roll()+mod) for i in range(m)]
