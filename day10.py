from itertools import chain
import math
from imports import *
from more_itertools import SequenceView, peekable, spy, value_chain

from utils import np_bounds

pipes = {'|':"NS","-":"EW","F":"ES","J":"WN","L":"NE","7":"WS",'.':""}
sides = {'|':"EW","-":"SN","F":("","WN"),"J":("","SE"),"L":("","SW"),"7":("NE","")}
directions = {"N":(-1,0),"S":(1,0),"W":(0,-1),"E":(0,1)}
invdir = {"N":"S","E":"W","S":"N","W":"E"}
order = "NESW"
reverse_pipes = {frozenset(v):k for k,v in pipes.items()}

# l = [1,2,3,4,5]
# l2 = {1:2,2:3,"a":1,3:4,4:5}

# l2[0]

def get_path(input):

    grid = np.array([np.array(list(i)) for i in input])
    bounds = grid.shape
    print(bounds)



    start:tuple[int,int] = next(zip(*np.where(grid=="S")))
    start = (start[0],start[1])
    print(start)

    starts:list[tuple[tuple[int,int],str]] = []
    for dir,off in directions.items():
        # print(dir,off)
        if invdir[dir] in pipes[grid[*(s := np.add(start,off))]]:
            starts.append((tuple(s),invdir[dir]))
            continue
        # print(s,grid[*s])
        # print(invdir[dir],pipes[grid[*s]])

    curr:tuple[int,int] = starts[0][0]
    last:str = starts[0][1]
    yield start,invdir[last]

    while np.any(curr != start):
        dirs = pipes[grid[*curr]]
        dirs = dirs.strip(last)
        assert len(dirs) == 1,f"{pipes[grid[*curr]]} {dirs} {last}"
        yield curr,dirs ##the yield is here so that it doesn't yield the last element, and always returns "current pipe", "current direction"
        last = invdir[dirs]
        curr = np.add(curr,directions[dirs])
        

def part1(input):
    return math.ceil(len(list(get_path(input)))/2)
    


    # pass

def part2(input):
    

    grid = np.array([np.array(list(i)) for i in input])
    
    def turn_dir(prevdir,currdir):
        o1,o2 = order.index(prevdir),order.index(currdir)
        match (o1-o2) % 4:
            case 0 | 2:
                return 0
            case 1:
                return 1
            case 3:
                return -1
            case _:
                raise ValueError()

    
    ##two goals: mark the boundary on the grid and get the turning direction of the path
    g = np.zeros(grid.shape)    
    path = get_path(input)
    acc_turn = 0 #accumulated turning angle
    last_dir:str = ""
    (start,),path = spy(path,1)
    path = chain(path,[start])

    disp_grid = np.copy(grid)
    
    flood_starts:tuple[list[tuple[int,int]],list[tuple[int,int]]] = ([],[])
    for p,dir in path:
        # print(grid[*p])
        # iembed()
        
        g[*p] = 1 #boundary = 1
        if last_dir is not None:
            acc_turn += turn_dir(last_dir,dir)

        c = grid[*p]
        if c == "." or c not in pipes:
            if last_dir != "":
                print(last_dir,dir)
                c = "".join(reverse_pipes[frozenset([invdir[last_dir],dir])])
                # disp_grid[p] = c
                # print(c)
            else:
                continue
        for direction in [0,1]:
            flood_starts[direction].extend([(p[0]+directions[d][0],p[1]+directions[d][1]) for d in sides[c][pipes[c].index(dir) ^ direction]])
        last_dir = dir
        

    acc_turn += turn_dir(last_dir,start[1])
    print(acc_turn)

    handed = 1 if acc_turn > 0 else 0
    print(np.array(flood_starts[handed]).T.dtype)
    
    flood = []
    for p in flood_starts[handed]:
        if p in np_bounds(g) and g[p] != 1:
            flood.append(p)
            
    
    for f in SequenceView(flood):
        g[f] = 2 #2 = flooded
        if disp_grid[f] == '.':
            disp_grid[f] = "I"
        for off in directions.values():
            p:tuple[int,int] = tuple(np.add(f,off))
            if p in np_bounds(g) and g[p] not in [1,2]:
                flood.append(p)
    
    # g[grid != '.'] = -1 #non-ground
    with np.printoptions(linewidth=1000):
        print("\n".join(["".join(c) for c in disp_grid]))
        print(g)
    res = np.sum(g == 2)
    print(res)
    
    # grid[tuple(np.array(flood_starts[handed]).T)] = 2
    
    return res


print(reverse_pipes)
input_data = get_input()
test_data = get_input("test.txt")

part = "1"
part = "2"

if part == "1":
    p = part1(input_data)
    # print(part1(test_data))
    submit_answer(p,part='a')
else:
    p = part2(input_data)
    print(part2(test_data))
    submit_answer(p,part='b')