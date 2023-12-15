from _imports import *


def get_reflect(grid:np.ndarray,skip:int|None=None):
    ##only check rows
    w = grid.shape[0]
    flip = np.flipud(grid)
    for i in range(1,w):
        if i == skip:
            continue
        ##reflection index is between (i-1,i)
        #flip: clamp(w - 2*i: 2*w - 2*i)
        #grid: clamp(2*i-w:2*i)
        f0 = flip[max(w-2*i,0):2*w-2*i]
        g0 = grid[max(2*i-w,0):2*i]
        # print(f0,g0)
        if np.all(f0 == g0):
            return i
    return None


symbols = ("#",".")
def other(s:Literal["#","."]):
    return symbols[symbols.index(s)-1]

def part1(input:list[str]):
    blocks = splitlist(input,"")
    s = 0
    for b in blocks:
        # print(b)
        grid = np.array([list(s) for s in b])
        reflect = get_reflect(grid.T) or 100*get_reflect(grid)
        # print(reflect)
        s += reflect
    return s

def part2(input):
    blocks = splitlist(input,"")
    s = 0
    for b in blocks:
        grid = np.array([list(s) for s in b])
        print(grid)
        old_reflects = (get_reflect(grid.T),get_reflect(grid))
        reflect = None
        for ind in np.ndindex(grid.shape):
            grid[ind] = other(grid[ind])
            reflects = (get_reflect(grid.T,skip=old_reflects[0]),get_reflect(grid,skip=old_reflects[1]))
            grid[ind] = other(grid[ind])
            if any(reflects):
                reflect = reflects[0] or 100*reflects[1]
                break
        print(reflect)
        s += reflect
    return s
    pass

if __name__ == "__main__":
    # print(get_reflect(np.array([1,2,3,4])))
    # print(get_reflect(np.array([1,2,2,1])))
    # print(get_reflect(np.array([1,1,3,3])))
    
    # exit()

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