from copy import copy
from math import prod
from random import shuffle

from numpy import sign
from _imports import *

def part1(input):
    # broad = input[0]
    modules:dict[str,tuple[str,list[str]]] = {}
    # modules["broadcaster"] = ("",broad.split(" -> ")[0].split(", "))
    for l in input:
        if l.startswith("broadcaster"):
            modules["broadcaster"] = ("",l.split(" -> ")[1].split(", "))
            continue
        name,outs = l[1:].split(" -> ")
        outs = outs.split(", ")
        modules[name] = (l[0],outs)
        print(name,outs,l[0])
    
    states:dict[str,dict[str,bool]] = DefaultDict(dict)
    for name,(mtype,conns) in list(modules.items()):
        for c in copy(conns):
            if c not in modules:
                modules[c] = ("output",[])
                continue
            if modules[c][0] == "&":
                states[c][name] = False
        if mtype == "%":
            states[name][""] = False
    states = dict(states)

    pulses = (0,0)
    for i in trange(100000):
        p = process_modules(modules,states) #mutates states
        pulses = (p[0] + pulses[0], p[1] + pulses[1])

    return prod(pulses)
    

def process_modules(modules:dict[str,tuple[str,list[str]]],states:dict[str,dict[str,bool]]):
    pulses:list[tuple[str,bool,str]] = [("broadcaster",False,"button")] ##False = low, True = high
    nlow = 0
    nhigh = 0
    e =everyn(1000)
    while pulses:
        # e(lambda: tqdm.write(f"{len(pulses)}"))
        dest,signal,source = pulses.pop(0)
        # tqdm.write(f"{source} {"-high" if signal else "-low"} -> {dest}")
        if signal:
            nhigh += 1
        else:
            nlow += 1
        mtype,connections = modules[dest]
        # print(mtype,connections)
        new = []
        match mtype:
            case "": ##broadcaster
                new = ([(conn,signal,dest) for conn in connections])
            case "%": ##flip flop
                if signal == False:
                    state = states[dest]['']
                    states[dest][""] = (state := not state)
                    # print(state)
                    new = ([(conn,state,dest) for conn in connections])
            case "&": ##conjunction
                state = states[dest]
                state[source] = signal
                # print(state)
                out = not all(state.values());
                # print(out)
                new = ([(conn,out,dest) for conn in connections])
        pulses = pulses + (new)
        # shuffle(pulses)
        # print(new)
        # input()
            
    
    return (nlow,nhigh)

##P2 thoughts:
# Flip-flops are the only stateful thing; conjucntors' "state" can be described as the state of the wire between soruce and dest
# essentially, this is a FSM where conjunctors are the logic and flip-flops are the SM
# the big difference is the fact that the clock is always on, pulses are processed sequentially, and pulses can die
## *most* of the input is flip-flops; fascinating



def part2(input):
    # broad = input[0]
    modules:dict[str,tuple[str,list[str]]] = {}
    # modules["broadcaster"] = ("",broad.split(" -> ")[0].split(", "))
    for l in input:
        if l.startswith("broadcaster"):
            modules["broadcaster"] = ("",l.split(" -> ")[1].split(", "))
            continue
        name,outs = l[1:].split(" -> ")
        outs = outs.split(", ")
        modules[name] = (l[0],outs)
        print(name,outs,l[0])
    
    states:dict[str,dict[str,bool]] = DefaultDict(dict)
    for name,(mtype,conns) in list(modules.items()):
        for c in copy(conns):
            if c not in modules:
                modules[c] = ("output",[])
                continue
            if modules[c][0] == "&":
                states[c][name] = False
        if mtype == "%":
            states[name][""] = False
    states = dict(states)

    pulses = (0,0)
    for i in trange(100000):
        p = process_modules(modules,states) #mutates states
        pulses = (p[0] + pulses[0], p[1] + pulses[1])
        print(states["gf"])
        iembed()

    return prod(pulses)
    
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