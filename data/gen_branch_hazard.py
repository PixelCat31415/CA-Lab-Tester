from lib.defs import *

def gen_branch_hazard(nops_count: int) -> Testcase:
    nops = "    add t0, t0, t0  ; nops\n"

    source_asm = ""

    source_asm += '''
    sw zero, 0(zero)
    sw zero, 4(zero)
    add t0, zero, zero  ; a fake x0 for nops
    addi t1, zero, 42   ; payload
'''
    source_asm += nops * 4
    source_asm += "    addi t2, zero, 8\n"
    source_asm += nops * nops_count
    source_asm += '''
    beq t2, zero, BRANCH1
    sw t1, 0(zero)
BRANCH1:
    sw t1, 4(zero)
'''
    source_asm += "\n"

    source_asm += '''
    sw zero, 8(zero)
    sw zero, 12(zero)
    add t0, zero, zero  ; a fake x0 for nops
    addi t1, zero, 42   ; payload
'''
    source_asm += nops * 4
    source_asm += "    addi t2, zero, 8\n"
    source_asm += nops * nops_count
    source_asm += '''
    beq zero, t2, BRANCH2
    sw t1, 8(zero)
BRANCH2:
    sw t1, 12(zero)
'''

    return Testcase(asm=source_asm)
