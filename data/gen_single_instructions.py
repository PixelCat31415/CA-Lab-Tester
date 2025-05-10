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

def gen_lw(ref_addr):
    asm = i_li(1, 2, ref_addr)
    for i in range(2, 32):
        addr = random.randint(0, 4) * 4
        asm += i_lw(i, 1, addr - ref_addr)
    return asm

def gen_sw(ref_addr):
    asm = i_li(1, 2, ref_addr)
    for i in range(8):
        src = random.randint(24, 31)
        asm += i_sw(src, 1, i * 4 - ref_addr)
    return asm
