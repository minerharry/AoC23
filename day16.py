from _imports import *

splitters = {'|':"NS","-":"EW"}
reflectors:dict[str,tuple[str,str]] = {'\\':("NE","SW"),"/":("NW","SE")}
directions = {"N":(-1,0),"S":(1,0),"W":(0,-1),"E":(0,1)}
invdir = {"N":"S","E":"W","S":"N","W":"E"}

pipes:dict[str,dict[str,list[str]]] = DefaultDict(dict)
for s,dirs in splitters.items():
    for d in directions:
        if d in dirs:
            pipes[s][d] = [d]
        else:
            pipes[s][d] = list(dirs)

for r,(d1,d2) in reflectors.items():
    for d in directions:
        de = invdir[d]
        if de in d1:
            pipes[r][d] = list(other(tuple(d1),de))
        else:
            pipes[r][d] = list(other(tuple(d2),de))

for d in directions:
    pipes['.'][d] = d

# print(pipes)

def part1(input,start=((0,-1),"E")):
    grid = str_ndarray(input) if not isinstance(input,np.ndarray) else input
    beams = [start]
    visited = set()
    bounds = np_bounds(grid)
    l = [["."]*grid.shape[1] for g in range(grid.shape[0])]
    total = set()
    while beams:
        # print(len(beams))
        pos,dir = beams.pop()
        pos = np.add(pos,directions[dir])
        if (tuple(pos),dir) in visited or pos not in bounds:
            continue
        visited.add((tuple(pos),dir))
        total.add(tuple(pos))
        # l[pos[0]][pos[1]] = "#"
        # print(np.array(l))
        # builtins.input()
        # print(pipes[grid[*pos]])
        # print(grid[*pos])
        for d in pipes[grid[*pos]][dir]:
            beams.append((pos,d))
    # l = [["."]*grid.shape[1] for g in range(grid.shape[0])]
    # for v in total:
    #     l[v[0]][v[1]] = "#"
    # print(np.array(l))
    # print(grid)
    return len(total)
    pass

def part2(input):
    gr = str_ndarray(input)
    g = gr.shape
    m = (None,-1)
    for row in lqdm(range(g[0])):
        start = ((row,-1),"E")
        a = part1(gr,start)
        if a > m[1]:
            m = (start,a)
        start = ((row,g[1]),"W")
        a = part1(gr,start)
        if a > m[1]:
            m = (start,a)
    for col in lqdm(range(g[1])):
        start = ((-1,col),"S")
        a = part1(gr,start)
        if a > m[1]:
            m = (start,a)
        start = ((g[0],col),"N")
        a = part1(gr,start)
        if a > m[1]:
            m = (start,a)

    return m[1]



if __name__ == "__main__":
    input_data = get_input()
    test_data = get_input("test.txt")

    part = "1"
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