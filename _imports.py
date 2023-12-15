from contextlib import redirect_stdout
from IPython.lib.pretty import pretty
# pretty(obj)
import functools
import io
import itertools
from logging import DEBUG, INFO, WARNING, Formatter, StreamHandler, getLogger
import re
import traceback
from typing import TYPE_CHECKING, Callable, Literal
from aocd.post import submit
from aocd.get import get_data,get_day_and_year,current_day
from aocd.models import Puzzle,User
from contextlib import nullcontext

import aocd
from tqdm import tqdm
import numpy as np
from inquirer import confirm
from IPython import embed as iembed
import text
from typing import DefaultDict,Iterable,Any
from utils import *

logger = getLogger()
logger.setLevel(WARNING)
s = StreamHandler()
s.setFormatter(Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
logger.addHandler(s)

try:
    puzzle = Puzzle(2023,get_day_and_year()[0])
except:
    try:
        s = current_day()
        logger.warning(f"Unable to ascertain day; using current day, {s}")
        puzzle = Puzzle(2023,s)
    except:
        puzzle = None

def get_input(puzzle:Puzzle|str=puzzle):
    if isinstance(puzzle,Puzzle):
        with open("aocd_input.txt",'w') as f:
            f.write(puzzle.input_data)
        return puzzle.input_data.splitlines()
    else:
        return text.get_input(puzzle)

_maxC = 18446744073709551615 ##largest number storable in C long long type
def submit_answer(answer,part:Literal['a','b','A','B',1,2],puzzle=puzzle,do_confirm=True):
    part = (1 if str(part).lower() == "a" else 2) if not isinstance(part,int) else part
    if do_confirm:
        if not confirm(f"Are you sure you want to submit answer {answer} to part {part} of puzzle {pretty(puzzle)}?") or ((answer > _maxC or answer < -_maxC) and \
            not confirm(f"Are you sure you're sure? {answer} is outside of C's normal data type range of [{-_maxC},{_maxC}] by {min(abs(answer - _maxC),abs(-_maxC-answer))}")):
            print("Answer not sent.")
            return
        
    if part in ['a','A',1]:
        puzzle.answer_a = answer
    elif part in ['b','B',2]:
        puzzle.answer_b = answer
    else:
        raise ValueError()
    print("Answer Submitted")
