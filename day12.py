from __future__ import annotations
from ast import literal_eval
from copy import copy
from typing import Any, Generator, Hashable, Iterator, Mapping, Protocol, Self, Sequence, TypeVar, runtime_checkable
import inquirer
from more_itertools import SequenceView, first
import more_itertools
import dill as pickle
from _imports import *
import builtins

def simplify(obj):
    # print(obj)
    if hasattr(obj,"__simple__"):
        s = obj.__simple__()
        # print("simplified:",s)
        return s
    elif isinstance(obj,(str,int,bool,float)):
        return obj
    elif isinstance(obj,Mapping):
        return {simplify(k):simplify(v) for k,v in obj.items()}
    elif isinstance(obj,Sequence):
        if first(obj,None) == obj: #one-length string kinda deal
            return obj
        return tuple([simplify(o) for o in obj])
    else:
        return obj

Q = TypeVar("Q")
@runtime_checkable
class Copyrator(Iterator[Q],Protocol):
    def __copy__(self)->Copyrator[Q]: ...
    def __hash_tuple__(self) -> tuple[Hashable]: ...
    def __eq__(self, __value: Copyrator[Q]) -> bool:
        return hasattr(__value,"__hash_tuple__") and self.__hash_tuple__() == __value.__hash_tuple__()
    def __hash__(self) -> int:
        return hash(self.__hash_tuple__())

class Stringerator(Copyrator[str],Iterable[str]):
    def __init__(self,s:str,start:int=0):
        self.base = s
        self.curr = start

    def __copy__(self)->Self:
        return Stringerator(self.base,start=self.curr)
    
    def __next__(self) -> str:
        self.curr += 1
        try:
            return self.base[self.curr-1]
        except:
            raise StopIteration

    def __simple__(self):
        return (self.__class__,self.base,self.curr)

    def __iter__(self) -> Iterator[str]:
        return self

    def __hash_tuple__(self) -> tuple[Hashable]:
        return (self.curr,)
    
    def string(self) -> str:
        return "".join(self)

BROKEN = "#"
OPERATIONAL = "."
UNKNOWN = "?"
block_match = re.compile(r"(\.*)")
block_match_any = re.compile(r"(#+)")



def dotrue():
    return True

class DelegateTo:
    def __init__(self, to, method=None):
        self.to = to
        self.method = method
    def __get__(self, obj, objecttype):
        if self.method is not None:
            return getattr(getattr(obj, self.to), self.method)

        for method, v in obj.__class__.__dict__.items():
            if v is self:
                self.method = method
                return getattr(getattr(obj, self.to), method)

class TryDelegateTo:
    def __init__(self, to, method:str|None=None, default:str|None=None):
        self.to = to
        self.method:str|None = method
        self.default:str|None = default
    def __get__(self, obj, objecttype):
        if self.method is not None:
            return getattr(getattr(obj, self.to), self.method, getattr(obj,self.default if self.default else self.method))

        for method, v in obj.__class__.__dict__.items():
            if v is self:
                self.method = method
                return getattr(getattr(obj, self.to), method, getattr(obj,self.default if self.default else method))

def prepend[T](it:Copyrator[T],*s:T):
    if isinstance(it,Prepend):
        it.prepend(*s)
        return it
    else:
        return Prepend(it,*s)

null = object() 
T = TypeVar("T")
class Prepend(Copyrator[T]):
    __next__ = TryDelegateTo("it_next",default="next") #type:ignore
    def __init__(self,it:Copyrator[T],*s:T) -> None:
        self.val = list(s)
        # assert isinstance(it,Copyrator),it
        while isinstance(it,Prepend):
            self.val.extend(it.val)
            it = it.it
        self.it = it
        self.it_next = None

    def __getattr__(self, __name: str) -> Any:
        ##delegate any other variables (base,curr) to underlying iterator
        return getattr(self.it,__name)
    
    def prepend(self,*s:T):
        self.val = list(s) + self.val
    
    def next(self) -> T:
        if self.val:
            return self.val.pop()
        else:
            self.it_next = self.it
            return next(self.it)

    def __simple__(self):
        return (self.__class__,tuple(self.val),simplify(self.it))
    
    def __copy__(self) -> Copyrator[T]:
        return copy(self.it_next) if self.it_next else prepend(copy(self.it),*self.val)
    
    def __hash_tuple__(self):
        if self.val:
            return (tuple(self.val),self.it.__hash_tuple__())
        else:
            return self.it.__hash_tuple__()

def trim(springs:Copyrator[str]):
    acc = 0
    for s in springs:
        if s == '.':
            acc += 1
        else:
            springs = prepend(springs,s)
            break
    return springs,acc
from functools import wraps



cache = {}
def cached(func):
    @wraps(func)
    def wrapper(*args):
        try:
            c =  cache[args[:3]]
            print(args,c)
            return c
        except KeyError:
            cache[args] = result = func(*args)
            return result   
    return wrapper

# @cached
# @functools.lru_cache(10000)
def match_blocks_v3(springs:str,lengths:tuple[int,...],buffer:str,history="")->int:
    if len(lengths) == 0:
        if not any(map(lambda x: x == "#",springs)):
            ##successfully consumed all blocks
            print("success",history)
            return 1
        print("fail1",history)
        return 0
    if buffer == "": ##not in the middle of a block, trim
        springs= springs.lstrip(".")
    for i,s in enumerate(springs):
        print("iter",i,s,history)
        inp = builtins.input()
        if inp != "":
            iembed()
        if len(buffer) > lengths[0]:
            print("fail2",history)
            return 0
        if s == "?":
            return match_blocks_v3("#" + springs[i+1:],lengths,buffer,history+"#") \
                 + match_blocks_v3("." + springs[i+1:],lengths,buffer,history+".")
        if s == ".":
            if len(buffer) == lengths[0]:
                return match_blocks_v3(springs[i+1:],lengths[1:],"",history)
            print("fail3",history)
            return 0
        if s == "#":
            buffer += "#"
    print("fail4",history)
    return 0


# @cached
# @functools.lru_cache(10000)
def match_blocks_v2(springs:Copyrator[str],lengths:tuple[int,...],buffer:str,history="")->int:
    if len(lengths) == 0:
        if "#" not in list(springs):
            ##successfully consumed all blocks
            print("success",history)
            return 1
        print("fail1",history)
        return 0
    if buffer == "": ##not in the middle of a block, trim
        springs,acc = trim(springs)
    for i,s in enumerate(springs):
        print("iter",i,s,history)
        inp = builtins.input()
        if inp != "":
            iembed()
        if len(buffer) > lengths[0]:
            print("fail2",history)
            return 0
        if s == "?":
            return match_blocks_v2(prepend(copy(springs),"#"),lengths,buffer,history+"#") \
                 + match_blocks_v2(prepend(copy(springs),"."),lengths,buffer,history+".")
        if s == ".":
            if len(buffer) == lengths[0]:
                return match_blocks_v2(springs,lengths[1:],"",history)
            print("fail3",history)
            return 0
        if s == "#":
            buffer += "#"
    print("fail4",history)
    return 0

def rep(seq:tuple[int],blocks:tuple[int],length:int):
    res = ['.']*(length)
    for i in range(len(seq)):
        res[seq[i]:seq[i]+blocks[i]] = "#"*blocks[i]
    return "".join(res)

def part1(input):
    global cache
    res = 0
    for line in input:
        cache = {}
        # match_blocks_v3.cache_clear()
        springs,blocks = line.split(" ")
        springs += "."
        blocks = literal_eval(blocks)
        tqdm.write("==LINE== " + line)
        m = match_blocks_v3(springs,blocks,"")
        # m = match_blocks_v2(Stringerator(springs),blocks,"")
        assert len(m) == len(set(m)),m
        # print(m)
        # l = len(springs)
        # for e in m:
        #     g = [len(i) for i in re.findall(block_match_any,rep(e,blocks,l))]
        #     assert tuple(g) == blocks,g
        # print([rep(e,blocks,l) for e in m])
        
        tqdm.write(str(m))
        # c = simplify(cache)
        # s = prepend(Stringerator("1,2"),"5")
        # c = simplify(s)
        # c = s.__class__
        # print(c)
        # with open("dump.pkl","wb") as f:
        #     pickle.dump(c,f)
        # iembed()
        # tqdm.write(repr(match_blocks_v3.cache_info()))
        res += m
    return res


    pass

def part2(input):
    expanded = []
    for l in input:
        e1,e2 = l.split(" ")
        e1 = "?".join([e1]*5)
        e2 = ",".join([e2]*5)
        expanded.append(e1 + " " + e2)
    # expanded.append(expanded.pop(0))
    # expanded.insert(0,expanded.pop(16))
    # expanded.append(expanded.pop(3))
    # expanded.pop(0)    
    with redirect_to_tqdm():
        return part1(expanded)

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
        # p = part2(input_data)
        print("=== TEST INPUT ===")
        print(part2(test_data))
        # submit_answer(p,part=2)