from copy import deepcopy
from math import prod
from _imports import *
from math import perm


import sys
sys.setrecursionlimit(1000000)

cache:dict[tuple[tuple[str,str],...],list[frozenset[str]]] = {}


def get_trees(conns:tuple[tuple[str,str],...])->list[frozenset[str]]:
    if conns in cache:
        # print("cache hit")
        return cache[conns]
    if len(conns) == 0:
        return []
    tree = list(get_trees(conns[1:]))
    conn = conns[0]
    inds = [None,None]
    for n,c in enumerate(conn):
        for i,p in enumerate(tree):
            if c in p:
                inds[n] = i
                break
        else:
            ind = None
    if inds[0] == inds[1]:
        if inds[0] == None:
            tree.append(frozenset(conn))
    else:
        # assert inds[0] is not None or inds[1] is not None
        if inds[0] is None:
            assert inds[1] is not None
            tree[inds[1]] |= frozenset([conn[1]])
        elif inds[1] is None:
            assert inds[0] is not None
            tree[inds[0]] |= frozenset([conn[0]])
        else: #both belong to different, existing trees; merge
            tree[inds[0]] |= (tree[inds[1]])
            tree.pop(inds[1])
    cache[conns] = tree
    return tree



def part1(input:list[str])->int:

    connections:list[tuple[str,str]] = []
    nodes:set[str] = set()
    for l in input:
        name,comps = l.split(": ")
        comps = comps.split(", ")
        connections.extend([(name,c) for c in comps])
        nodes.update(name,*comps)
    

    for conns in tqdm(itertools.combinations(connections,r=len(connections)-3),total=perm(len(connections),3)):
        # print(len(conns))
        trees = get_trees(conns)
        if not all([any([n in t for t in trees]) for n in nodes]): #if not every node is in at least one tree
            continue
        if len(trees) != 3:
            continue
        return prod(map(len,trees))


    pass

def part2(input:list[str])->int:
    pass

if __name__ == "__main__":
    input_data = get_input()
    test_data = get_input("test.txt")

    part = "1"
    # part = "2"

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