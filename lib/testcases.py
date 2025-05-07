from util import *
from defs import *
import os.path

logger = get_logger("Testcases")


# import generator functions from data/
# modifying sys.path because python imports are dumb

import sys
script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(script_dir)

from data.util import *
from data.gen_branch_hazard import gen_branch_hazard
from data.gen_lab1 import *


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
    ("instruction_addi", [
        Testcase(asm=gen_addi()) for _ in range(5)
    ]),
    ("instruction_and", [
        Testcase(asm=gen_rtype("i_and")) for _ in range(5)
    ]),
    ("instruction_xor", [
        Testcase(asm=gen_rtype("i_xor")) for _ in range(5)
    ]),
    ("instruction_sll", [
        Testcase(asm=gen_sll()) for _ in range(5)
    ]),
    ("instruction_add", [
        Testcase(asm=gen_rtype("i_add")) for _ in range(5)
    ]),
    ("instruction_sub", [
        Testcase(asm=gen_rtype("i_sub")) for _ in range(5)
    ]),
    ("instruction_mul", [
        Testcase(asm=gen_rtype("i_mul")) for _ in range(5)
    ]),
    ("instruction_srai", [
        Testcase(asm=gen_srai()) for _ in range(5)
    ]),
    ("lab1", [
        Testcase(asm=gen_random(i < 2)) for i in range(5)
    ]),
    ("bad_registers", [
        from_asm("bad_registers.s")
    ]),
]


if __name__ == '__main__':
    raise RuntimeError("This module is not meant to be run as a script")
