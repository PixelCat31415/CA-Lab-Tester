import os
import os.path
import shutil
import argparse
from util import get_logger, write_file, compare_last

logger = get_logger("Generator")

script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
gen_dir = os.path.join(script_dir, "gen")
tests_dir = os.path.join(script_dir, "tests")

parser = argparse.ArgumentParser(
            prog='gen_testcase.py',
            description='Generate testcases')
args = parser.parse_args()

def check_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        logger.warning(f"directory {dir_path} does not exist; creating one")
        os.mkdir(dir_path)
    if not os.path.isdir(dir_path):
        logger.error(f"{dir_path} is not a directory")
        raise ValueError()
check_dir_exists(gen_dir)
check_dir_exists(tests_dir)

def clear_directory(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.error(f"Failed to delete {file_path} when clearing {dir_path}")
            raise e
clear_directory(tests_dir)


from testcases import testcase_groups
from assembler import assemble
from simulator import simulate
tot_test = 0
tot_generated = 0
for group_name, testcases in testcase_groups:
    for testid, testcase in enumerate(testcases):
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
        tot_test += 1
logger.info(f"Successfully generated {tot_generated} out of {tot_test} testcases")
