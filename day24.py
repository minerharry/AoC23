from calendar import c
from sympy import Mul
from _imports import *
from kingdon import Algebra,MultiVector

# def intersection(h1:tuple[int,int],h2:tuple[int,int]): #position, velocity for a single axis
#     #equation: h1.v*t+h1.p = h2.v*t+h2.p
#     # thus t = (h2.p-h1.p)/(h1.v-h2.v)
#     # and y = h1.v*t+h1.p

#     if h1[1] == h2[1]: #same velocities:
#         return None if h1 == h2 else float('-inf')

#     t = (h2[0]-h1[0])/(h1[1]-h2[1])
#     pos = h1[1]*t+h1[0]
#     return pos

def part1(input:list[str],area=(200000000000000,400000000000000))->int:
    # area = range(area[0],area[1]+1)
    hails:list[tuple[tuple[int,int,int],tuple[int,int,int]]] = []
    for i in input:
        hails.append(tuple([tuple([int(j.strip()) for j in l.split(", ")]) for l in i.split(" @ ")]))
    # print(hails)

    alg = Algebra(2,0,1)
    # print(alg)
    # print(dict(**alg.blades))

    def to_point(x:int,y:int)->MultiVector:
        return alg.blades["e12"] - x*alg.blades["e02"] + y*alg.blades["e01"]

    ahails = []
    for h in hails:
        p1 = to_point(*h[0][:2])
        p2 = to_point(*addtuple(h[0],h[1])[:2])
        line = alg.rp(p1,p2)
        ahails.append(line)

    axes = [0,1]

    res = 0
    for n,h in enumerate(ahails):
        for t,i in enumerate(ahails):
            if t <= n:
                continue
            assert n != t
            # print("woo")
            intersection:MultiVector = alg.op(h,i)
            # print("wow")
            assert intersection.grades == (2,) #only bivectors (points)
            # print("whoa")
            try:
                intersection /= intersection["e12"]
            except ZeroDivisionError:
                print("Lines are parallel; they do not cross")
                #lines are parallel; they meet at a point at infinity
                continue
            # print("whoo")

            x,y = (-intersection["e02"]),intersection["e01"]
            x = float(x)
            y = float(y)

            # print()
            # print(intersection)
            # print("Hailstone A:",input[n])
            # print("Hailstone B:",input[t])
            # print("Paths crossed at",(x,y))

            #check if it's in the past blegh
            try:
                for k in (n,t):
                    for a,p in zip(axes,(x,y)):
                        if (p - hails[k][0][a]) / hails[k][1][a] < 0:
                            # print(k,a,p)
                            #in the past ree
                            raise UserWarning()
            except UserWarning:
                print(f"Crossed in the past for hailstone {["A","B"][(n,t).index(k)]}")
                continue

            # print("weaow")
            # print(type(x),type(y))
            if (area[0] <= x and x <= area[1]) and (area[0] <= y and y <= area[1]):
                print(f"Paths crossed in the test area")
                res += 1
            else:
                print(f"Paths cross outside the test area")
                
            # print("huh?")

            

            # if all([j is None or (area[0] <= j and j <= area[1]) for j in intersect]):
            #     res += 1
            # print(h,i)
            # print(intersect)
    return res




def part2(input:list[str])->int:
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
        print(part1(test_data,area=(7,27)))
        submit_answer(p,part=1)
    else:
        print("=== PUZZLE INPUT ===")
        p = part2(input_data)
        print("=== TEST INPUT ===")
        print(part2(test_data))
        submit_answer(p,part=2)