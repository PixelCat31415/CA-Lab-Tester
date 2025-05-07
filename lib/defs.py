# dataclass definitions

from dataclasses import dataclass

@dataclass
class Instruction:
    addr: int
    codeln: str
    codeseg: str
    lineno: int

    inst: str | None = None
    rs1: int | None = None
    rs2: int | None = None
    imm: int | None = None
    rd: int | None = None
    label: str | None = None

INST_NOPS = Instruction(0, "nops", "nops", -1, "nops", 0, 0, 0, 0, None)


@dataclass
class Testcase:
    asm: str | None = None
    bincode: str | None = None
    output: str | None = None
    expected: str | None = None
