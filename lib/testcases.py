from util import *
from defs import *
from data.util import *
import os.path

logger = get_logger("Testcases")


# import generator functions from data/
# modifying sys.path because python imports are dumb

import sys
script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(script_dir)

from data.gen_branch_hazard import gen_branch_hazard


testcase_groups: list[tuple[str, list[Testcase]]] = [
    ("sample", [
        from_bincode("instruction_1.txt", "output_1.txt"),
        from_bincode("instruction_2.txt", "output_2.txt"),
        from_bincode("instruction_3.txt", "output_3.txt"),
        from_bincode("instruction_4.txt", "output_4.txt"),
    ]),
    ("branch_hazard", [
        gen_branch_hazard(i) for i in range(6)
    ]),
]


if __name__ == '__main__':
    raise RuntimeError("This module is not meant to be run as a script")
