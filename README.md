# CA Lab 2 Tester

## Features

- Assemble RISC-V assembly into binary code that could be fed into the verilog testbench (only for instructions included in the spec)
- Simulate expected behavior of a series of instructions and save the final state (registers and data memory)
- Compile and run the CPU module
- Compare the CPU's output against the simulated result

## Usage

- `lib/testcases.py`: defines the testcases
- `lib/gen.py`: generates testcases from `lib/testcases.py`
- `lib/invoke.py source_dir`: compile, run, and compare the output of the CPU

Pass `-h` option to the scripts to check usage.
