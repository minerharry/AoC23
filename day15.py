from typing import OrderedDict
from _imports import *

def HASH(s:str):
    curr = 0
    for r in s:
        curr += ord(r)
        curr *= 17
        curr %= 256
    return curr

def part1(input):
    s = "".join(input)
    res = 0
    for b in s.split(","):
        h = HASH(b)
        res += h
    return res

def part2(input):
    boxes:dict[int,OrderedDict[str,int]] = DefaultDict(OrderedDict)
    s = "".join(input)
    for b in s.split(","):
        if "-" in b:
            op = b.split("-")[0]
            box = HASH(op)
            if op in boxes[box]:
                del boxes[box][op]
        else:
            op,num = b.split("=")
            num = int(num)
            box = HASH(op)
            boxes[box][op] = num
        # print(boxes)
    res = 0
    for b,box in boxes.items():
        for i,(op,l) in enumerate(box.items()):
            res += (b+1)*(i+1)*l
    return res

if __name__ == "__main__":
    input_data = get_input()
    test_data = get_input("ttest.txt")

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