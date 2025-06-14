AK-VM-1 is virtual machine written in C that simulates a fantasy 16-bit CPU with its own ISA. The goal of the project is to learn how computers actually work on the lowest level, explore systems programming and maybe create a tiny digital microcosm, with its own hardware and software.

ALL CODE IS ENTIRELY HUMAN-WRITTEN (NO AI).

### Usage:
Assembling program.asm into output.bin binary:
```
python assembler.py program.asm -o output.bin
```

Running output.bin:
```
./akvm output.bin
```

Redirecting debug output to file:
```
./akvm program.bin 2> output.txt
```

### Features:

- 8 16-bit general purpose registers and PC, SP, flags (Z, C, S)
- 64 KB flat memory
- Stack (grows downwards)
- Instructions are encoded as 1, 2 or  4-byte bytecodes
- Functions (via CALL, args passed via stack)
- Serial I/O and graphics mode
- Little-endian

### Memory layout:
```
[0x0000 - 0x3FFF] - program space (16 KB)
[0x4000 - 0xD6FF] - general purpose memory (~38 KB)
[0xD700 - 0xDEFF] - stack (2 KB)
[0xDF00-0xFEFF] - video memory (8 KB)
[0xFF00 - 0xFFFF] - other I/O (256 bytes)
```

### Addressing modes:
- Immediate (I): literal value
- Register (R): by specified register
- Direct memory (D): by specified address
- Indirect memory (M): by address in specified register

### ISA:

#### Control flow:
```
CMP R R/I - compares and sets flags
JMP label - sets PC to said adress
JZ label - jumps if Z flag is set
JNZ label - jump if not Z
JMC label - jump if not Z
JMS label - jump if not Z
CALL label - saves PC to stack and jumps
RET - retrieves PC from stack
NOP - does nothing
HLT - stops execution
```

#### Memory:
```
MOV R R/I - copies value from src to dst
STOR D/M R/I - stores value from src in memory
LOAD R D/M - loads value from memory to dst
PUSH R - pushes value to stack
POP R - pops value from stack
```

#### Arithmetics:
```
ADD R R/I - adds src to dst
SUB R R/I - subs src from dst
INC R - increments by 1
DEC R - decrements by 1
MUL R R/I
```

#### Bit ops:
```
AND R R/I
OR R R/I
XOR R R/I
NOT R
SHR R

### Encoding:
Every bytecode is 1-byte, 2-byte or 4-byte depending on instruction. Different addressing modes are actually resolved to different opcodes (e.g ADDI, ADDR). Some opcodes have 1 byte (NOP, HLT, RET), some 2 bytes and some 4.
Byte 1: [8 bits: opcode]
Byte 2: [3 bits: reg1, 3 bits: reg2, 2 bits: idk]
Byte 3-4: [16 bits: immediate or address]

0x00-0x0F - Control flow
0x10-0x1F - Memory
0x20-0x2F - Arithmetics
0x30-0x3F - Bit ops
0x40-0x4F - System/debug

### I/O:

#### Serial I/O. 
```
[0xFF00] - serial input (RX), read a char;
[0xFF01] - serial output (TX), write a char;
[0xFF02] - status register;
[0xFF03] - refresh screen trigger;
```

Bit | Name          | Meaning
----|---------------|-----------------------------------------
 0  | RX_READY      | 1 = New byte is available in RX
 1  | TX_READY      | 1 = TX is ready to accept a new byte
 2  | RX_OVERFLOW   | 1 = RX was overwritten before being read
 3  | TX_BUSY       | 1 = TX is still sending previous byte
... | (others)      | e.g., parity error, framing error, etc.


#### Graphics mode: 

palette in [0xDF00 - 0xDF1F] and pixel indexes in [0xDF20 - 0xFEFF].
indexed with 16-color palette and 16-bit colors
160*100 resolution (probably)
2 pixels per byte
8 kB framebuffer
updates triggered via specific address


### Assembly features:
- Opcodes resolution;
- Labels;
- Raw data embedding (decimal, binary, hex, string);
- Macros/constants.