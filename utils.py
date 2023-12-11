from collections import Counter
from _collections_abc import Container

import numpy as np


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

class np_bounds(Container[tuple[int,...]]):
    def __init__(self,arr:np.ndarray):
        self.arr = arr
        super().__init__()

    def __contains__(self, __x: tuple[int,...]) -> bool:
        ##this is stupid
        try:
            self.arr[__x]
            return True
        except IndexError:
            return False