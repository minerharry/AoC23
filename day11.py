import math
from more_itertools import SequenceView
from _imports import *
from utils import str_ndarray
mt = "."
gal = "#"

test = False

def expand_grid(grid:np.ndarray):
    new_grid = []
    for i in range(grid.shape[0]):
        if np.all(grid[i]==mt):
            new_grid.append(grid[i])
        new_grid.append(grid[i])
    
    grid = np.array(new_grid)
    new_grid = []
    for j in range(grid.shape[1]):
        if np.all(grid[:,j]==mt):
            new_grid.append(grid[:,j])
        new_grid.append(grid[:,j])
    
    return np.array(new_grid).T

def part1(input):
    grid = str_ndarray(input)
    grid = expand_grid(grid)

    galaxies = list(zip(*np.where(grid==gal)))
    res = 0
    for g1,g2 in itertools.combinations(galaxies,2):
        dist = sum(abs(g1i-g2i) for g1i,g2i in zip(g1,g2))
        res += dist
    return res
    
        

def part2(input,expand=1000000):
    grid = str_ndarray(input)
    crit_rows = [r for r in range(grid.shape[0]) if np.all(grid[r] == mt)]
    crit_cols = [r for r in range(grid.shape[1]) if np.all(grid[:,r] == mt)]
    print(crit_rows)

    galaxies = list(zip(*np.where(grid==gal)))
    res = 0
    for g1,g2 in itertools.combinations(galaxies,2):
        ranges = [range(e1,e2,np.sign(e2-e1) if e1 != e2 else 1) for e1,e2 in zip(g1,g2)]
        # dist = [abs(g1i-g2i) for g1i,g2i in zip(g1,g2)]
        # for c in crit_rows:
        #     if c in ranges[0]:
        #         dist +=
        
        dist = []
        for e1,e2,crit,rang in zip(g1,g2,[crit_rows,crit_cols],ranges):
            # print(e1,e2,rang,crit)
            d = abs(e1-e2)
            for c in crit:
                if c in rang:
                    d += expand - 1
            dist.append(d)
        res += sum(dist)
    return res
    # pass

input_data = get_input()
test_data = get_input("test.txt")

part = "1"
part = "2"

if part == "1":
    p = part1(input_data)
    print(part1(test_data))
    submit_answer(p,part='a')
else:
    p = part2(input_data)
    print(part2(test_data,expand=100))
    submit_answer(p,part='b')