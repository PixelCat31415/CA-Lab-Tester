# cp ../testcases/instruction_15.txt instruction.txt
# iverilog -o ./cpu ../code/**/*.v
# vvp ./cpu
# python ../gen/simulator.py ./instruction.txt ./simulated.txt --expected_file ./output.txt

from util import *
import argparse
import json
import subprocess

logger = get_logger("Invoker")


parser = argparse.ArgumentParser(
            prog='invoke.py',
            description='Compile and run the CPU, and compare the output against simulated result')
parser.add_argument('source_dir', help="directory containing source code of the CPU (typically lab2/code)")
args = parser.parse_args()
source_dir = os.path.abspath(args.source_dir)


script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
tests_dir = os.path.join(script_dir, "tests")
sandbox_dir = os.path.join(script_dir, "sandbox")
log_dir = os.path.join(script_dir, "log")

check_dir_exists(logger, tests_dir)
check_dir_exists(logger, sandbox_dir)
check_dir_exists(logger, log_dir)
clear_directory(logger, sandbox_dir)
clear_directory(logger, log_dir)
os.chdir(sandbox_dir)

inst_file = os.path.join(sandbox_dir, "instruction.txt")
output_file = os.path.join(sandbox_dir, "output.txt")
waveform_file = os.path.join(sandbox_dir, "waveform.vcd")


# compile CPU
source_files = os.path.join(source_dir, '**', '*.v')
cpu_program = os.path.join(sandbox_dir, "cpu")
try:
    with open(os.path.join(log_dir, f"iverilog-stdout.txt"), "w") as iverilog_stdout, \
            open(os.path.join(log_dir, f"iverilog-stderr.txt"), "w") as iverilog_stderr:
        proc = subprocess.run(f"iverilog -o {cpu_program} {source_files}", shell=True, stdout=iverilog_stdout, stderr=iverilog_stderr)
except Exception as e:
    logger.error(f"Failed to compile CPU program: failed to execute iverilog")
    raise e
if proc.returncode != 0:
    logger.error(f"Failed to compile CPU program: iverilog finished with return code {proc.returncode}")
    raise RuntimeError()
logger.info(f"Compilation completed")


# run tests

try:
    test_summary = json.loads(read_file(logger, os.path.join(tests_dir, "summary.json")))
except Exception as e:
    logger.error(f"Failed to load tests from directory {tests_dir}. Have you run the generator?")
    raise e

tot_tests = 0
tot_passed = 0
for group in test_summary:
    group_name = group["name"]
    test_names = group["tests"]
    group_passed = 0
    for test_name in test_names:
        test_inst = os.path.join(tests_dir, f"{test_name}.in")
        test_output = os.path.join(tests_dir, f"{test_name}.out")
        shutil.copyfile(test_inst, inst_file)
        try:
            with open(os.path.join(log_dir, f"{test_name}-vvp-stdout.txt"), "w") as vvp_stdout, \
                    open(os.path.join(log_dir, f"{test_name}-vvp-stderr.txt"), "w") as vvp_stderr:
                proc = subprocess.run(["vvp", cpu_program], stdout=vvp_stdout, stderr=vvp_stderr)
        except Exception as e:
            logger.info(f"Test '{test_name}' - RE: vvp failed to execute CPU program")
            continue
        if proc.returncode != 0:
            logger.info(f"Test '{test_name}' - RE: vvp finished with return code {proc.returncode}")
            continue
        shutil.copyfile(output_file, os.path.join(log_dir, f"{test_name}-output.txt"))
        shutil.copyfile(waveform_file, os.path.join(log_dir, f"{test_name}-waveform.txt"))
        try:
            output = read_file(logger, output_file)
            expected = read_file(logger, test_output)
        except Exception as e:
            logger.error(f"Test '{test_name}' - Judge Error: failed to read CPU output and simulation result")
            logger.error(f"what: {e}")
            continue
        if compare_last(output, expected):
            logger.info(f"Test '{test_name}' - AC")
            group_passed += 1
        else:
            logger.info(f"Test '{test_name}' - WA: CPU output differs from simulation result")
    logger.info(f"Group '{group_name}' - {group_passed} out of {len(test_names)} tests passed")
    tot_passed += group_passed
    tot_tests += len(test_names)
logger.info(f"Total - {tot_passed} out of {tot_tests} tests passed ({tot_tests - tot_passed} failed)")
