from operator import indexOf, itemgetter
from _imports import *
input_data = get_input()
# input_data = get_input("test.txt")
print(input_data)

order = [str(a) for a in ["A", "K", "Q", "J", "T", 9, 8, 7, 6, 5, 4, 3, 2]]


hands = ((5,),(4,1),(3,2),(3,1,1),(2,2,1),(2,1,1,1),(1,1,1,1,1))

def key(hand:tuple[str,str,str,str,str]):
    
    c = set(hand)
    m = []
    for h in c:
        m.append(hand.count(h))

    return tuple(m),tuple([-order.index(h) for h in hand])

hs = []
for l in input_data:
    hand,bid = l.split(" ")
    hk = key(hand)
    hs.append((hk,hand,bid))

hs.sort(key=itemgetter(0))

print(hs)

res = 0
for i,(k,h,b) in enumerate(hs):
    res += (i+1)*int(b)

# print(res)
submit_answer(res,part='a')

# submit_answer(res,part='b')
