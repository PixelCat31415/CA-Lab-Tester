# definition of instruction objects

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


# logging

import logging
import os

class CustomFormatter(logging.Formatter):

    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREY = '\x1b[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    format = "%(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: GREY + format + ENDC,
        logging.INFO: format,
        logging.WARNING: YELLOW + format + ENDC,
        logging.ERROR: RED + format + ENDC,
        logging.CRITICAL: RED + BOLD + format + ENDC
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def get_logger(module_name, debug = False):
    level = logging.DEBUG if debug else logging.INFO
    logger = logging.getLogger(module_name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger

def read_file(logger: logging.Logger, file_path: str) -> str:
    # logger.info(f"Reading from {file_path}")
    if not os.path.isfile(file_path):
        logger.error(f"Reading from file {file_path}, which is not a regular file")
        raise ValueError()
    try:
        with open(file_path) as f:
            cont = f.read()
    except Exception as e:
        logger.error(f"Failed to read from file {file_path}")
        raise e
    return cont

def write_file(logger: logging.Logger, file_path: str, content: str) -> None:
    # logger.info(f"Writing binary code to {file_path}")
    try:
        with open(file_path, "w") as f:
            f.write(content)
    except Exception as e:
        logger.error(f"Failed to write to instruction file `{file_path}`")
        raise e


# compare last n lines of strings
# returns True if identical

def compare_last(src_1: str, src_2: str, line_count: int = 19) -> bool:
    src_1 = "\n".join(src_1.split("\n")[-line_count:])
    src_2 = "\n".join(src_2.split("\n")[-line_count:])
    return src_1 == src_2


# random

def rand_until(rand_func, check_func):
    ret = None
    while ret is None or not check_func(ret):
        ret = rand_func()
    return ret
