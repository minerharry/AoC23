from imports import *
p = Puzzle(2023,2)
input_data = get_input(puzzle=p)
# input_data = get_input("test.txt")

limit = {"red":12,"green":13,"blue":14}

ss = []
for l in input_data:
    name,i = l.split(": ")
    id = int(name.split("Game ")[1])
    os = i.split("; ")
    possible = True
    mins = {'red':0,'green':0,"blue":0}
    for o in os:
        for m in o.split(", "):
            num,color = m.split(" ")
            num = int(num)
            mins[color] = max(num,mins[color])
            # if num > limit[color]:
            #     possible = False
            #     break
    
    power = mins['red']*mins['blue']*mins["green"]

    # if possible:
    ss.append(power)
print(ss)
print(sum(ss))
submit_answer(sum(ss),part='b',puzzle=p)