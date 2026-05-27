# AK-VM-1

## Overview

AK-VM consists of virtual machine written in C and assembler in Python. VM simulates a hypothetical 16-bit CPU with its own ISA. 

The goal of the project is to learn how computers actually work on the lowest level, explore systems programming and maybe create a tiny digital microcosm, with its own hardware and software.

All code is human-written.

## Features:
- 16-bit VM
- custom ISA
- assembler
    - labels
    - expressions
    - constants
- console I/O
- variable-length encoding
- object files

## Usage:
Compilation:
```
clang akvm.c -o build/akvm -Wall -Wextra -O3
```

Assembling program.asm into output.bin binary:
```
python assembler.py program.asm -o output.bin -f bin
```

Running output.bin:
```
./build/akvm output.bin
```

Redirecting debug output to file:
```
./akvm program.bin 2> output.txt
```