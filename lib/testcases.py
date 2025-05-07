from util import *
from defs import *
import os.path

logger = get_logger("Testcases")


script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
gen_dir = os.path.join(script_dir, "gen")

def get_gen_file(file_name: str | None) -> str | None:
    if file_name is None:
        return None
    return read_file(logger, os.path.join(gen_dir, file_name))

def from_asm(file_name: str, expected: str | None = None) -> Testcase:
    return Testcase(asm=get_gen_file(file_name), expected=get_gen_file(expected))

def from_bincode(file_name: str, expected: str | None = None) -> Testcase:
    return Testcase(bincode=get_gen_file(file_name), expected=get_gen_file(expected))


def gen_branch_hazard(nops_count: int) -> Testcase:
    source_asm = ""
    source_asm += '''
    sw zero, 0(zero)
    sw zero, 4(zero)
    add t0, zero, zero  ; a fake x0 for nops
    addi t1, zero, 42   ; payload
    addi t2, zero, 0    ; tested value

    add t0, t0, t0  ; nops
    add t0, t0, t0  ; nops
    add t0, t0, t0  ; nops
    add t0, t0, t0  ; nops
    add t0, t0, t0  ; nops

    addi t2, zero, 8
'''
    source_asm += '''
    add t0, t0, t0  ; nops''' * nops_count
    source_asm += "\n"
    source_asm += '''
    beq t2, zero, BRANCH
    sw t1, 0(zero)
BRANCH:
    sw t1, 4(zero)
'''
    return Testcase(asm=source_asm)


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
