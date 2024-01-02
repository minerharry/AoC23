import pdb
from numpy import block
from _imports import *
directions = {"N":(-1,0),"S":(1,0),"W":(0,-1),"E":(0,1)}

def part1(input,num=64):
    g = str_ndarray(input)
    curr = [np.array(np.where(g=="S"))[:,0]]
    g[curr[0]] = "."
    print(curr)
    # exit()
    bounds = np_bounds(g)
    for _ in range(num):
        n = set()
        for c in curr:
            for d in directions.values():
                o = tuple(np.add(c,d))
                if o in bounds and g[o] == ".":
                    n.add(o)
        curr = n
    return len(curr)

def part2(input,num=26501365):
    g = str_ndarray(input)
    # g = np.pad(g,1,'constant',constant_values='.')
    # print(g)
    curr:list[tuple[tuple[int,int],tuple[int,int]]] = [(tuple(np.array(np.where(g=="S"))[:,0]),(0,0))] #grid-position, global-offset
    start = curr[0][0]
    g[*curr[0][0]] = "."
    print(curr)
    # exit()
    bounds = np_bounds(g)
    completed_blocks = set()
    block_completion:dict[tuple[int,int],list[bool]] = DefaultDict(lambda: [False,False,False,False])
    visited:dict[tuple[int,int],tuple[set[tuple[int,int]],set[tuple[int,int]]]] = DefaultDict(lambda: (set(),set()))
    corners = list(itertools.product([0,g.shape[0]],[0,g.shape[1]]))
    for _ in trange(1,num+1):
        n:set[tuple[tuple[int,int],tuple[int,int]]] = set()
        for c in curr:
            for d in directions.values():
                # if c[1] != (0,0):
                #     pdb.set_trace()
                # print(c)
                o = addtuple(c[0],d)
                # print(o)
                o = (bounds.wrap(o),addtuple(bounds.off(o),c[1]))
                if g[*o[0]] == "#":
                    continue
                # print(o)
                if o[0] in visited[o[1]]:
                    continue
                try:
                    i = corners.index(o[0])
                    block_completion[o[1]][i] = True
                except ValueError: #not a corner
                    pass
                visited[o[1]][_ % 2].add(o[0])
                if all(block_completion[o[1]]):
                    completed_blocks.add(o[1])
                if o[1] == c[1]:
                    n.add(o)
                    continue
                # print("new block!")
                # pdb.set_trace()
                if o[1] in completed_blocks:
                    continue
                n.add(o)
        ##garbage collect block_completion and visited
        blocks = set((c[1] for c in n))
        for b in list(visited):
            if b not in blocks:
                completed_blocks.add(b)
                del visited[b]
        for b in list(block_completion):
            if b not in blocks:
                completed_blocks.add(b)
                del block_completion[b]
        curr = list(n)

    def alternating_array(shape:tuple[int,int],off=0):
        return (((np.arange(shape[0])[:,None] + np.arange(shape[1])) + off + 1) % 2 )
    
    #now: parity
    ## goal: 
        # 1) add up all completed blocks by calculating parity
        # 2) use the parity-visited sets for visited on the edge blocks
    
    alt_sums = (np.sum(alternating_array(g.shape) & (g == ".")),np.sum(alternating_array(g.shape,off=1) & (g == ".")))

    def parity(*s):
        return int(sum(s)%2)
    
    num_parity = parity(num,*start)

    res = 0
    for b in completed_blocks:
        res += alt_sums[parity(num_parity,*b)]
    
    for b,vs in visited.items():
        res += len(vs[parity(num_parity)])

    iembed()
    print({k:(len(v1),len(v2)) for k,(v1,v2) in visited.items()})
    print(alt_sums)
    
    g2 = g.copy()
    for c in visited[0,-1][num_parity]:
        g2[*c] = "O"
    print(g2)

    return res
    pass

if __name__ == "__main__":
    input_data = get_input()
    test_data = get_input("test.txt")

    part = "1"
    part = "2"

    if part == "1":
        print("=== PUZZLE INPUT ===")
        p = part1(input_data)
        print("=== TEST INPUT ===")
        print(part1(test_data,num=6))
        submit_answer(p,part=1)
    else:
        print("=== PUZZLE INPUT ===")
        # p = part2(input_data)
        print("=== TEST INPUT ===")
        # iembed()
        # print(part2(test_data,num=1))
        # print(part2(test_data,num=4))
        # print(part2(test_data,num=6))
        # print(part2(test_data,num=8))
        print(part2(test_data,num=100))
        # print(part1(test_data,num=103))
        # submit_answer(p,part=2)