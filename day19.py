from typing import NamedTuple

from numpy import clip, isin
from _imports import *


class Datum(NamedTuple):
    x:int
    m:int
    a:int
    s:int

class RangeDatum(NamedTuple):
    x:range
    m:range
    a:range
    s:range

class WorkFlow:
    def __init__(self,src:str):
        self.name = src.split("{")[0]
        body = src.split("{")[1].rstrip("}").split(",")
        self.flow:list[tuple[str,str|bool]] = []
        for b in body:
            if ":" in b:
                cond,res = b.split(":")
                
            else:
                cond = "True"
                res = b
            if res == "A":
                res = True
            elif res == "R":
                res = False
            else:
                res = res
            self.flow.append((cond,res))
        
    def eval(self,t:Datum):
        for cond,res in self.flow:
            if eval(cond,t._asdict(),{}):
                return res
        raise ValueError()


class RangeWorkFlow:
    def __init__(self,src:str):
        self.name = src.split("{")[0]
        body = src.split("{")[1].rstrip("}").split(",")
        self.flow:list[tuple[tuple[str,int,str]|None,str|bool]] = []
        for b in body:
            if ":" in b:
                condstr,res = b.split(":")
                for c in [">","<"]:
                    if c in condstr:
                        sp = condstr.split(c)
                        cond = (sp[0],int(sp[1]),c)
                        break
                else:
                    raise Exception()
            else:
                cond = None
                res = b
            if res == "A":
                res = True
            elif res == "R":
                res = False
            else:
                res = res
            self.flow.append((cond,res))
        
    def eval(self,data:RangeDatum):
        if size(data) == 0:
            return []
        d:dict[str,range] = data._asdict()
        result:list[tuple[bool|str,RangeDatum]] = []
        for cond,res in self.flow:
            if cond is None:
                result.append((res,RangeDatum(**d)))
            else:
                char,lim,dir=cond
                r = d[char]
                if dir == ">":
                    lim += 1
                lim = clip(lim,r.start,r.stop)
                sr,nr = [range(r.start,lim ), range(lim,r.stop)][::1 if dir == ">" else -1]
                for i in r:
                    if dir == ">":
                        if i > cond[1]: ##condition holds
                            assert i in nr,iembed()
                            assert i not in sr
                        else:
                            assert i in sr,iembed()
                            assert i not in nr
                    else:
                        if i < cond[1]:
                            assert i in nr
                            assert i not in sr
                        else:
                            assert i in sr,iembed()
                            assert i not in nr
                    assert i in sr or i in nr,iembed() #conservation of range
                r = sr
                # iembed()
                d[char] = r
                result.append((res,RangeDatum(**d)._replace(**{char:nr}))) #stupid
        return result
    
def processdatum(flows,datum):
    curr = "in"
    while not isinstance(curr,bool):
        curr = flows[curr].eval(datum)
    return curr

def part1(input):
    flows,parts = splitlist(input,"")
    fl:dict[str,WorkFlow] = {}
    for f in flows:
        w = (WorkFlow(f))
        fl[w.name] = w
    par:list[Datum] = [eval(f"Datum({p.strip("{}")})") for p in parts]
    res = 0
    for p in par:
        if processdatum(fl,p):
            res += sum(p)
    return res


def size(d:RangeDatum):
    return len(d.x)*len(d.m)*len(d.a)*len(d.s)

def part2(input):
    flows,_ = splitlist(input,"")
    fl:dict[str,RangeWorkFlow] = {}
    for f in flows:
        # print(f)
        w = (RangeWorkFlow(f))
        fl[w.name] = w
    limit = 4000
    res = 0
    open:list[tuple[str,RangeDatum]] = [("in",RangeDatum(*(range(1,limit+1) for _ in range(4))))]
    while open:
        dest,datum = open.pop()
        for newdest,ndatum in fl[dest].eval(datum):
            if isinstance(newdest,bool):
                if newdest:
                    res += size(ndatum)
            else:
                open.append((newdest,ndatum))
    return res
        
                



    pass

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