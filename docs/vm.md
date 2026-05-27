## Features:

- 8 general purpose 16-bit registers
- PC, SP, flags (Z, C, S) registers
- 64 KB flat memory
- Stack (grows downwards)
- Variable-length instructions (1, 2, 4-byte)
- Functions (via CALL, args passed via stack)
- Serial I/O
- Little-endian

### Memory layout:
```
[0x0000 - 0x3FFF] - Program Space (16 KB)
[0x4000 - 0xEFFF] - Heap (~44 KB) 
[0xF000 - 0xF7FF] - Video Buffer (2 KB)
[0xF800 - 0xF8FF] - Mapped I/O (256 bytes)
[0xF900 - 0xFFFF] - Stack (2 KB, grows downward)
```

### Addressing modes:
- Immediate (I): literal value
- Register (R): by specified register
- Direct memory (D): by specified address
- Indirect memory (M): by address in specified register

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
[0xF800] - serial input (RX), read a char;
[0xF801] - serial output (TX), write a char;
[0xF802] - refresh screen trigger;
```