from util import *
from defs import *
import argparse
import re


logger = get_logger("Assembler")


def parse_immediate(imm: str, lo: int, hi: int) -> int:
    try:
        imm = int(imm)
    except ValueError as e:
        logger.error(f"Immediate `{imm}` is not a number in base 10")
        raise e
    if not (lo <= imm <= hi):
        logger.error(f"Immediate `{imm}` is out of range [{lo}, {hi}]")
        raise ValueError()
    return imm


def parse_register(reg: str) -> int:
    try:
        match reg:
            case "zero":
                return 0
            case "ra":
                return 1
            case "sp":
                return 2
            case "gp":
                return 3
            case "tp":
                return 4
            case "fp":
                return 8
            case str(s) if s.startswith("t"):
                n = parse_immediate(s[1:], 0, 6)
                if 0 <= n <= 2:
                    return 5 + n
                elif 3 <= n <= 6:
                    return 28 - 3 + n
                raise ValueError()
            case str(s) if s.startswith("s"):
                n = parse_immediate(s[1:], 0, 11)
                if 0 <= n <= 1:
                    return 8 + n
                elif 2 <= n <= 11:
                    return 18 - 2 + n
                raise ValueError()
            case str(s) if s.startswith("a"):
                n = parse_immediate(s[1:], 0, 7)
                return 10 + n
            case str(s) if s.startswith("x"):
                n = parse_immediate(s[1:], 0, 31)
                return n
            case _:
                raise ValueError()
    except ValueError as e:
        logger.error(f"Cannot parse register `{reg}`")
        raise e


# returns: (register, immediate = offset)
def parse_address(addr: str) -> tuple[int, int]:
    try:
        mat = re.match(r'^(.*)\((.*)\)$', addr)
        reg = parse_register(mat.group(2))
        imm = parse_immediate(mat.group(1), -2048, 2047)
    except Exception as e:
        logger.error(f"Cannot parse address `{addr}`")
        raise e
    return (reg, imm)


def parse_instruction(code: str, inst: Instruction) -> Instruction:
    if code.endswith(":"):
        # label
        inst.inst = None
        inst.label = code[:-1]
        return inst
    # instruction
    inst.inst, code = re.split(r'\s+', code, maxsplit=1)
    ops = list(map(lambda op: op.strip(), code.split(",")))
    match inst.inst:
        case "and" | "xor" | "sll" | "add" | "sub" | "mul":
            if len(ops) != 3:
                logger.error(f"R-type instructions expect 3 operands, but {len(ops)} are given")
                raise ValueError()
            inst.rd = parse_register(ops[0])
            inst.rs1 = parse_register(ops[1])
            inst.rs2 = parse_register(ops[2])
        case "addi" | "srai":
            if len(ops) != 3:
                logger.error(f"I-type instructions expect 3 operands, but {len(ops)} are given")
                raise ValueError()
            inst.rd = parse_register(ops[0])
            inst.rs1 = parse_register(ops[1])
            inst.imm = parse_immediate(ops[2], -2048, 2047) if inst.inst == "addi" \
                        else parse_immediate(ops[2], 0, 31)
        case "lw" | "sw":
            if len(ops) != 2:
                logger.error(f"S-type instructions expect 2 operands, but {len(ops)} are given")
                raise ValueError()
            inst.rd = parse_register(ops[0])  # lw
            inst.rs2 = parse_register(ops[0])  # sw
            inst.rs1, inst.imm = parse_address(ops[1])
        case "beq":
            if len(ops) != 3:
                logger.error(f"B-type instructions expect 3 operands, but {len(ops)} are given")
                raise ValueError()
            inst.rs1 = parse_register(ops[0])
            inst.rs2 = parse_register(ops[1])
            inst.label = ops[2]
        case _:
            raise ValueError()
    return inst


def parse_lines(lines: list[str]):
    insts: list[Instruction] = []
    cur_pc: int = 0
    for lineno, ln in enumerate(lines, start=1):
        try:
            # remove comment
            code = re.sub(r';.*$', '', ln)
            # separate labels and code
            code = code.replace(":", ":\n")
            for seg in code.split("\n"):
                seg = seg.strip()
                if len(seg) == 0:
                    continue
                inst = Instruction(addr=cur_pc, lineno=lineno, codeln=ln.strip(), codeseg=seg)
                inst = parse_instruction(seg, inst)
                insts.append(inst)
                if inst.inst is not None:
                    cur_pc += 4
        except Exception as e:
            logger.info(f"At line {lineno}: {ln.strip()}")
            raise SyntaxError()
    return insts


def resolve_labels(insts: list[Instruction]) -> list[Instruction]:
    labels = {}
    for inst in insts:
        if inst.inst is not None:
            continue
        if inst.label in labels:
            logger.error(f"Duplicated label `{inst.label}`")
            logger.info(f"At line {inst.lineno}: {inst.codeln}")
            raise SyntaxError()
        labels[inst.label] = inst.addr
    for inst in insts:
        if inst.inst != "beq":
            continue
        if inst.label not in labels:
            logger.error(f"Unknown label `{inst.label}`")
            logger.info(f"At line {inst.lineno}: {inst.codeln}")
            raise SyntaxError()
        inst.imm = (labels[inst.label] - inst.addr) // 2
    return insts


def assemble_one(inst: Instruction) -> str:
    def imm(value: int, width: int) -> str:
        min_value = 2 ** (width - 1)
        assert -min_value <= value < min_value * 2
        if value < 0:
            value += 2 ** width
        return f"{value:0{width}b}"
    def reg(reg: int) -> str:
        return imm(reg, 5)
    match inst.inst:
        case None:
            return ""
        case "and":
            return f"0000000_{reg(inst.rs2)}_{reg(inst.rs1)}_111_{reg(inst.rd)}_0110011"
        case "xor":
            return f"0000000_{reg(inst.rs2)}_{reg(inst.rs1)}_100_{reg(inst.rd)}_0110011"
        case "sll":
            return f"0000000_{reg(inst.rs2)}_{reg(inst.rs1)}_001_{reg(inst.rd)}_0110011"
        case "add":
            return f"0000000_{reg(inst.rs2)}_{reg(inst.rs1)}_000_{reg(inst.rd)}_0110011"
        case "sub":
            return f"0100000_{reg(inst.rs2)}_{reg(inst.rs1)}_000_{reg(inst.rd)}_0110011"
        case "mul":
            return f"0000001_{reg(inst.rs2)}_{reg(inst.rs1)}_000_{reg(inst.rd)}_0110011"
        case "addi":
            return f"{imm(inst.imm, 12)}_{reg(inst.rs1)}_000_{reg(inst.rd)}_0010011"
        case "srai":
            return f"0100000_{imm(inst.imm, 5)}_{reg(inst.rs1)}_101_{reg(inst.rd)}_0010011"
        case "lw":
            return f"{imm(inst.imm, 12)}_{reg(inst.rs1)}_010_{reg(inst.rd)}_0000011"
        case "sw":
            im = imm(inst.imm, 12)
            return f"{im[:7]}_{reg(inst.rs2)}_{reg(inst.rs1)}_010_{im[7:]}_0100011"
        case "beq":
            im = imm(inst.imm, 12)
            return f"{im[0]}{im[2:8]}_{reg(inst.rs2)}_{reg(inst.rs1)}_000_{im[8:]}{im[1]}_1100011"
        case _:
            raise RuntimeError()


def assemble_all(insts: list[Instruction]) -> str:
    result = ""
    for inst in insts:
        try:
            bincode = assemble_one(inst)
            result += f"{bincode:37s}  // {inst.codeseg}\n"
        except Exception as e:
            logger.error("Failed to generate binary code")
            logger.info(f"At line {inst.lineno}: {inst.codeln}")
            raise e
    return result


def assemble(source_asm: str) -> None:
    try:
        code = parse_lines(source_asm.split("\n"))
        code = resolve_labels(code)
        code = assemble_all(code)
    except Exception as e:
        logger.error(f"Failed to assemble source code")
        raise e
    return code


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                prog='assembler.py',
                description='Assembly to binary-code compiler for Lab 2 simplified RISC-V instruction set')
    parser.add_argument('input_file', help="source file with assembly code")
    parser.add_argument('target_file', help="target file to hold binary machine code")
    args = parser.parse_args()

    # check if input_file is actually a file
    source_asm = read_file(logger, args.input_file)
    dest_bincode = assemble(source_asm)
    write_file(logger, args.target_file, dest_bincode)
