from math import prod
from _imports import *
input_data = get_input("test.txt")
input_data = get_input()

##naive solution
times = [int(f) for f in input_data[0].split("Time: ")[1].split(" ") if f != '']
lengths = [int(f) for f in input_data[1].split(": ")[1].split(" ") if f != '']


part = 1
if part == 2:
    times = [int(''.join([str(t) for t in times]))]
    lengths = [int(''.join([str(t) for t in lengths]))]

races:list[tuple[int,int]] = [*zip(times,lengths)]
ss = []
for t,l in races:
    s = 0
    for t1 in tqdm(range(t+1)):
        t2 = t - t1
        r = (t1)*(t2)
        if r > l:
            s += 1
            # print(t1,t2,r,l)    
    ss.append(s)
print(ss)
res = prod(ss)

# 0 6 10 12 12 10 6 0



print(res)
# submit_answer(res,part='a')

submit_answer(res,part='b')