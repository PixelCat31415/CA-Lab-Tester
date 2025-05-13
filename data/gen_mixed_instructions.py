import random
from data.util import *
from data.instruction_asm import *

def gen_mixed(include_x0: bool = False):
    asm = ""
    selected = []
    if include_x0:
        selected.append(0)
    # select a small set of registers and load random small numbers as initial values
    for _ in range(5):
        reg = rand_until(rand_reg, lambda r: r not in selected)
        selected.append(reg)
        asm += i_addi(reg, 0, rand_simm(12))
    # run random instructions on selected registers
    for _ in range(25):
        inst_id = random.randint(1, 10)
        rs1 = random.choice(selected)
        rs2 = random.choice(selected)
        rd = random.choice(selected)
        addr = random.randint(0, 7) * 4
        match inst_id:
            case 1:
                asm += i_and(rd, rs1, rs2)
            case 2:
                asm += i_xor(rd, rs1, rs2)
            case 3:
                asm += i_sll(rd, rs1, rs2)
            case 4:
                asm += i_add(rd, rs1, rs2)
            case 5:
                asm += i_sub(rd, rs1, rs2)
            case 6:
                asm += i_mul(rd, rs1, rs2)
            case 7:
                asm += i_addi(rd, rs1, rand_simm(12))
            case 8:
                asm += i_srai(rd, rs1, rand_uimm(5))
            case 9:
                asm += i_lw(rd, 0, addr)
            case 10:
                asm += i_sw(rs2, 0, addr)
    return asm
