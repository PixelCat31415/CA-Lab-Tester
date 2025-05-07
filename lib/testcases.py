from util import *
from defs import *
import os.path

logger = get_logger("Testcases")


script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_dir = os.path.join(script_dir, "data")

def get_gen_file(file_name: str | None) -> str | None:
    if file_name is None:
        return None
    return read_file(logger, os.path.join(data_dir, file_name))

def from_asm(file_name: str, expected: str | None = None) -> Testcase:
    return Testcase(asm=get_gen_file(file_name), expected=get_gen_file(expected))

def from_bincode(file_name: str, expected: str | None = None) -> Testcase:
    return Testcase(bincode=get_gen_file(file_name), expected=get_gen_file(expected))


# import generator functions from data/
# modifying sys.path because python imports are dumb

import sys
sys.path.append(script_dir)

from data.gen_branch_hazard import gen_branch_hazard


testcase_groups: list[tuple[str, list[Testcase]]] = [
    ("sample", [
        from_bincode("instruction_1.txt", "output_1.txt"),
        from_bincode("instruction_2.txt", "output_2.txt"),
        from_bincode("instruction_3.txt", "output_3.txt"),
        from_bincode("instruction_4.txt", "output_4.txt"),
    ]),
    ("branch_hazard", [
        gen_branch_hazard(i) for i in range(6)
    ]),
]


if __name__ == '__main__':
    raise RuntimeError("This module is not meant to be run as a script")
