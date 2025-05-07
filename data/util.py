from lib.util import *
from lib.defs import *
import os

logger = get_logger("Testcases")


script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_dir = os.path.join(script_dir, "data")


# for testcase generation from files

def get_data_file(file_name: str | None) -> str | None:
    if file_name is None:
        return None
    return read_file(logger, os.path.join(data_dir, file_name))

def from_asm(file_name: str, expected: str | None = None) -> Testcase:
    return Testcase(asm=get_data_file(file_name), expected=get_data_file(expected))

def from_bincode(file_name: str, expected: str | None = None) -> Testcase:
    return Testcase(bincode=get_data_file(file_name), expected=get_data_file(expected))


# for random testcase generation

import random

def rand_imm(width) -> int:
    return random.randint(0, 2 ** width - 1)

def rand_reg() -> int:
    return rand_until(
        lambda: rand_imm(5),
        lambda reg: reg != 0
    )
