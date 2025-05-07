import os
import argparse
from util import *
from defs import *

logger = get_logger("Generator")

script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
tests_dir = os.path.join(script_dir, "tests")

parser = argparse.ArgumentParser(
            prog='gen_testcase.py',
            description='Generate testcases')
args = parser.parse_args()


check_dir_exists(logger, tests_dir)
clear_directory(logger, tests_dir)


from testcases import testcase_groups
from assembler import assemble
from simulator import simulate
tot_test = 0
tot_generated = 0
test_summary: list[dict] = []
for group_name, testcases in testcase_groups:
    group_summary: list[str] = []
    for testid, testcase in enumerate(testcases):
        tot_test += 1
        test_name = f"{group_name}-{testid:02d}"
        try:
            if testcase.bincode is None:
                testcase.bincode = assemble(testcase.asm)
            testcase.output = simulate(testcase.bincode)
            write_file(logger, os.path.join(tests_dir, f"{test_name}.in"), testcase.bincode)
            write_file(logger, os.path.join(tests_dir, f"{test_name}.out"), testcase.output)
        except Exception as e:
            logger.error(f"Testcase {test_name}: assembler/simulator failed")
            continue
        if testcase.expected is not None and not compare_last(testcase.output, testcase.expected):
            logger.error(f"Testcase {test_name}: simulation result does not match expected output")
        else:
            logger.info(f"Testcase {test_name}: generation OK")
            tot_generated += 1
            group_summary.append(test_name)
    test_summary.append({
        "name": group_name,
        "tests": group_summary
    })
logger.info(f"Successfully generated {tot_generated} out of {tot_test} testcases")


import json

write_file(logger, os.path.join(tests_dir, "summary.json"), json.dumps(test_summary))
