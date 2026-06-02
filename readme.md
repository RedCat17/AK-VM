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

## Code example
"Hello world" written in Assembly for AK-VM:
```
JMP start
msg:
.STR "Hello world!"

start:
MOV R0, msg         ; load msg address to reg R0

loop:
LOADB R1, [R0]      ; load byte from memory to R1
STORB R1, [0xF801]  ; send byte to TX address
INC R0              ; increment pointer
CMP R0, start       ; test if we reached end of string
JNZ loop

HLT                 ; stop execution
```

## Documentation

See:
- [ISA](docs/isa.md)
- [Machine](docs/machine.md)
- [Assembler](docs/assembler.md)
- [Linker](docs/linker.md)