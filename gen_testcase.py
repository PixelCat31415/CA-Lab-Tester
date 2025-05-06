import os
import os.path
import shutil
import argparse
import re
from util import get_logger

logger = get_logger("Testcase Generator")

script_dir = os.path.dirname(os.path.realpath(__file__))
script_dir_rel = os.path.relpath(script_dir, os.getcwd())
default_assembly_dir = os.path.join(script_dir_rel, "assembly")
default_bincode_dir = os.path.join(script_dir_rel, "bincode")
default_simulated_dir = os.path.join(script_dir_rel, "simulated")

parser = argparse.ArgumentParser(
            prog='gen_testcase.py',
            description='Generate testcases from assembly code')
parser.add_argument(
    'assembly_dir',
    nargs="?",
    default=default_assembly_dir,
    help=f"the directory holding assembly code, one for each testcase. defaults to '{default_assembly_dir}'"
)
parser.add_argument(
    'bincode_dir',
    nargs="?",
    default=default_bincode_dir,
    help=f"the directory to hold assembled binary code. defaults to '{default_bincode_dir}'"
)
parser.add_argument(
    'simulated_dir',
    nargs="?",
    default=default_simulated_dir,
    help=f"the directory to hold simulation output. defaults to '{default_simulated_dir}'"
)
parser.add_argument(
    "--clear",
    action="store_true",
    help="clear bincode_dir and simulated_dir before generation"
)
parser.add_argument(
    "--testcases_dir",
    help="copy generated binary code to this directory as instruction files, and copy simulated output as expected output"
)
args = parser.parse_args()

assembly_dir: str = args.assembly_dir
bincode_dir: str = args.bincode_dir
simulated_dir: str = args.simulated_dir
flag_clear: bool = args.clear
testcases_dir: str = args.testcases_dir

def check_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        logger.warning(f"directory {dir_path} does not exist; creating one")
        os.mkdir(dir_path)
    if not os.path.isdir(dir_path):
        logger.error(f"{dir_path} is not a directory")
        raise ValueError()
check_dir_exists(assembly_dir)
check_dir_exists(bincode_dir)
check_dir_exists(simulated_dir)
if testcases_dir is not None:
    check_dir_exists(testcases_dir)

if flag_clear:
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
    clear_directory(bincode_dir)
    clear_directory(simulated_dir)

from assembler import assemble
from simulator import simulate
for filename in os.listdir(assembly_dir):
    filepath: str = os.path.join(assembly_dir, filename)
    if not os.path.isfile(filepath):
        logger.warning(f"Skipping {filename}: not a regular file")
        continue

    testid_str: str = os.path.splitext(os.path.basename(filename))[0]
    if not re.match(r"^[1-9][0-9]*$", testid_str):
        logger.warning(f"Skipping {filename}: filename is not a number without leading zeros")
        continue
    testid: int = int(testid_str)

    if 1 <= testid <= 4:
        logger.warning(f"Skipping {filename}: testcase id conflicts with default testcases")
        continue
    
    logger.info(f"Generating testcase for {filename} (id = {testid})")
    bincode_path = os.path.join(bincode_dir, f"instruction_{testid}.txt")
    simulated_path = os.path.join(simulated_dir, f"simulation_{testid}.txt")
    assemble(filepath, bincode_path)
    simulate(bincode_path, simulated_path)
    if testcases_dir is not None:
        try:
            shutil.copyfile(bincode_path, os.path.join(testcases_dir, f"instruction_{testid}.txt"))
            shutil.copyfile(simulated_path, os.path.join(testcases_dir, f"output_{testid}.txt"))
        except Exception as e:
            logger.error(f"Failed to copy testcase {testid}")
            logger.error(f"what: {e}")

