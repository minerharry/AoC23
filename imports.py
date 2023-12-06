import functools
from typing import TYPE_CHECKING, Callable, Literal
from text import get_input
from aocd.post import submit
from aocd.get import get_data,get_day_and_year,current_day
from aocd.models import Puzzle,User

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
        return puzzle.input_data.splitlines()
    else:
        return text.get_input(puzzle)


def submit_answer(answer,part:Literal['a','b'],puzzle=puzzle,do_confirm=True):
    if do_confirm and not confirm(f"Are you sure you want to submit answer {answer} to puzzle {puzzle}?"):
        print("Answer not sent.")
        return
    if part == 'a':
        puzzle.answer_a=answer
    else:
        puzzle.answer_b=answer

if TYPE_CHECKING:
    lqdm = tqdm()
else:
    lqdm = functools.partial(tqdm,leave=False)
