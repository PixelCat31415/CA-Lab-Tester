# generate code without lw, sw, beq (same as lab 1)

import random
from data.util import *
from data.instruction_asm import *


def gen_addi():
    asm = ""
    for _ in range(30):
        asm += i_addi(rand_reg(), rand_reg(), rand_simm(12))
    return asm

def gen_rtype(inst_name: str):
    inst = eval(inst_name)
    rs1 = rand_reg()
    rs2 = rand_reg()
    rd = rand_reg()
    asm = ""
    for _ in range(10):
        asm += i_addi(rs1, rs1, rand_simm(12))
        asm += i_addi(rs2, rs2, rand_simm(12))
        asm += inst(rd, rs1, rs2)
    return asm

def gen_sll():
    rs1 = rand_reg()
    rs2 = rand_until(rand_reg, lambda r: r != rs1)
    rd = rand_reg()
    asm = ""
    for _ in range(10):
        asm += i_addi(rs1, 0, rand_simm(12))
        asm += i_addi(rs2, 0, rand_uimm(5))
        asm += i_sll(rd, rs1, rs2)
    return asm

def gen_srai():
    asm = ""
    rs1 = rand_reg()
    rd = rand_until(rand_reg, lambda r: r != rs1)
    # sign bit = 0
    asm += i_li(rs1, rd, rand_uimm(31))
    for _ in range(9):
        asm += i_srai(rd, rs1, rand_uimm(5))
    # sign bit = 1
    asm += i_li(rs1, rd, rand_uimm(31) + 2 ** 31)
    for _ in range(9):
        asm += i_srai(rd, rs1, rand_uimm(5))
    return asm

def gen_random(include_x0: bool = False):
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
        inst_id = random.randint(1, 8)
        rs1 = random.choice(selected)
        rs2 = random.choice(selected)
        rd = random.choice(selected)
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
    return asm
