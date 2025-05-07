from lib.defs import *

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
