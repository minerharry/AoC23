from copy import copy
import enum
from tabnanny import check
from typing import Generator, NamedTuple, Self
from more_itertools import first

from numpy import isin
from _imports import *
from distutils import extension

axes = ["x","y","z"]

# class Brick(NamedTuple):
#     origin: tuple[int,int,int]
#     axis: int
#     length: int

#     @functools.cache
#     def blocks(self)->list[tuple[int,int,int]]:
#         o = np.array([0,0,0])
#         o[self.axis] = 1
#         res = []
#         for i in range(self.length):
#             res.append(tuple(np.add(o*i,self.origin)))
#         return res
    
#     def shifted(self,offset:tuple[int,int,int]):
#         return Brick(addtuple(self.origin,offset),self.axis,self.length)
    
#     def intersects(self,other:Self):
#         return not set(self.blocks()).isdisjoint(other.blocks())

#     def __contains__(self, k:tuple[int,int,int]) -> bool:
#         return k in self.blocks()
    
def range_intersection(x:range,y:range):
    return range(max(x[0], y[0]), min(x[-1], y[-1])+1)

class Brick:
    def __init__(self,pos:tuple[int,int,int]|tuple[range,range,range],axis:int,length:int|None=None):
        if isinstance(pos[0],range):
            self.extents:tuple[range,range,range] = pos
            self.axis = axis
            return
        self.extents = [range(p,p+1) for p in pos]
        self.extents[axis] = range(self.extents[axis].start,self.extents[axis].start+length)
        self.extents = tuple(self.extents)
        self.axis = axis

    def __eq__(self,other:Self):
        return self.extents == other.extents
    
    def __hash__(self) -> int:
        return hash(self.extents)
    

    def __repr__(self) -> str:
        return tuple((x[0] if i != self.axis else x for i,x in enumerate(self.extents))).__str__()
    
    def __str__(self) -> str:
        return tuple((x[0] if i != self.axis else x for i,x in enumerate(self.extents))).__str__()
        

    # @functools.cache
    # def blocks(self)->list[tuple[int,int,int]]:
    #     o = np.array([0,0,0])
    #     o[self.axis] = 1
    #     res = []
    #     for i in range(self.length):
    #         res.append(tuple(np.add(o*i,self.origin)))
    #     return res
    
    # # def shifted(self,offset:tuple[int,int,int]):
    #     return Brick(addtuple(self.origin,offset),self.axis,self.length)
    
    def shiftz(self,dist:int):
        return Brick((self.extents[0],self.extents[1],range(self.extents[2].start+dist,self.extents[2].stop+dist)),self.axis)

    def intersects(self,other:Self,check_z=True):
        for i in range(3 if check_z else 2):
            if not range_intersection(other.extents[i],self.extents[i]):
                return False
        return True
    
    def inshadow(self,other:Self):
        return other.intersects(self,check_z=False)
    
    def distance_above(self,other:Self):
        """distance between bottom of self and top of other"""
        if not other.inshadow(self):
            return None
        elif other.intersects(self):
            raise ValueError("Intersecting blocks!")
        else:
            return self.extents[2].start - other.extents[2].stop + 1
        



    

def settle_bricks(input):
    bricks:list[Brick] = []
    for l in input:
        p1,p2 = l.split("~")
        p1:tuple[int,int,int] = tuple(map(int,p1.split(",")))
        p2:tuple[int,int,int] = tuple(map(int,p2.split(",")))
        diff = subtuple(p1,p2)
        x = np.nonzero(diff)[0]
        # print(x)
        axis = x[0] if len(x) > 0 else 0
        origin = p2 if diff[axis] > 0 else p1
        length = abs(diff[axis])+1
        bricks.append(Brick(origin,axis,length))

    supports:dict[int,set[int]] = DefaultDict(set)

    for i,b in enumerate(bricks):
        for j,o in enumerate(bricks):
            if i == j:
                continue
            dist = b.distance_above(o)
            if dist is None:
                continue
            elif dist >= 0: #o below b by some nonzero distance; means b is ""supported"" by o
                supports[i].add(j)
    
    
    open = list(range(len(bricks)))
    settled:list[int] = []
    # e = everyn(1000)

    open_supports = {k:copy(supports[k]) for k in range(len(bricks))}
    # print(open_supports)

    while open:
        for i in open:
            if len(open_supports[i]) == 0:
                index = i
                curr = bricks[i]
                break
        else:
            raise AssertionError("No bricks to drop!")
        
        #clear from open
        open.remove(index)
        del open_supports[index]
        for v in open_supports.values():
            try:
                v.remove(index)
            except KeyError:
                continue

        tofloor =-curr.extents[2].start
        dist_to_lower = tofloor #to floor = 0
        for l in settled:
            l = bricks[l]
            dist_to_lower = max(dist_to_lower,-(curr.distance_above(l) or -tofloor))
        
        bricks[index] = (curr.shiftz(dist_to_lower+1))
        settled.append(index)

    direct_supports:dict[int,set[int]] = DefaultDict(set)

    for i,s in supports.items():
        b = bricks[i]
        for j in s:
            o = bricks[j]
            if b.distance_above(o) == 1: #touching
                direct_supports[i].add(j)
    
    print("indirect",supports)
    print("direct",direct_supports)
    # iembed()
    return bricks,supports,direct_supports



    # def __contains__(self, k:tuple[int,int,int]) -> bool:
    #     return k in self.blocks()

def part1(input):
    bricks,supports,direct_supports = settle_bricks(input)
    
    needed = set()
    for b,s in tqdm(direct_supports.items()):
        if len(s) == 1: #would be <=, but unsupported bricks are sitting on the ground and have no supports
            needed.add(s.pop())
    print(needed)


def part2(input):
    bricks,_,direct_supports = settle_bricks(input)

    supportedby:dict[int,set[int]] = DefaultDict(set) ##inverted direct_supports; B is A in supports[B]  means A is supporting B; B in supportedby[A] means B is supported by A
    for i,s in direct_supports.items(): #inv
        for j in s:
            print(i,j,s)
            supportedby[j].add(i)

    # print(supportedby)

    res = 0
    for i,b in tqdm(enumerate(bricks)):
        #what happens if we delete it?
        all_affected = set([i])
        consequences = set([i])
        while consequences:
            c = consequences.pop()
            for s in supportedby[c]: #this relies on the fact that there are no simultaneous supports; that is, if A supports B and A supports C, B can't also support C because they are rectangles
                # print(i,c,s,direct_supports[s],all_affected)
                if len(direct_supports[s].difference(all_affected)) == 0:
                    if s in all_affected:
                        continue
                    consequences.add(s)
                    all_affected.add(s)
                    # print("w")
                
            # consequences.update([s for s in supportedby[i] if len(supports[s].difference(all_affected)) == 0])
        all_affected.remove(i)
        # print(i,all_affected)
        res += len(all_affected)

    return res

        

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