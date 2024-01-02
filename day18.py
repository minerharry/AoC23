from collections import UserList
from operator import itemgetter
from threading import local
from timeit import timeit
from typing import Final, NamedTuple, Sequence
from numpy import argmin
from _imports import *

directions = {"U":(-1,0),"D":(1,0),"L":(0,-1),"R":(0,1)}
pipes = {'|':"UD","-":"RL","F":"RD","J":"LU","L":"UR","7":"LD",'.':""}
sides = {'|':"RL","-":"DU","F":("","LU"),"J":("","DR"),"L":("","DL"),"7":("UR","")}
directions = {"U":(-1,0),"D":(1,0),"L":(0,-1),"R":(0,1)}
invdir = {"U":"D","R":"L","D":"U","L":"R"}
order = "URDL"
reverse_pipes = {frozenset(v):k for k,v in pipes.items()}


def part1(input):
    trenches:list[list[tuple[int,int]]] = [] 
    edges:set[tuple[int,int]] = set()
    pipe_path:list[tuple[tuple[int,int],tuple[str,str]|None]] = []
    pos = (0,0)
    last_dir = None
    first_dir = None
    nturns = 0

    def turn_dir(prevdir,currdir):
        o1,o2 = order.index(prevdir),order.index(currdir)
        match (o1-o2) % 4:
            case 0 | 2:
                return 0
            case 1:
                return 1
            case 3:
                return -1
            case _:
                raise ValueError()

    for l in tqdm(input):
        d,n,_ = l.split(" ")
        n = int(n)
        trench = [tuple(np.add(pos,np.multiply(directions[d],i+1))) for i in range(n)]
        corner = None if last_dir is None else (last_dir,d)
        if last_dir:
            nturns += turn_dir(last_dir,d)
        if first_dir is None:
            first_dir = d
        trenches.append(trench)
        edges = edges.union(trench)
        pipe_path.append((pos,corner))
        for t in trench[:-1]:
            pipe_path.append((t,(d,d)))
        pos = trench[-1]
        last_dir = d
    
    pipe_path[0] = (pipe_path[0][0],(last_dir,first_dir))
    nturns += turn_dir(last_dir,first_dir)
    assert nturns in (4,-4), nturns
    pipe_path:list[tuple[tuple[int,int],tuple[str,str]]] = pipe_path


    

    indices = np.array(list(edges))
    offset = -np.min(indices,0)
    print("offset",offset)
    print(np.max(indices,0))
    indices += offset
    print(indices.shape)
    print(np.max(indices,0))
    print(np.min(indices,0))
    l = np.zeros(np.max(indices,0)+np.array((1,1)))
    bounds = np_bounds(l)
    for i in edges:
        l[*(i+offset)] = 1
    print(l)

    td = 1 if nturns > 0 else -1
    flood_starts:set[tuple[int,int]] = set()
    for p,(d1,d2) in tqdm(pipe_path):
        
        if d1 == d2:
            if td == 1:
                dirs = [order[order.index(d1)-1]]
            else:
                dirs = [order[(order.index(d1)+1)%4]]
        else:
            if turn_dir(d1,d2) == td:
                dirs = []
            else:
                dirs = [d1,invdir[d2]]

        # y = []
        for d in dirs:
            n = tuple(np.add(p,directions[d])+offset)
            # print(np.subtract(n,offset),n)
            if n in bounds and l[*n] != 1:
                flood_starts.add(n)
                # y.append(n)
        # print(p,(d1,d2),dirs,y)

    for f in flood_starts:
        if l[*f] == 1:
            raise Exception()
        l[*f] = 3
    print(l)

    # flood_starts = set([tuple(np.add(f,offset)) for f in flood_starts])
    e = everyn(100)
    while flood_starts:
        f = flood_starts.pop()
        if l[*f] == 1:
            continue
        e(lambda: print(len(flood_starts),end="\r"))
        l[*f] = 2 #flood
        for d,o in directions.items():
            new = tuple(np.add(f,o))
            if new in bounds:
                if l[*new] not in [1,2]:
                    flood_starts.add(new)
    print(l)

    return np.count_nonzero(l)

def str2hex(s:str):
    n = 0
    hex = "0123456789ABCDEF"
    for i,k in enumerate(s):
        # print(k)
        n += hex.index(k.upper())*(16**(len(s)-1-i))
    return n





class Edge(NamedTuple):
    dir:str
    length:int
    interior:bool

class EdgeList(MutableSequence[Edge]):
    def __init__(self,edges:Iterable[Edge]=[],inv=False):
        self.edges = list(edges)
        self.inverted = inv

    def __repr__(self) -> str:
        return repr([self[k] for k in range(len(self))])

    def invert(self):
        self.inverted ^= True

    def __get(self,e:Edge):
        if self.inverted:
            return Edge(e.dir,e.length,not e.interior)
        return e

    def __getitem__(self,k:int):
        if isinstance(k,slice):
            raise ValueError("can't slice edgelist")
        e = self.edges[k]
        return self.__get(e)
    
    def __setitem__(self,k:int,e:Edge):
        if isinstance(k,slice):
            raise ValueError("can't slice edgelist")
        self.edges[k] = self.__get(e)

    def __contains__(self, e: Edge) -> bool:
        return self.__get(e) in self.edges
        
    def __delitem__(self,i:int):
        del self.edges[i]

    def __len__(self):
        return len(self.edges)
    
    def insert(self,i:int,e:Edge):
        self.edges.insert(i,self.__get(e))

        
        
# EdgeList([])

        


def vis_edges(edges:Sequence[Edge]):
    # print(edges)
    corners = []
    points = set()
    pos = (0,0)
    for e in lqdm(edges,desc="vizzing"):
        corners.append(pos)
        d = e.dir
        n = e.length
        trench = [tuple(np.add(pos,np.multiply(directions[d],i+1))) for i in range(n)]
        points.update(trench)
        pos = trench[-1]
    # print(corners)
    points = np.array([*points])
    off = np.min(points,0)
    # print(off)
    points -= off
    # print(np.min(points,0))
    grid = np.ndarray(np.max(points,0)+[1,1],dtype=object)
    grid.fill('.')
    for p in points:
        # print(grid[p[0],p[1]])
        grid[p[0],p[1]] = '#'
        # print(grid[p[0],p[1]])

    # print(grid)
    for i,c in enumerate(corners):
        grid[c[0] - off[0],c[1] - off[1]] = hex(i)[2:]
    
    # print(grid)
    return "\n".join(["".join(g) for g in grid])

def vis_edges_svg(edges:Sequence[Edge]):
    import drawsvg as draw
    corners = []
    pos = (0,0)
    for e in lqdm(edges,desc="vizzing"):
        d = e.dir
        n = e.length
        corners.append(pos)
        pos = addtuple(pos,tuple(np.multiply(directions[d],n)))
    corners = np.array([*corners],dtype="float64")
    off = np.min(corners,0)
    corners -= off

    size = (1000,1000)
    corners[:,0] /= np.max(corners[:,0])/900
    corners[:,0] += 50
    corners[:,1] /= np.max(corners[:,1])/900
    corners[:,1] += 50

    d = draw.Drawing(1000,1000)

    els = [z for (x,y) in corners for z in (x,y)]

    d.append(draw.Lines(*els,close=True,fill="none",stroke="black",stroke_width=3))

    for i,c in enumerate(corners):
        d.append(draw.Text(str(i),font_size=10,x=c[0],y=c[1]))

    return d


##ALGORITHM DESCRIPTION
## follow the contour of the shape, corner by corner. if you hit a corner, and the last two corners were inside, you can attempt to make a rectangle/
## however, there are a handful of edge cases on rectangle creation. Our goal is to create a rectangle with homogenous sides; 
## that is, no side of the rectangle should transition from boundary to interior. To that end, the side between the interior corner will always be on the boundary, 
## as will the sides before and after; the fourth side will be interior. (The only exception is once the sides have been simplfied to a single rectangle; a simple 4-vertice check will suffice)
## 
##To ensure neither of the adjacent (before/after double inside side) walls are nonhomogenous, the rectangle is as long as the shorter of the two walls.
## Additionally, to ensure the fourth wall is homogenous, the shorter wall must either: 
## 1 - be an exterior corner; this means the bridge is guaranteed to be entirely interior
## 2 - an interior corner, and the adjoining corner (not part of the rectangle) must be farther away than the width of the rectangle
## if neither of these conditions are met, the rectangle check is discarded and the algorithm advances to the next vertex
## Now, if you pay attention to the geometry, that second condition is a little sus, as that would the rectangle to intersect itself.
## This is correct; due to nonlocal effects, it is possible that the algorithm can simplify to a self-intersecting boundary. 
## The algorithm can deal with this, but it requires edge case #2
##
## When suitable conditions for a rectangle are found, the edge will be simplified by "removing" the rectangle. Its area is added to a counter, and edges will be removed or modified as follows:
## The between-interior-corners edge and both walls will be deleted. on the shorter wall, this means removing the wall entirely, for the longer wall, this means moving the position
## of the edge from the bottom of the rectangle to its new top. (If the walls were the same size, the wall gets deleted as well). The interior edge is removed all together. Finally, to add the upper edge, the length of the edge across
## the corner of the shorter wall will be lengthened (or, in the case of case #2, shortened) from ending at one side of the rectangle to the other.
## Finally, to reduce the number of loops the algorithm has to make, these steps should be reflected in the vertex buffer, so a new rectangle can be created with the new vertices.
##
## To finish the shape, run the algorithm until there are 4 vertices left. There are two cases: all four are exterior, or all four are interior.
## In each case, the area is either added or removed from the total correspondingly, and the program returns.

def part2(input,do_hex=True,do_vis:bool=False):
    segments:list[tuple[str,int]] = []
    
    def turn_dir(prevdir,currdir):
        o1,o2 = order.index(prevdir),order.index(currdir)
        match (o1-o2) % 4:
            case 0 | 2:
                return 0
            case 1:
                return 1
            case 3:
                return -1
            case _:
                raise ValueError()
            
    total_turn = 0
    o2 = "RDLU"
    for i,l in enumerate(input):
        if do_hex:
            h = l.split(" ")[2][2:-1]
            n:int = str2hex(h[:5])
            d = o2[int(h[5])]
        else:
            d,n,_ = l.split(" ")
            n = int(n)            
        segments.append((d,n))
        if len(segments) > 1:
            total_turn += turn_dir(segments[i-1][0],d)
    
    total_turn += turn_dir(segments[-1][0],segments[0][0])
    assert total_turn / 4 in [1,-1]
    total_turn_dir = total_turn / 4
    
    perimeter = 0
    edges:EdgeList = EdgeList() #direction,length,(previous) corner is_interior
    for i,s in enumerate(segments):
        t = turn_dir(segments[i-1][0],s[0])
        e = (Edge(s[0],s[1],t==total_turn_dir))
        edges.append(e)
        perimeter += e.length ## THIS ASSUMES NO SELF INTERSECTIONS IN THE INPUT SHAPE
    # print("initial perimeter:",perimeter)
    
    if do_vis:
        with open('vis_out.txt','w') as f:
            f.write(vis_edges(edges))

    interior_area = 0
    i = 0
    e1000 = everyn(100)
    fr = 0
    # v = vis_edges_svg(edges)
    # v.save_svg(f"18_svgs/{fr}.svg")
    fr += 1
    change_timer = 0
    last_change = -1
    while len(edges) > 4:
        # print("length:",len(segments))
        def p():
            nonlocal fr
            print("               \t             \t                          ",end="\r")
            print(f"index: {i}\tedges: {len(edges)}\ttotal_turn: {total_turn}",end="\r")
            # v = vis_edges_svg(edges)
            # v.save_svg(f"18_svgs/{fr}.svg")
            # fr += 1
        try:
            pass
            # time.sleep(0.001)
        except KeyboardInterrupt:
            iembed()
        # e1000(p)
        ##NOTE: subtraction from i means negative indices will work throughout, with the exception of slices. NO slices should be used, 
        ## nor should any index past i be accessed without proper moduloing
        e = edges[i]
        #names are oriented with interior corners on the bottom ("floor")
        if not (edges[i-1].interior and edges[i-2].interior): # if not both previous vertices interior:
            # print(i,"not double interior")
            i += 1
            i %= len(edges)
            change_timer += 1
            if change_timer > 10 and last_change%len(edges) == i:
                change_timer = 0
                # iembed()
                edges.invert()
                # print("inverted")
            continue
        # if edges.inverted:
        #     iembed()
        rect_width = edges[i-2][1]

        ##NOTE: the numbering here will be strange; each edge has information specifically on the vertex at its start
        ## this means the wall corners are at [i], [i-3], but the wall lengths are at [i-1], [i-3]
        wall_vertices = (edges[i].interior,edges[i-3].interior)
        wall_lengths = (edges[i-1].length,edges[i-3].length)

        if wall_lengths[0] == wall_lengths[1]:
            shortest = 1 if wall_vertices[1] else 0 #always try to pick an interior vertex so the next check will trigger 
        else:
            shortest = int(argmin(wall_lengths))
        
        if wall_vertices[shortest]: #if the shorter wall is an interior corner, an extra check needs to be made to see if the overhang is wider than the rectangle
            overhang = (edges[i].length,edges[i-4].length)[shortest]
            if overhang < rect_width: ##if they are the same even more checks should be hit, but that can be dealt with later
                # print(i,"overhang too small")
                i += 1
                i %= len(edges)
                continue

        #Rect check passed; making rectangle
        rect_height = wall_lengths[shortest]
        
        #this slice will replace edges [i-4]...[i]. It can be shorter than that
        new_edges:list[Edge] = []

        ##Edge names: "Wings" - outside the rectangle, "walls": adjacent to the floor, to be deleted or shortened, "floor": interior corners, to be deleted
        ##Current edge order from [i-4]...[i]: wing 1, wall 1, floor, wall 2, wing 2. (wing/wall 2 are shortest == 0)
        
        #Wings
        wing1:Edge|None = edges[i-4]
        wing2:Edge|None = edges[i]
        if shortest == 1: #shortest == 1 means wing 1 is on the shorter wall, shortest == 0 means wing 2 is on the shorter wall
            ##wing 1 on the shorter wall: lengthen (or shorten) by width of rectangle 
            wing1 = Edge(wing1.dir,wing1.length + (rect_width if not wall_vertices[1] else -rect_width),wing1.interior) #direction is at the beginning of the wall, which is far from the rectangle; unchanged
            #wing 2 is on the longer wall; unchanged
        else:
            ##wing 2 is on the shorter wall: lengthen by with of rectangle. (other walls will position the start in the right place)
            wing2 = Edge(wing2.dir,wing2.length + (rect_width if not wall_vertices[0] else -rect_width),not wing2.interior) #if exterior (normal case), will become interior; if interior (overhang case), becomes exterior
            #wing 1 is on the longer wall; unchanged
        
        #Walls
        wall1:Edge|None = edges[i-3]
        wall2:Edge|None = edges[i-1]
        if shortest == 1: #wall1 is shorter wall
            #wall 1 gets deleted; set to None
            wall1 = None
            #wall 2 gets shortened by rect_height (length of shorter wall)
            wall2 = Edge(wall2.dir,wall2.length-rect_height,wall2.interior)
            #if wall2 is now 0-length, remove as well
            if wall2.length == 0:
                wall2 = None
        else:
            wall2 = None
            wall1 = Edge(wall1.dir,wall1.length-rect_height,wall1.interior)
            if wall1.length == 0:
                wall1 = None
        
        ##Edge case: both walls originally same length -> remove both walls, merge wings into one
        if wall1 is None and wall2 is None:
            ##NOTE: this becomes quite complicated in the overhang case, as then both wings will pass over each other. Hopefully, the algorithm should never let that happen.
            ##However, the one exception is if both wing1 and wing2's vertices meet; then the rectangle is a fully enclosed square, like below:
            #.......#....
            #.......#....
            #...####▚####
            #...#...#....
            #...#...#....
            #...#####....
            #............
            ## (▚ symbol shows that the path goes from top to left to down to right to up to right; the walls don't intersect, just meet at the vertex)
            ## In this case, it should simplify to just an interior corner at the ▚ symbol. In other words, the interior wing is removed and the exterior wing becomes interior
            ## It turns out, though, that the logic is then the same; properly combining the length of the wings with proper cancellation will always result in a success

            ## if both edges are in the same direction, then simply add the lengths. 
            ## However, if exactly one rectangle corner is exterior, and the other interior, there is cancellation
            ## First, note that the end of the wing1 is the beginnning of wing2, because one has been shifted to the other side of the rectangle.
            ## This means that the longer one will be the one that defines the corner.
            ## Thus, the new wing length and direction will be that of whichever wing is longer, with length subtracted by the shorter wing
            ## These cases can again be combined: the result is in the direction of the longest wing; if the other wing is in the same direction, add the lengths, otherwise, subtract
            ## The final loose end is the interior/exterior of the wing; this is just copied from the first wing, but inverted if the first wing's direction is different from the combined wing

            comb_wing,other_wing = sorted([wing1,wing2],key=itemgetter(1),reverse=True) #pick wing with longest length
            comb_wing = Edge(comb_wing.dir, comb_wing.length + (other_wing.length if other_wing.dir == comb_wing.dir else -other_wing.length), wing1.interior if wing1.dir == comb_wing.dir else not wing1.interior)
            wing1 = comb_wing
            wing2 = None

            if edges.inverted:
                if other_wing.dir != comb_wing.dir: ##if the wings are in the other direction, cancel out the areas now
                    interior_area -= other_wing.length - 1


        ##FINALLY: assemble new edges
        new_edges.append(wing1)
        if wall1 is not None: new_edges.append(wall1)
        if wall2 is not None: new_edges.append(wall2)
        if wing2 is not None: new_edges.append(wing2)


        test = edges[(i+1)%len(edges)] #make sure the index modification works

        turn_diff = sum([[-1,1][e.interior] for e in new_edges])

        new_range,subbed_edges = list_sub_index(edges,range(i-4,i+1),new_edges)
        
        turn_diff -= sum([[-1,1][e.interior] for e in subbed_edges])

        i = new_range.stop-1 % len(edges)

        if edges.inverted:
            #Calculate area diff as follows: 4 cases (2*2)
            ## if the wall lengths are not the same:
            ##   if the shorter wall is exterior:
            ##      diff = 2 [vertices] + 2*(depth-1) [walls] + 1*(width-1) [floor] + interior
            ##   if the shorter wall is interior:
            ##      diff = 3 [vertices] + 2*(depth-1) [walls] + 2*(width-2) [floor and shortened edge] + interior
            ## if the wall lengths are the same:
            ##   if both vertices are either exterior or interior:
            ##      diff = 2 [vertices] + 2*(depth-1) [walls] + 1*(width-1) [floor] + interior
            ##   if the vertices are different turning directions:
            ##      diff = 4 [vertices] + 2*(depth-1) [walls] + 2*(width-1) [floor and removed edge] + interior + canceled out edge, if existent
            ## the final term in condition 2b is calculated in the equal-wall-lengths clause above because it is easier
            ## additionally, some of the common terms are factored out below, removing cases 1a) and 2a) as they are the same effect
            rect_interior_area = (rect_height - 1)*(rect_width - 1) #exclude edges so -1
            interior_area -= 2 + 2*(rect_height-1) + (rect_width - 1) + rect_interior_area

            if (wall1 or wall2) and wall_vertices[shortest]: # wall lengths different (at least one wall is not None) and shorter wall is interior
                # shortening the interior wall by the width of the rectangle, so harvest the edge length that is removed
                interior_area -= 2 + (rect_width-1)
                # print("intersnect")
            if wall1 is None and wall2 is None and wall_vertices[0] != wall_vertices[1]: #wall lengths are the same (both walls None) and turning directions are different
                # means the entire far edge will be deleted; harvest both vertices and the top edge
                interior_area -= 2 + (rect_width-1)

        else:
            interior_area += (rect_height - 1)*(rect_width - 1) #add rectangle **interior** area; subtract -1 to not add edges
            if wall_lengths[0] != wall_lengths[1]: #walls were different lengths
                if not wall_vertices[shortest]: #exterior shortest; means the glass ceiling was open/interior, harvest and add to area
                    interior_area += rect_width - 1 #add interior length of ceiling
            else:
                if not any(wall_vertices): ##if walls of equal length and **both** edges are exterior, then the ceiling is interior
                    interior_area += rect_width - 1 
        
        if do_vis:
            with open('vis_out.txt','a') as f:
                f.write("\n\n" + vis_edges(edges))
                f.write(f"\nArea: {interior_area}")
                f.write(f"\nInverted: {interior_area}")
        #iembed()

        #index modification test: the above should not change what the next element is pointing to (as long as the list is big enough that it doesn't wrap around)
        if len(edges) > 5:
            assert test == edges[(i+1)%len(edges)],iembed()

        # if len(edges) < 80:
        #     iembed()

        #### ONE FINAL ISSUE YAYYYYYY ####
        ## because of nonlocal interactions, it is possible for this algorithm to simplify a shape until it is (effectively) inside out, 
        ## to the point where there are no interior dimples / pairs of interior corners.
        ## Bar adding more simplification rules, the only way to fix this is to then turn it inside out!
        # print(turn_diff)
        # total_turn += turn_diff
        # if total_turn < 0:
        #     # print("inverting")
        #     total_turn = -total_turn
        #     edges.invert()
            
        last_change = i




    if edges.inverted:
        edges.invert()
        total_turn = -total_turn
    
    # print("interior area:",interior_area) #clear the everyn

    area = interior_area + perimeter

    #Calculate area of final rectangle
    assert len(edges) == 4
    assert sorted([e.dir for e in edges]) == sorted("DLRU"),sorted([e.dir for e in edges]) #one of each direction
    assert all([e.interior for e in edges]) or not any([e.interior for e in edges]) #homogenous turning direction
    
    length,width = edges[0].length-1,edges[1].length-1
    
    if edges[0].interior:
        area += length*width
    else: #inverted rectangle, subtract area **and edges**
        area -= (length+2)*(width+2)

    return area
        

if __name__ == "__main__":
    input_data = get_input()
    test_data = get_input("test.txt")

    part = "1"
    part = "2"

    if part == "1":
        print("=== PUZZLR IUPUT ===")
        p = part1(input_data)
        print("=== TRDT IUPUT ===")
        print(part1(test_data))
        submit_answer(p,part=1)
    else:
        print("=== PUZZLR IUPUT ===")
        iembed()
        # r = timeit("part2(input_data)",globals=globals())
        # print(r)
        p = part2(input_data)
        print("=== TRDT IUPUT ===")
        # i = get_input("day18.txt")
        # print(part2(i))
        # print(part2(i,do_hex=False,do_vis=True))
        # for j in range(len(i)):
        #     l = [i[k-j] for k in range(len(i))]
        #     print(l,part2(l,do_hex=False,do_vis=True))
        submit_answer(p,part=2)


#### OLD AREA OFFSET CODE
if False:
            pass
        

            #in the equal-wall-lengths case