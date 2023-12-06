from imports import *
input_data = get_input()#"test.txt")


res = 0

for l in input_data:
    n,ls = l.split(": ")
    win,have = ls.split(" | ")
    print(win)
    win = [int(w) for w in win.split(" ") if w != ""]
    have = [int(h) for h in have.split(" ") if h != ""]
    nsame = set(win).intersection(set(have)).__len__()
    if nsame > 0:
        res += 2**(nsame-1)


submit_answer(res,part='a')