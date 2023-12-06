from typing import DefaultDict
from imports import *
input_data = get_input()#"test.txt")


res = 0
accs = DefaultDict(lambda:1)
idx = 1
for l in input_data:
    nthis = accs[idx]
    idx += 1
    # accs = DefaultDict(lambda:0,{k-1:v for k,v in accs.items()})
    n,ls = l.split(": ")
    win,have = ls.split(" | ")
    print(win)
    win = [int(w) for w in win.split(" ") if w != ""]
    have = [int(h) for h in have.split(" ") if h != ""]
    nsame = set(win).intersection(set(have)).__len__()

    for k in range(idx,idx+nsame):
        accs[k] += nthis*1
    print(nsame)
    print(accs)
    res += nthis

print(accs)
print(res)
    # if nsame > 0:
    #     res += 2**(nsame-1)


submit_answer(res,part='b')