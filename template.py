from imports import *

def part1(input):
    pass

def part2(input):
    pass

input_data = get_input()
test_data = get_input("test.txt")

part = "1"
# part = "2"

if part == "1":
    p = part1(input_data)
    print(part1(test_data))
    submit_answer(p,part='a')
else:
    p = part2(input_data)
    print(part2(test_data))
    submit_answer(p,part='a')