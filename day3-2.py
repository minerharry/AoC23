from typing import DefaultDict
from imports import *
import text
import re
p = Puzzle(2023,3)
arr = get_input(p)

def issymbol(s:str):
    if len(s) != 1: raise Exception()
    # print(s)
    return (s != '.' and not s.isdigit())

def get_neighbors(row:int,col:int):
    o = [(-1,0),(-1,-1),(-1,1),(0,1),(0,-1),(1,-1),(1,1),(1,0)]
    for o1,o2 in o:
        if o1 + row < 0:
            continue
        if o2 + col < 0:
            continue
        try:
            yield (o1+row,o2+col)
        except:
            pass
# parts = []
gears:dict[tuple[int,int],list[tuple[int,int]]] = DefaultDict(list)
for r in range(len(arr)):
    for c,el in enumerate(arr[r]):
        if el == "*":
            for g in (get_neighbors(r,c)):
                gears[g].append((r,c))
        # if any([issymbol(v) for v in get_neighbors(r,c)]):
        #     # print(el)
        #     partidx.append((r,c))
            # parts.append(arr[r][c])
print(gears)

nums:list[tuple[tuple[int,int],int,int]] = []
for r,row in enumerate(arr):
    idx = 0
    for n in re.split('[^0-9]',row):
        # print(repr(n))
        if n.isdigit():
            nums.append(((r,idx),len(n),int(n)))
        idx += len(n) + 1
print(nums)

partdict:dict[tuple[int,int],list[int]] = DefaultDict(list)
for n in nums:
    for k in range(n[0][1],n[0][1]+n[1]):
        # print(n)
        # print(k)
        t = n[0][0],k
        if t in gears:
            for g in gears[t]:
                partdict[g].append(n[2])
            break
print(partdict)
# print(parts)
# print(sum(parts))
doubles = [v[0]*v[1] for _,v in partdict.items() if len(v) == 2]
print(doubles)
print(sum(doubles))
        
submit_answer(sum(doubles),part='b',puzzle=p)
