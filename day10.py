from imports import *
from bidict import bidict

pipes = {'.':"",'|':"NS","-":"EW","F":"ES","J":"WN","L":"NE","7":"WS"}
directions = {"N":(-1,0),"S":(1,0),"W":(0,-1),"E":(0,1)}
invdir = {"N":"S","E":"W","S":"N","W":"E"}

def get_path(input):

    grid = np.array([np.array(list(i)) for i in input])
    bounds = grid.shape
    print(bounds)



    start = next(zip(*np.where(grid=="S")))
    start = (start[0],start[1])
    print(start)

    starts:list[tuple[tuple[int,int],str]] = []
    for dir,off in directions.items():
        print(dir,off)
        if invdir[dir] in pipes[grid[*(s := np.add(start,off))]]:
            starts.append((tuple(s),invdir[dir]))
            continue
        print(s,grid[*s])
        print(invdir[dir],pipes[grid[*s]])

    curr:tuple[int,int] = starts[0][0]
    last:str = starts[0][1]

    yield curr
    while np.any(curr != start):
        dirs = pipes[grid[*curr]]
        dirs = dirs.strip(last)
        assert len(dirs) == 1,f"{pipes[grid[*curr]]} {dirs} {last}"
        last = invdir[dirs]
        curr = np.add(curr,directions[dirs])
        yield curr

def part1(input):
    return len(list(get_path(input)))
    


    # pass

def part2(input):
    p = list(get_path(input))
    grid = np.array([np.array(list(i)) for i in input])

    g = np.zeros(grid.shape)
    
    g[[tuple(l) for l in p]] = 1 #boundary
    

    g[grid != '.'] = -1 #non-ground
    pass

input_data = get_input()
test_data = get_input("test.txt")

part = "1"
# part = "2"

if part == "1":
    p = part1(input_data)
    # print(part1(test_data))
    submit_answer(p,part='a')
else:
    p = part2(input_data)
    print(part2(test_data))
    submit_answer(p,part='a')