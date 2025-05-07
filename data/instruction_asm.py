def i_rtype(inst, rd, rs1, rs2):
    return f"{inst} x{rd}, x{rs1}, x{rs2}\n"

def i_itype(inst, rd, rs1, imm):
    return f"{inst} x{rd}, x{rs1}, {imm}\n"


# R-type

def i_and(rd, rs1, rs2):
    return i_rtype("and", rd, rs1, rs2)

def i_xor(rd, rs1, rs2):
    return i_rtype("xor", rd, rs1, rs2)

def i_sll(rd, rs1, rs2):
    return i_rtype("sll", rd, rs1, rs2)

def i_add(rd, rs1, rs2):
    return i_rtype("add", rd, rs1, rs2)

def i_sub(rd, rs1, rs2):
    return i_rtype("sub", rd, rs1, rs2)

def i_mul(rd, rs1, rs2):
    return i_rtype("mul", rd, rs1, rs2)


# I-type

def i_addi(rd, rs1, imm):
    return i_itype("addi", rd, rs1, imm)

def i_srai(rd, rs1, imm):
    return i_itype("srai", rd, rs1, imm)


# pseudo instructions

def i_li(rd, tmp, imm):
    imms = (
        (imm >> 22) & 2047,
        (imm >> 11) & 2047,
        (imm >>  0) & 2047,
    )
    asm = ""
    asm += i_addi(tmp, 0, 11)
    asm += i_addi(rd, 0, imms[0])
    asm += i_sll(rd, rd, tmp)
    asm += i_addi(rd, rd, imms[1])
    asm += i_sll(rd, rd, tmp)
    asm += i_addi(rd, rd, imms[2])
    return asm