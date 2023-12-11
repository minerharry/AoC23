from contextlib import redirect_stdout
import functools
import io
import itertools
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


try:
    puzzle = Puzzle(2023,get_day_and_year()[0])
except:
    try:
        puzzle = Puzzle(2023,current_day())
    except:
        puzzle = None

def get_input(puzzle:Puzzle|str=puzzle):
    if isinstance(puzzle,Puzzle):
        with open("aocd_input.txt",'w') as f:
            f.write(puzzle.input_data)
        return puzzle.input_data.splitlines()
    else:
        return text.get_input(puzzle)

max = 18446744073709551615 ##largest number storable in C long long type
def submit_answer(answer,part:Literal['a','b'],puzzle=puzzle,do_confirm=True):
    if do_confirm:
        if not confirm(f"Are you sure you want to submit answer {answer} to part {part} puzzle {puzzle}?") or ((answer > max or answer < -max) and \
            not confirm(f"Are you sure you're sure? {answer} is outside of C's normal data type range of [{-max},{max}] by {min(abs(answer - max),abs(-max-answer))}")):
            print("Answer not sent.")
            return
        
    if part == 'a':
        puzzle.answer_a = answer
    else:
        puzzle.answer_b = answer
    print("Answer Submitted")


if TYPE_CHECKING:
    lqdm = tqdm()
else:
    lqdm = functools.partial(tqdm,leave=False)

no_print = redirect_stdout(io.StringIO())
