# AK-VM-1

## Overview

AK-VM consists of virtual machine written in C and assembler in Python. VM simulates a hypothetical 16-bit CPU with its own ISA. 

The goal of the project is to learn how computers actually work on the lowest level, explore systems programming and maybe create a tiny digital microcosm, with its own hardware and software.

All code is human-written.

Licensed under MIT.

## Features

### VM:
- 16-bit VM
- custom ISA
- console I/O
- variable-length encoding
### Assembler:
- labels
- expressions evaluation
- constants (e.g. .DEF A 0x040)
- named registers (e.g. R0)
- pattern matching based on operands (e.g. MOV -> MOVR or MOVI)
- detailed error handling with line numbers
- object files
### Other
- makefile for easy building, assembling, running and testing
- automated black-box testing to expected output
- set of example programs

## Prerequisites 
- C compiler (Clang or other)
- Python 3.10+

## Building
```bash
git clone https://github.com/RedCat17/AK-VM.git
cd AK-VM
make
```

## Usage
Assembling program.asm into output.bin binary:
```bash
python asm.py program.asm -o output.bin -f bin
```

Assembling object file:
```bash
python asm.py program.asm -o output.bin -f obj
```

Running output.bin:
```bash
./build/akvm output.bin
```

Debug mode:
```bash
./build/akvm program.bin -d
```

Redirecting debug output to file:
```bash
./build/akvm program.bin -d 2> output.txt
```

Quick example for Hello World:
```bash
make run FILE=examples/hello.asm
```

Calculator example:
```bash
make run FILE=examples/calc.asm
```

Run tests:
```bash
make test
```

## Code example
"Hello world" written in Assembly for AK-VM:
```
JMP start

msg: .STR "Hello world!"

start:
    MOV R0, msg         ; load msg address to reg R0

loop:
    LOADB R1, [R0]      ; load byte from memory to R1
    CMP R1, 0           ; check for null terminator
    JZ done

    STORB R1, [0xF801]  ; send byte to TX address
    INC R0              ; increment pointer
    JMP loop

done:
    HLT                 ; stop execution
```

## Documentation

See:
- [ISA](docs/isa.md)
- [Machine](docs/machine.md)
- [Assembler](docs/assembler.md)