# RISC-V Pipeline Simulator

A Python implementation of a RISC-V (RV32I) processor simulator featuring both single-stage and 5-stage pipeline architectures.

## Overview

This project implements a functional simulator for the RISC-V 32-bit integer instruction set (RV32I). It provides two distinct pipeline implementations:
- **Single-Stage Pipeline**: Executes one instruction completely in each cycle
- **5-Stage Pipeline**: Implements the classic RISC pipeline stages (IF, ID, EX, MEM, WB)

## Features

- ✅ Full RV32I instruction set support
- ✅ Byte-addressable memory (instruction and data memory)
- ✅ 32 general-purpose registers (x0-x31)
- ✅ Hazard detection and handling in 5-stage pipeline
- ✅ Performance metrics comparison (CPI, IPC)
- ✅ Detailed state dumps for debugging

## Project Structure

```
rh3884_CSA_project/
├── main.py                    # Main simulator entry point
├── SingleStageDecode.py       # Instruction decoder for single-stage
├── SingleStageExecution.py    # Execution logic for single-stage
├── FiveStageDecode.py         # Instruction decoder for 5-stage
├── FiveStageExecution.py      # Pipeline stage implementations
└── utils.py                   # Utility functions
```

## Requirements

- Python 3.x
- No external dependencies required

## Installation

```bash
git clone https://github.com/RaghuHemadri/rh3884_CSA_project.git
cd rh3884_CSA_project
```

## Usage

Run the simulator with an input directory containing the instruction and data memory files:

```bash
python main.py --iodir <path_to_io_directory>
```

### Input Files

The IO directory must contain:
- `imem.txt` - Instruction memory (hex format, byte-addressable)
- `dmem.txt` - Data memory (hex format, byte-addressable)

### Output Files

The simulator generates:
- `StateResult_SS.txt` - Single-stage pipeline state trace
- `StateResult_FS.txt` - 5-stage pipeline state trace
- `SS_RFResult.txt` - Single-stage register file state
- `FS_RFResult.txt` - 5-stage register file state
- `SS_DMEMResult.txt` - Single-stage data memory dump
- `FS_DMEMResult.txt` - 5-stage data memory dump
- `PerformanceMetrics.txt` - Performance comparison (CPI/IPC)

## Architecture Details

### Single-Stage Pipeline
- Fetches, decodes, and executes one complete instruction per cycle
- Simpler control logic
- Higher CPI (Cycles Per Instruction)

### 5-Stage Pipeline
Implements the classic RISC pipeline:
1. **IF (Instruction Fetch)**: Fetch instruction from memory
2. **ID (Instruction Decode)**: Decode instruction and read registers
3. **EX (Execute)**: Perform ALU operations
4. **MEM (Memory)**: Access data memory for loads/stores
5. **WB (Write Back)**: Write results back to register file

Features:
- Pipeline hazard detection
- Data forwarding support
- Stall insertion when necessary

## Performance Metrics

The simulator calculates and compares:
- **CPI (Cycles Per Instruction)**: Average cycles needed per instruction
- **IPC (Instructions Per Cycle)**: Average instructions executed per cycle
- **Total Cycles**: Number of cycles to complete program execution
- **Instruction Count**: Total number of instructions executed

## Memory Organization

- **Instruction Memory**: 1000 bytes, byte-addressable
- **Data Memory**: 1000 bytes, byte-addressable
- **Register File**: 32 registers (32-bit each), with x0 hardwired to 0

## Example

```bash
python main.py --iodir ./test_programs/example1
```

This will execute the program in the specified directory and generate all output files with performance comparisons.

## Implementation Notes

- Instructions are stored in little-endian format
- Memory addresses are byte-addressable
- Register x0 is always 0 (writes to x0 are ignored)
- The simulator halts when all pipeline stages are empty (5-stage) or on HALT instruction (single-stage)

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

This project is part of a Computer Architecture course project.

## Author

Raghu Hemadri (@RaghuHemadri)
