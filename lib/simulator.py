from util import *
from defs import *
from cpu import Cpu
import argparse
import re


logger = get_logger("Simulator")


# returns: list of 32-bit binary strings
def parse_bincode(lines: list[str]) -> list[tuple[str, Instruction]]:
    insts: list[Instruction] = []
    for lineno, ln in enumerate(lines, start=1):
        ln = ln.strip()
        code = re.sub(r'//.*$', '', ln)
        for it in code.split():
            if len(it) == 0:
                continue
            tok = it.replace("_", "")
            if not (re.match(r'^[01]+$', tok) and len(tok) == 32):
                logger.error(f"Token `{tok}` is not a 32-bit binary number with underscores")
                logger.info(f"At line {lineno}: {ln}")
                raise ValueError()
            inst = Instruction(addr=len(insts) * 4, codeln=ln, codeseg=it, lineno=lineno)
            insts.append((tok, inst))
    return insts


def parse_instruction(bincode: str, inst: Instruction) -> Instruction:
    fun7 = int(bincode[0:7], 2)
    rs2 = int(bincode[7:12], 2)
    rs1 = int(bincode[12:17], 2)
    fun3 = int(bincode[17:20], 2)
    rd = int(bincode[20:25], 2)
    opcode = int(bincode[25:32], 2)
    inst.rs2 = rs2
    inst.rs1 = rs1
    inst.rd = rd
    match opcode:
        case 0b0110011:
            # R-type
            match (fun7 << 3) + fun3:
                case 0b111:
                    inst.inst = "and"
                case 0b100:
                    inst.inst = "xor"
                case 0b001:
                    inst.inst = "sll"
                case 0b000:
                    inst.inst = "add"
                case 0b0100000000:
                    inst.inst = "sub"
                case 0b0000001000:
                    inst.inst = "mul"
                case _:
                    raise SyntaxError()
        case 0b0010011:
            # I-type
            match fun3:
                case 0b000:
                    inst.inst = "addi"
                    inst.imm = (fun7 << 5) + rs2
                case 0b101:
                    if fun7 != 0b0100000:
                        raise SyntaxError()
                    inst.inst = "srai"
                    inst.imm = rs2
                case _:
                    raise SyntaxError()
        case 0b0000011:
            # lw
            inst.inst = "lw"
            inst.imm = (fun7 << 5) + rs2
        case 0b0100011:
            # sw
            inst.inst = "sw"
            inst.imm = (fun7 << 5) + rd
        case 0b1100011:
            # beq
            inst.inst = "beq"
            imm_str = bincode[0] + bincode[24] + bincode[1:7] + bincode[20:24]
            inst.imm = int(imm_str, 2)
        case _:
            raise SyntaxError()
    return inst


def parse_instructions(bincodes: list[tuple[str, Instruction]]) -> list[Instruction]:
    insts: list[Instruction] = []
    for instno, it in enumerate(bincodes, start=1):
        bincode, inst = it
        try:
            inst = parse_instruction(bincode, inst)
            insts.append(inst)
        except Exception as e:
            logger.error(f"Illegal instruction `{bincode}`")
            logger.info(f"At instruction {instno}: {inst.codeseg}")
            logger.info(f"At line {inst.lineno}: {inst.codeln}")
            raise e
    return insts


def simulate(source_bincode: str) -> str:
    # decode binary code into instructions
    try:
        code = parse_bincode(source_bincode.split("\n"))
        insts = parse_instructions(code)
    except Exception as e:
        logger.error(f"Failed to parse binary code")
        raise e
    
    # initialize CPU with instructions, along with default values in register file and data memory
    try:
        cpu = Cpu(
            insts,
            registers = {
                24: -24,
                25: -25,
                26: -26,
                27: -27,
                28: 56,
                29: 58,
                30: 60,
                31: 62,
            },
            datamem = {
                0: 5,
                1: 6,
                2: 10,
                3: 18,
                4: 29,
            }
        )
    except Exception as e:
        logger.error("Failed to initialize CPU")
        raise e
    
    # do simulation for 63 cycles, and dump the CPU state at the beginning of the 64-th cycle
    try:
        output = ""
        for _ in range(63):
            cpu.run_cycle()
        output += cpu.dump_states()
        output += cpu.dump_registers()
        output += cpu.dump_data()
        output += "\n\n"
    except Exception as e:
        logger.error(f"Failed to simulate CPU execution")
        raise e
    return output


def compare_output(output: str, expected: str):
    if output == expected:
        logger.info(f"Output matches the expected output")
    else:
        logger.warning(f"Output does not match the expected output")
        # logger.warning(f"Output:")
        # print(output)
        # logger.warning(f"Expected:")
        # print(expected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                prog='simulator.py',
                description='CPU simulator for Lab 2 simplified RISC-V instruction set',
                epilog='The CPU is simulated for 63 cycles. At the beginning of the 64-th cycle, the CPU state is dumpped to the target file.')
    parser.add_argument('input_file', help="source file with binary machine code")
    parser.add_argument('target_file', help="target file to hold output of CPU simulation")
    parser.add_argument('--expected_file', help="if provided, the target file will be compared against this file. only the content of registers and data memory will be compared; the program counter and cycle/stall/flush counts are not compared")
    args = parser.parse_args()

    source_bincode = read_file(logger, args.input_file)
    output = simulate(source_bincode)
    write_file(logger, args.target_file, output)
    if args.expected_file is not None:
        expected = read_file(logger, args.expected_file)
        compare_output(output, expected)
        logger.info(f"Expected {args.expected_file}, got {args.target_file}")

