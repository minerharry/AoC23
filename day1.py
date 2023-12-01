from imports import *
p = Puzzle(2023,1)
input_data = get_input(puzzle=Puzzle(2023,1))

su = []
names = ['one','two','three','four','five','six','seven','eight','nine']

part:Literal[1,2] = 2
for s in input_data.split('\n'):
    print(f'input: {s}')
    st = ""
    for i in range(len(s)):
        o1 = s[:i+1]
        # print(o)
        if o1[-1].isdigit():
            st += o1[-1]
        elif part == 2:
            for k in range(len(o1)-1,-1,-1):
                o = o1[k:]
                for n in names:
                    o = o.replace(n,str(names.index(n)+1))
                if o[-1].isdigit():
                    st += o[-1]

    print(s)
    su += [int(s[0]+s[-1])]
    print(int(s[0]+s[-1]))

with open('out.txt','w') as f:
    for s in su:
        f.write(f"{s}\n")

s = (sum(su))

submit_answer(s,part='b')
