from imports import *

def part1(input):
    def get_sequence(l:list[int]):
        if np.allclose(l,0):
            return 0
        diff = np.diff(l)
        s = get_sequence(diff)
        return l[-1] + s
    
    res = 0
    for l in input:
        s = map(int,l.split(" "))
        n = get_sequence(list(s))
        res += n
    return res

    pass

def part2(input):
    def get_sequence(l:list[int]):
        if np.allclose(l,0):
            return 0
        diff = np.diff(l)
        s = get_sequence(diff)
        return l[0] - s
    
    res = 0
    for l in input:
        s = map(int,l.split(" "))
        n = get_sequence(list(s))
        print(n)
        res += n
    return res

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
    print(part2(test_data))
    submit_answer(p,part='a')