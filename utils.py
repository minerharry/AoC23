import builtins
from collections import Counter
from _collections_abc import Container
import contextlib
import functools
import io
import math
from numbers import Number
from operator import index
from os import remove
from typing import TYPE_CHECKING, Callable, Iterable, Iterator, MutableSequence, Sequence

import numpy as np
from tqdm import tqdm


def splitlist(list,delimiter):
    if delimiter not in list:
        return [list];
    idx_list = [idx + 1 for idx, val in enumerate(list) if val == delimiter]
    size = len(list);
    return [list[i: j-1] for i, j in
        zip([0] + idx_list, idx_list +
        ([size+1] if idx_list[-1] != size else []))]

def rotatePos(p,rot,size):
    rot %= 4;
    if rot == 0:
        return p;
    return rotatePos((p[1],size-p[0]-1),rot-1,size);

def mDist(p1:tuple[int,int],p2:tuple[int,int]):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1]);

def most_frequent(l:list):
    occurence_count = Counter(l)
    return occurence_count.most_common(1)[0][0]

def str_ndarray(inp:list[str]):
    return np.array([np.array(list(i)) for i in inp])

class np_bounds(Container[tuple[int,...]]):
    def __init__(self,arr:np.ndarray,allow_negative:bool=False):
        self.neg_ok = allow_negative
        self.arr = arr
        super().__init__()

    def __contains__(self, __x: tuple[int,...]) -> bool:
        ##this is stupid
        if not self.neg_ok and not all([xi >= 0 for xi in __x]):
            return False
        try:
            self.arr[__x]
            return True
        except IndexError:
            return False

    def wrap[*P](self,x:tuple[*P])->tuple[*P]:
        return tuple([x % s for x,s in zip(x,self.arr.shape)])
    
    def off[*P](self,x:tuple[*P])->tuple[*P]:
        return tuple((x//s for x,s in zip(x,self.arr.shape)))
        # return tuple((np.sign(q)*math.ceil(abs(q)) for q in s))
    
def addtuple[*T](*t:tuple[*T])->tuple[*T]:
    return tuple(sum(ts) for ts in zip(*t))

def subtuple[*T](t1:tuple[*T],t2:tuple[*T])->tuple[*T]:
    return tuple(t01-t02 for (t01,t02) in zip(t1,t2))
        
@contextlib.contextmanager
def redirect_to_tqdm():
    # Store builtin print
    old_print = print
    def new_print(*args, **kwargs):
        # If tqdm.tqdm.write raises error, use builtin print
        try:
            tqdm.write(*args, **kwargs)
        except:
            old_print(*args, ** kwargs)

    try:
        # Globaly replace print with new_print
        builtins.print = new_print
        yield
    finally:
        builtins.print = old_print

if TYPE_CHECKING:
    lqdm = tqdm
else:
    lqdm = functools.partial(tqdm,leave=False)

@functools.wraps(range)
def trange(*args,**kwargs):
    return tqdm(range(*args),**kwargs)

no_print = contextlib.redirect_stdout(io.StringIO())


def other[A,B](t:tuple[A,B],s:A|B):
    return t[t.index(s)-1]


def everyn[T](n:int):
    count = 0
    def dof(f:Callable[[],T]):
        nonlocal count
        try:
            if count == 0:
                return f()
            else:
                return None
        finally:
            count = (count + 1) % n
    return dof

# class Ringable(Protocol):
#     def __add__(self,o:Self|Literal[0])->Self|Literal[0]:...
#     def __sub__(self,o:Self|Literal[0])->Self|Literal[0]:...
#     def __abs__(self)->Self:...

def taxicab[T:float|int](__p: Iterable[T], __q: Iterable[T]) -> T:
    res = 0
    for p,q in zip(__p,__q):
        x = p - q
        res += abs(x)
    return res

import time
# https://stackoverflow.com/a/39858851/13682828
class StopWatch:
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0

    def start(self):
        self.start_time = time.time()
        return self.start_time

    def stop(self):
        self.stop_time = time.time()
        return self.stop_time

    def time(self):
        return time.strftime("%H:%M:%S",time.gmtime(time.time() - self.start_time))
    
    def total_time(self):
        return time.strftime("%H:%M:%S",time.gmtime(self.stop_time - self.start_time))
    

def list_sub_index[T](array:MutableSequence[T],slice:range,replace:Iterable[T])->tuple[range,Iterable[T]]:
    ###AXIOMS
    ## returns (out_slice,removed)
    ## before:
    ## removed = array[slice]*
    ## after:
    ## array[out_slice]* = replace
    ## *this slicing doesn't work because negative, but [array[s] for s in slice] does
    ## thus,
    ## len(output slice) == len(replace)
    ## This means:
    ## if an element is consumed from replace:
    ##   len(output slice) should increase
    ## if an element is not consumed from replace:
    ##   len(output slice) should remain the same length; if they change, they should change in lockstep
    assert slice.step == 1
    it = iter(replace)
    ind = slice.start
    removed = []
    assert slice.stop >= 0 
    start = slice.start
    for _ in range(len(slice)): #iterate over the window in the array
        removed.append(array[ind])
        try:
            e = next(it)
            array[ind] = e
            ind += 1
        except StopIteration:
            #no more edges, just remove from the list
            array.pop(ind)
            ##If ind is nonnegative, the later entries will automatically shift themselves down, so no increment necessary.
            ##If negative, though, the length of the list will decrease in step with the removed entries, so the index does need to be incremented
            if ind < 0:
                ind += 1 
                start += 1 #since start is always less than ind, start will also be negative, so it must increase as well

    for e in it: #insert remaining elements into the list
        array.insert(ind,e)
        ind += 1

    out_slice = range(start,ind)
    return (out_slice,removed)




# class ReductionEnumerator[T](Iterator[tuple[int,T]]):
#     def __init__(self,i:Sequence[T],index=0):
#         self.index = 0 
#         self.list = i

#     def __next__(self):
#         res = self.index,self.list[self.index]
#         self.index += 1
#         self.index %= len(self.list)

#     def 

