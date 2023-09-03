#!/usr/bin/python3

import random

def roll(n = 20, mod = 0):
    return random.randint(1, n) + mod

def rolls(m, n = 20, mod = 0):
    return [roll(n)+mod for i in range(m)]

def toss0(r):
    if not r:
        return None
    r.remove(min(r))
    return r

def toss1(r):
    if not r:
        return None
    r.remove(max(r))
    return r

def toss01(r):
    return toss0(toss1(r))

def rolls_toss0(m, n = 20, mod = 0):
    return toss0(rolls(m, n, mod))

def rolls_toss1(m, n = 20, mod = 0):
    return toss1(rolls(m, n, mod))

def rolls_toss01(m, n = 20, mod = 0):
    return toss0(toss1(rolls(m, n, mod)))
