from math import dist
from operator import itemgetter
from typing import ChainMap
from _imports import *

directions = {"N":(-1,0),"S":(1,0),"W":(0,-1),"E":(0,1)}
arrows = {"N":"^","W":"<","S":"V","E":">"}
invdir = {"N":"S","E":"W","S":"N","W":"E"}



def part1(input):
    return search(input,part=1)
            
def dir_options(d:tuple[str,int]|None,part:Literal[1,2]):
    options = set(directions)
    if d is not None:
        last,num = d
        options.remove(invdir[last])
        if part == 1:
            if num >= 3:
                options.remove(last)
        else:
            if num <= 3:
                options = set([last])
            elif num >= 10:
                options.remove(last)
    return [(l,directions[l]) for l in options]

def search(input,part:Literal[1,2]):
    grid = np.array([[int(i) for i in l] for l in input])

    pos = (0,0)
    goal = tuple(np.subtract(grid.shape,(1,1)))
    print(goal)

    def heur(p):
        # return 0
        return taxicab(p,goal)
    
    key = tuple[tuple[int,int],tuple[str,int]|None]
    # open:set[tuple[tuple[int,int],tuple[str,int]|None]] = set([(pos,None)])
    cost:dict[key,tuple[int,float]] = {}
    cost[(pos,None)] = (0,heur(pos))
    visited:dict[key,tuple[int,float]] = {}
    costs = ChainMap(cost,visited)
    pred:dict[key,key] = {}
    res = None
    last = None
    bounds = np_bounds(grid)
    e = everyn(500)
    t = StopWatch()
    t.start()
    while cost:
        n = sorted(cost.items(),key=lambda k:k[1][0] + k[1][1])[0]
        
        # print(len(cost))
        # print(len(visited))
        del cost[n[0]]
        visited[n[0]] = n[1]
        (p,d),c = n
        e(lambda:print(t.time(),len(cost),p,goal,dist(p,goal),end='\r'))
        if p == goal:
            if part == 1 or (d is not None and d[1] >= 4):    
                last = (p,d)
                res = c[0]
                break
        for nd,o in dir_options(d,part=part):
            new:tuple[int,int] = tuple(np.add(p,o))
            if new not in bounds:
                continue
            n = None
            if d is None or d[0] != nd:
                n = (new,(nd,1))
            else:
                n = (new,(nd,d[1]+1))
            if n:
                co = (c[0] + grid[*new],heur(new))
                if n in costs:
                    if sum(co) >= sum(costs[n]): #worse
                        continue
                pred[n] = (p,d)
                cost[n] = co #update or put back into cost set
    path:list[key] = []
    r = last
    while r:
        path.append(r)
        if r in pred:
            r = pred[r]
        else:
            r = None
    print()
    print(path)
    dg = np.char.mod('%d', grid)
    print(dg)
    for p,d in path:
        dg[*p] = arrows[d[0]] if d else dg[*p]
    print("\n".join(["".join(s) for s in dg]))


    print()
    return res
def part2(input):
    return search(input,part=2)
    

if __name__ == "__main__":
    input_data = get_input()
    test_data = get_input("test.txt")

    part = "1"
    part = "2"

    if part == "1":
        print("=== PUZZLE INPUT ===")
        # p = part1(input_data)
        print("=== TEST INPUT ===")
        print(part1(test_data))
        print(part1(test_data))
        # submit_answer(p,part=1)
    else:
        print("=== PUZZLE INPUT ===")
        p = part2(input_data)
        print("=== TEST INPUT ===")
        print(part2(test_data))
        submit_answer(p,part=2)
        "[((12, 12), ('S', 8)), ((11, 12), ('S', 7)), ((10, 12), ('S', 6)), ((9, 12), ('S', 5)), ((8, 12), ('S', 4)), ((7, 12), ('S', 3)), ((6, 12), ('S', 2)), ((5, 12), ('S', 1)), ((4, 12), ('E', 4)), ((4, 11), ('E', 3)), ((4, 10), ('E', 2)), ((4, 9), ('E', 1)), ((4, 8), ('S', 4)), ((3, 8), ('S', 3)), ((2, 8), ('S', 2)), ((1, 8), ('S', 1)), ((0, 8), ('E', 8)), ((0, 7), ('E', 7)), ((0, 6), ('E', 6)), ((0, 5), ('E', 5)), ((0, 4), ('E', 4)), ((0, 3), ('E', 3)), ((0, 2), ('E', 2)), ((0, 1), ('E', 1)), ((0, 0), None)]"