# from imports import .s*
import text
import re
arr = text.get_input("input.txt")

def issymbol(s:str):
    if len(s) != 1: raise Exception()
    # print(s)
    return (s != '.' and not s.isdigit())

def get_neighbors(row:int,col:int):
    o = [(-1,0),(-1,-1),(-1,1),(0,1),(0,-1),(1,-1),(1,1),(1,0)]
    for o1,o2 in o:
        if o1 + row < 0:
            continue
        if o2 + col < 0:
            continue
        try:
            yield arr[o1+row][o2+col]
        except:
            pass
# parts = []
partidx = []
for r in range(len(arr)):
    for c,el in enumerate(arr[r]):
        if el == "*":
            partidx += list(get_neighbors(r,c))
        # if any([issymbol(v) for v in get_neighbors(r,c)]):
        #     # print(el)
        #     partidx.append((r,c))
            # parts.append(arr[r][c])
# print(parts)
print(partidx)

nums:list[tuple[tuple[int,int],int,int]] = []
for r,row in enumerate(arr):
    idx = 0
    for n in re.split('[^0-9]',row):
        # print(repr(n))
        if n.isdigit():
            nums.append(((r,idx),len(n),int(n)))
        idx += len(n) + 1
# print(nums)

parts = []
for n in nums:
    for k in range(n[0][1],n[0][1]+n[1]):
        # print(n)
        # print(k)
        if (n[0][0],k) in partidx:
            parts.append(n[2])
            break

print(parts)
print(sum(parts))
        

print(list(get_neighbors(0,2)))