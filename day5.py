from collections import UserDict
from contextlib import redirect_stdout
import io
import itertools
from typing import Iterator, Mapping
from imports import *
input_data = get_input()#"input.txt")

seeds = list(map(int,input_data[0].split(": ")[1].split(" ")))
seeds = [range(k,k+l) for k,l in [(seeds[2*i],seeds[2*i+1]) for i in range(int(len(seeds)/2))]]

rem = iter(input_data[2:])

keys = ['seed','soil','fertilizer','water','light','temperature','humidity','location']
maps = DefaultDict[tuple[str,str],list[tuple[int,int,int]]](list)
try:
    while True:
        source,dest = next(rem).split(" map:")[0].split("-to-")
        while (n := next(rem)) != "":
            maps[(source,dest)].append(tuple(map(int,n.split(" "))))
except StopIteration:
    pass

print(maps['seed','soil'])

# class PassDict[K](dict[K,K]):
#     def __missing__(self, key:K):
#         return key

def splitrange(r:range,k:int):
    if k >= r.stop:
        return (r,None)
    elif k < r.start:
        return (None,r)
    else:
        return (range(r.start,k),range(k,r.stop))

    
class RangeDict(Mapping[Iterable[range],Iterable[range]]):
    def __init__(self,*ranges:tuple[range,range]):
        self.ranges = list(ranges)

    def __iter__(self) -> Iterator[Iterable[range]]:
        return super().__iter__()
    
    def __len__(self) -> Iterable[range]:
        return super().__len__()

    def __getitem__(self, key: Iterable[range]) -> Iterable[range]:
        ctx = redirect_stdout(io.StringIO())
        with ctx:
            remranges = [*key]
            for ri,ro in self.ranges:
                nranges:list[range] = []
                # print("splitting by",ri)
                for rem in remranges:
                    # print("rem",rem)
                    r = splitrange(rem,ri.start)
                    # print("split1",r)
                    if r[0]:
                        nranges.append(r[0])
                    if r[1]:
                        r = splitrange(r[1],ri.stop)
                        # print("split2",r)
                        if r[1]:
                            nranges.append(r[1])
                        if (r := r[0]):
                            #r now fully contained within ri
                            r = range(r.start - ri.start + ro.start, r.stop - ri.start + ro.start)
                            # print("mapped",r)
                            yield r
                # print("nranges",nranges)
                remranges = nranges
            yield from remranges
    
    def __repr__(self):
        return repr(self.ranges)
        



dicts:dict[tuple[str,str],RangeDict] = DefaultDict(RangeDict)

for m,ranges in tqdm(maps.items()):
    d = dicts[m]
    for r in ranges:
        d.ranges.append((range(r[1],r[1]+r[2]),range(r[0],r[0]+r[2])))
# print(dicts['seed','soil'])

# from IPython import embed; embed()
# print(seeds)

dicts = dict(dicts)
ress:list[list[range]] = []
for s in tqdm(seeds):
    s = [s]
    for k in lqdm(itertools.pairwise(keys)):
        # print(k)
        # print(s)
        # print(dicts[k])
        s = list(dicts[k][s])
    ress.append(s)
# print(ress)
m = [min([r0.start for r0 in r]) for r in ress]
# print(m)
res = min(m)

# print(seeds)
# exit()
# res = min(min(s) for s in seeds)
# print(res)
# submit_answer(res,part='b')

# submit_answer(res,part='b')