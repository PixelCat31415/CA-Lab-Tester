import random
from typing import TypeVar
from util import *
from defs import *

logger = get_logger("CPU")


TCpu = TypeVar("TCpu", bound="Cpu")

# register file stores 32x u32
# data memory stores 1024x u32

class Cpu:
    def __init__(self, instructions: list[Instruction], registers: dict, datamem: dict):
        self.cycle = 0
        self.pc = 0
        self.stall = -1
        self.flush = -1
        self.instructions = instructions
        self.registers = [0 for _ in range(32)]
        self.datamem = [0 for _ in range(1024)]
        for i in registers:
            self.check_reg(i)
            self.registers[i] = self.overflow(registers[i])
        for i in datamem:
            self.check_addr(i * 4)
            self.datamem[i] = self.overflow(datamem[i])

    
    # output-related functions

    def dump_states(self) -> str:
        dump = ""
        dump += f"cycle = {self.i32(self.cycle)}, Stall = {self.stall}, Flush = {self.flush}\n"
        dump += "PC = {}\n".format(self.i32(self.pc))
        return dump
    
    def dump_registers(self) -> str:
        dump = ""
        dump += "Registers\n"
        dump += "x0 = {}, x8  = {}, x16 = {}, x24 = {}\n".format(self.i32(self.registers[ 0]), self.i32(self.registers[ 8]), self.i32(self.registers[16]), self.i32(self.registers[24]))
        dump += "x1 = {}, x9  = {}, x17 = {}, x25 = {}\n".format(self.i32(self.registers[ 1]), self.i32(self.registers[ 9]), self.i32(self.registers[17]), self.i32(self.registers[25]))
        dump += "x2 = {}, x10 = {}, x18 = {}, x26 = {}\n".format(self.i32(self.registers[ 2]), self.i32(self.registers[10]), self.i32(self.registers[18]), self.i32(self.registers[26]))
        dump += "x3 = {}, x11 = {}, x19 = {}, x27 = {}\n".format(self.i32(self.registers[ 3]), self.i32(self.registers[11]), self.i32(self.registers[19]), self.i32(self.registers[27]))
        dump += "x4 = {}, x12 = {}, x20 = {}, x28 = {}\n".format(self.i32(self.registers[ 4]), self.i32(self.registers[12]), self.i32(self.registers[20]), self.i32(self.registers[28]))
        dump += "x5 = {}, x13 = {}, x21 = {}, x29 = {}\n".format(self.i32(self.registers[ 5]), self.i32(self.registers[13]), self.i32(self.registers[21]), self.i32(self.registers[29]))
        dump += "x6 = {}, x14 = {}, x22 = {}, x30 = {}\n".format(self.i32(self.registers[ 6]), self.i32(self.registers[14]), self.i32(self.registers[22]), self.i32(self.registers[30]))
        dump += "x7 = {}, x15 = {}, x23 = {}, x31 = {}\n".format(self.i32(self.registers[ 7]), self.i32(self.registers[15]), self.i32(self.registers[23]), self.i32(self.registers[31]))
        return dump
    
    def dump_data(self) -> str:
        dump = ""
        for i in range(8):
            dump += f"Data Memory: 0x{i * 4:02X} = {self.i32(self.datamem[i])}\n"
        return dump

    def i32(self, value: int) -> str:
        return f"{self.signed(value, 32):>10d}"


    # utility functions for 32-bit integer arithmetic simulation

    def check_reg(self, reg: int) -> None:
        if not 0 <= reg < 32:
            logger.error(f"Invalid register '{reg}'")
            raise RuntimeError()

    def check_imm(self, imm: int, width: int) -> None:
        if not 0 <= imm < 2 ** width:
            logger.error(f"Invalid immediate '{imm}' of width '{width}'")
            raise RuntimeError()
    
    def check_addr(self, addr: int) -> None:
        if addr < 0 or addr >= len(self.datamem) * 4:
            logger.error(f"Address `{addr}` out of bounds [0, 4096)")
            raise RuntimeError()
        if addr % 4 != 0:
            logger.error(f"Address `{addr}` is not word-aligned, as required in Data_Memory.v")
            raise RuntimeError()

    def overflow(self, value: int) -> int:
        return value % (2 ** 32)
    
    def sext(self, value: int, width: int) -> int:
        if value & (2 ** (width - 1)) != 0:
            value += 2 ** 32 - 2 ** width
        return value

    def signed(self, value: int, width: int) -> int:
        hibit = 2 ** (width - 1)
        value = (value + hibit) % (2 ** width) - hibit
        return value
    
    def store_data(self, addr: int, value: int) -> None:
        self.check_addr(addr)
        self.datamem[addr // 4] = self.overflow(value)
    
    def load_data(self, addr: int) -> int:
        self.check_addr(addr)
        return self.datamem[addr // 4]


    # simulate instructions

    def run_cycle(self) -> None:
        try:
            inst = self.fetch_instruction()
        except Exception as e:
            logger.error("Failed to fetch instruction")
            logger.info(f"On cycle {self.cycle}")
            raise e
        try:
            logger.debug(f"Cycle {self.cycle}: {inst}")
            self.run_instruction(inst)
        except Exception as e:
            logger.error("Failed to execute instruction")
            logger.info(f"On cycle {self.cycle}, pc = {self.pc}")
            logger.info(f"Failed instruction: {inst}")
            raise e
        self.cycle += 1

    def fetch_instruction(self) -> Instruction:
        if self.pc % 4 != 0:
            logger.error(f"Program counter {self.pc} is not multiple of 4")
            raise RuntimeError()
        if not 0 <= self.pc < 256 * 4:
            logger.error(f"Program counter {self.pc} out of range [0, 256 * 4)")
            raise RuntimeError()
        if self.pc // 4 >= len(self.instructions):
            return INST_NOPS
        return self.instructions[self.pc // 4]

    def run_instruction(self, inst: Instruction) -> None:
        rd, rs1, rs2, imm = inst.rd, inst.rs1, inst.rs2, inst.imm
        def check_inst(check_rd: bool, check_rs1: bool, check_rs2: bool, check_imm: int):
            self.check_reg(rd) if check_rd else None
            self.check_reg(rs1) if check_rs1 else None
            self.check_reg(rs2) if check_rs2 else None
            self.check_imm(imm, check_imm) if check_imm > 0 else None
        def check_rtype():
            check_inst(True, True, True, 0)
        def check_itype(imm_width):
            check_inst(True, True, False, imm_width)
        match inst.inst:
            case "and":
                check_rtype()
                self.registers[rd] = self.registers[rs1] & self.registers[rs2]
            case "xor":
                check_rtype()
                self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]
            case "sll":
                check_rtype()
                if self.registers[rs2] > 32:
                    self.registers[rd] = 0
                else:
                    self.registers[rd] = self.overflow(self.registers[rs1] * (2 ** self.registers[rs2]))
            case "add":
                check_rtype()
                self.registers[rd] = self.overflow(self.registers[rs1] + self.registers[rs2])
            case "sub":
                check_rtype()
                self.registers[rd] = self.overflow(self.registers[rs1] - self.registers[rs2])
            case "mul":
                check_rtype()
                self.registers[rd] = self.overflow(self.registers[rs1] * self.registers[rs2])
            case "addi":
                check_itype(12)
                imm = self.sext(imm, 12)
                self.registers[rd] = self.overflow(self.registers[rs1] + imm)
            case "srai":
                check_itype(5)
                val = self.registers[rs1]
                for _ in range(imm):
                    if val & (2 ** 31) != 0:
                        val += 2 ** 32
                    val = val // 2
                self.registers[rd] = val
            case "lw":
                check_inst(True, True, False, 12)
                imm = self.signed(imm, 12)
                self.registers[rd] = self.load_data(self.registers[rs1] + imm)
            case "sw":
                check_inst(False, True, True, 12)
                imm = self.signed(imm, 12)
                self.store_data(self.registers[rs1] + imm, self.registers[rs2])
            case "beq":
                check_inst(False, True, True, 12)
                imm = self.signed(imm, 12)
                if self.registers[rs1] == self.registers[rs2]:
                    self.pc += imm * 2
                else:
                    self.pc += 4
            case "nops":
                pass
            case _:
                logger.error(f"Illegal instruction")
                raise RuntimeError()
        if inst.inst != "beq":
            self.pc += 4
        self.registers[0] = 0


if __name__ == '__main__':
    raise RuntimeError("This module is not meant to be run as a script")
