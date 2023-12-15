from _imports import *

def part1(input):
    pass

def part2(input):
    pass

if __name__ == "__main__":
    input_data = get_input()
    test_data = get_input("test.txt")

    part = "1"
    # part = "2"

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