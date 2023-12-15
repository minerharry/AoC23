from functools import cache
from _imports import *
from joblib import Memory

m = Memory("cache.mem",verbose=0)
m.clear()
class Cachehit(RuntimeError):
    pass

def dec(m):
    def call(*args,**kwargs):
        if m.check_call_in_cache(*args, **kwargs):
            # pass
            raise Cachehit()
        return m(*args,**kwargs)
    return call


def shift_rocks_north(input:np.ndarray,reverse=False):
    for c in range(input.shape[1]):
        # print(c)
        # print(input[:,c])
        col = "".join(input[:,c])
        # print(col)
        blocks = col.split("#")
        newblocks = []
        for b in blocks:
            if reverse:
                newblocks.append("."*b.count(".")+"O"*b.count("O"))
            else:
                newblocks.append("O"*b.count("O")+"."*b.count("."))
        newcol = "#".join(newblocks)
        # print(newcol)
        input[:,c] = np.array(list(newcol))
        # print(input[:,c])
    return input

cache_checker = dec(m.cache(shift_rocks_north))

def get_load(rocks):
    res = 0
    for i,row in enumerate(rocks):
        res += (rocks.shape[0]-i)*np.sum(row == "O")
    return res


def part1(input):
    rocks = shift_rocks_north(str_ndarray(input))
    res = 0
    print(rocks)
    return get_load(rocks)

def part2(input):
    rocks = str_ndarray(input)
    cache_found = False
    i = 0
    limit = 1000
    t = tqdm(total=limit)
    while i < limit:
        i += 1
        t.update(1)
        tqdm.write(str(get_load(rocks)))
        if not cache_found:
            try:
                rocks = cache_checker(rocks)
            except Cachehit:
                print("cache hit!","cycle length:",i)
                offset = limit % i
                t.update(limit-offset)
                limit = offset
                
                i = 0
                cache_found = True
                continue
        else:
            rocks = shift_rocks_north(rocks)
        
        rocks = shift_rocks_north(rocks.T).T
        rocks = shift_rocks_north(rocks,reverse=True)
        rocks = shift_rocks_north(rocks.T,reverse=True).T

    return get_load(rocks)

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