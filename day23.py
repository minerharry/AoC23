from operator import itemgetter
from random import randint
import random
from _imports import *

directions = {"^":(-1,0),"v":(1,0),"<":(0,-1),">":(0,1)}
invdir = {"^":"v",">":"<","v":"^","<":">"}



def part1(input):
    grid = str_ndarray(input)
    start:tuple[int,int] = (0,np.where(grid[0]==".")[0][0])
    end:tuple[int,int] = (len(grid)-1,np.where(grid[-1]==".")[0][0])

    print(start,end)

    nodes = set()
    bounds = np_bounds(grid)
    for i,j in np.ndindex(grid.shape):
        neighbors = []
        if grid[i,j] != ".":
            continue
        for o in directions.values():
            if (s := addtuple((i,j),o)) in bounds and grid[*s] != "#":
                # if grid[*s] != ".": #slope
                #     if addtuple(s,directions[grid[*s]]) == (i,j):
                #         print(i,j)
                #         continue
                neighbors.append(s)
        if len(neighbors) > 2:
            nodes.add((i,j))

    nodes.add(start)
    nodes.add(end)

    # print(len(nodes))
    # iembed()

    print(nodes)
    print(set([grid[*c] for c in nodes]))

    paths:dict[tuple[int,int],dict[tuple[int,int],int]] = DefaultDict(dict)
    for i in tqdm(nodes):
        for d in directions:
            p = direct_path(grid,i,d,nodes)
            if p is not None:
                # print(i,d)
                paths[i][p[0]] = max(paths[i].get(p[0],-1),p[1])
        # ps = direct_paths(grid,i,nodes.difference([i]),nodes)
        # for dest,cost in ps.items():
        #     paths[i][dest] = cost

    # iembed()

    print(paths)

    ##node_neighbors = paths[i].keys(), "cost[i,j]" = paths[i][j]
    ##now: longest path from start to end without revisiting a node on the directed graph
    ##requires A* <-- WRONG
    ## instead, simplify recursively; let's try simple floyd-warshall, and then potentially something more clever

    # simp_nodes = nodes

    while True:
        pruned = False
        for n in paths:
            assert len(paths[n]) != 0 #we've abandoned a node, bad!
            prune = False
            if len(paths[n]) == 1: #stub; remove if not start or end
                if n not in (start,end):
                    prune = True
            if len(paths[n]) == 2: #intermediary; simplify
                l = list(paths[n])
                bridge = paths[n][l[0]] + paths[n][l[1]]
                if l[0] not in paths[l[1]] or paths[l[1]][l[0]] < bridge:
                    #bridge is better; extend path
                    paths[l[1]][l[0]] = paths[l[0]][l[1]] = bridge
                #path is better, bridge is cringe
                prune = True

            if prune:
                pruned = True
                del paths[n]
                for p in paths.values():
                    try:
                        del p[n]
                    except:
                        pass
        if not pruned:
            break

    print(paths)




                    

                

    # pairs:dict[tuple[tuple[int,int],tuple[int,int]],float] = DefaultDict(lambda:float('-inf'),{(k,v):l for k,t in paths.items() for v,l in t.items()})
    # for (p1,p2),l in pairs.copy().items():
    #     for j in nodes:
    #         if pairs[p1,j] + pairs[j,p2] > l:
    #             pairs[p1,p2] = pairs[p1,j] + pairs[j,p2]

    # print(pairs[start,end])
            
    


    # open:list[tuple[tuple[int,int],...]] = [((start,))] #node history, total length
    # costs:dict[tuple[tuple[int,int],...],tuple[int,int]] = DefaultDict(lambda:(-1,-1),{(start,):(0,0)})
    # closed:set[tuple[tuple[int,int],...]] = set()

    # res = None
    # e = everyn(1)
    # while open:
    #     open.sort(key=costs.__getitem__)
    #     hist = open.pop(0)

    #     cost = costs[hist]
    #     curr = hist[-1]
    #     e(lambda: print(len(open),random.randint(0,10),end="\r"))
    #     # print(open)
    #     for n,c in paths[curr].items():
    #         if n in hist:
    #             continue
    #         nhist = hist+(n,)
    #         if costs[nhist][0] < cost[0]+c:
    #             costs[nhist] = (cost[0]+c,0)
    #             open.append(nhist)

    # #this is inefficient
    # res = 0
    # minhist = None
    # for p,c in costs.items():
    #     if p[-1] == end:
    #         if c[0] > res:
    #             res = c[0]
    #             minhist = p

    # print(minhist)
    # # iembed()

    # return res
        





    
    


def neighbors(pos:tuple[int,int],bounds:np_bounds|None=None):
    for o in directions.values():
        s = addtuple(pos,o)
        if (bounds is None) or (s in bounds):
            yield s





def direct_path(grid:np.ndarray,start:tuple[int,int],dir:str,intersections:set[tuple[int,int]]):
    bounds = np_bounds(grid)
    pos = start
    dist = 1
    # print("starting from ",pos,"direction",dir)
    pos = addtuple(start,directions[dir])
    if pos not in bounds or (grid[*pos]) == "#":
        return None
    # if start == (5,3) and dir == ">":
    #     breakpoint()
    # print(grid[*pos])
    while True:
        # print(pos,dir)
        # pos = addtuple(pos,directions[dir])
        # print(pos,dir)
        for d,off in directions.items() if grid[*pos] == "." else [(grid[*pos],directions[grid[*pos]])]:
            if d != invdir[dir]:
                c = addtuple(pos,off)
                # print(pos,c,d)
                if c in bounds and grid[*c] != "#":
                    if c in intersections:
                        return c,dist+1
                    else:
                        pos = c
                        dir = d
                        dist = dist+1
                        break
        else: #not broken or returned; dead end
            return None




    # open:list[tuple[int,tuple[int,int]]] = [(1,n) for n in neighbors(start,bounds)]
    # res = {}
    # while open:
    #     open.sort(key=itemgetter(0))
    #     print(len(open))
    #     cost,curr = open.pop(0)
    #     if grid[*curr] in directions:
    #         nexts = [addtuple(curr,directions[grid[*curr]])]
    #     else:
    #         nexts = [addtuple(curr,o) for o in directions.values()]
        
    #     for n in nexts:
    #         iembed()
    #         if n == curr:
    #             continue
    #         if n in ends:
    #             if n in intersections:
    #                 res[n] = cost + 1
    #             break
    #         open.append((cost+1,n))
    # return res









def part2(input:list[str]):
    nl = []
    for l in input:
        for d in directions:
            l = l.replace(d,".")
        nl.append(l)
    return part1(nl)

if __name__ == "__main__":
    input_data = get_input()
    test_data = get_input("test.txt")

    # part = "1"
    part = "2"

    if part == "1":
        print("=== PUZZLE INPUT ===")
        p = part1(input_data)
        print("=== TEST INPUT ===")
        print(part1(test_data))
        submit_answer(p,part=1)
    else:
        print("=== PUZZLE INPUT ===")
        p = part2(input_data)
        print("=== TEST INPUT ===")
        print(part2(test_data))
        submit_answer(p,part=2)