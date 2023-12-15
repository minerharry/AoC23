import itertools
from math import lcm

import pandas as pd
from _imports import *
input_data = get_input()
# input_data = get_input("test.txt")

seq = itertools.cycle(input_data[0])

lines = {}
starts = []
for l in input_data[2:]:
    lo,lv = l.split(" = (")
    if lo.endswith("A"):
        starts.append(lo)
    lv = lv.strip(")").split(", ")
    lines[lo] = {"L":lv[0],"R":lv[1]}

tots = []
for s in starts:
    curr = s
    res = 0
    while not curr.endswith("Z"):
        # print(curr)
        res += 1
        s = next(seq)
        curr = lines[curr][s]
    tots.append(res)

res = lcm(*tots)

print(res)
# submit_answer(res,part='a')

submit_answer(res,part='b')