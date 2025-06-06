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
from data.gen_single_instructions import *
from data.gen_mixed_instructions import *


testcase_groups: list[tuple[str, list[Testcase]]] = [
    ("sample", [
        from_bincode("instruction_1.txt", "output_1.txt"),
        from_bincode("instruction_2.txt", "output_2.txt"),
        from_bincode("instruction_3.txt", "output_3.txt"),
        from_bincode("instruction_4.txt", "output_4.txt"),
    ]),
    ("hazards", [
        gen_branch_hazard(i) for i in range(6)
    ] + [
        from_asm("load-use.s"),
    ]),
    ("bad_registers", [
        from_asm("bad_registers.s")
    ]),
    ("forwarding", [
        from_asm("forwarding-rs1.s"),
        from_asm("forwarding-rs2.s"),
    ]),
    ("single_instructions", [
        Testcase(asm=gen_addi()) for _ in range(5)
    ] + [
        Testcase(asm=gen_rtype("i_and")) for _ in range(5)
    ] + [
        Testcase(asm=gen_rtype("i_xor")) for _ in range(5)
    ] + [
        Testcase(asm=gen_sll()) for _ in range(5)
    ] + [
        Testcase(asm=gen_rtype("i_add")) for _ in range(5)
    ] + [
        Testcase(asm=gen_rtype("i_sub")) for _ in range(5)
    ] + [
        Testcase(asm=gen_rtype("i_mul")) for _ in range(5)
    ] + [
        Testcase(asm=gen_srai()) for _ in range(5)
    ] + [
        Testcase(asm=gen_lw(0)),
        Testcase(asm=gen_lw(32)),
        Testcase(asm=gen_sw(0)),
        Testcase(asm=gen_sw(32)),
    ]),
    ("mixed_instructions", [
        Testcase(asm=gen_mixed(i < 10)) for i in range(20)
    ]),
]


if __name__ == '__main__':
    raise RuntimeError("This module is not meant to be run as a script")
