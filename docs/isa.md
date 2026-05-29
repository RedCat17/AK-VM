# ISA

## Features

- 16 general purpose 16-bit registers
- PC, SP, flags (Z, C, S) registers
- 64 KB flat byte-addressable memory
- Stack (grows downwards)
- Variable-length instructions (1, 2, 4-byte)
- Functions (via CALL, args passed via stack)
- Serial I/O
- Little-endian

## Addressing modes
- Immediate (I): literal value
- Register (R): by specified register
- Direct memory (D): by specified address
- Indirect memory (M): by address in specified register

## Encoding formats
Every instruction is 1-byte, 2-byte or 4-byte depending on opcode. Each opcode has a single specific encoding type.

### NONE
```
Byte 1: [8 bits: opcode]
```

### REG
```
Byte 1: [8 bits: opcode]
Byte 2: [4 bits: reg1, 4 bits: reserved]
```

### REG_REG
```
Byte 1: [8 bits: opcode]
Byte 2: [4 bits: reg1, 4 bits: reg2]
```

### IMM
```
Byte 1: [8 bits: opcode]
Byte 3-4: [16 bits: immediate or address]
```

### REG_IMM
```
Byte 1: [8 bits: opcode]
Byte 2: [4 bits: reg1, 4 bits: reserved]
Byte 3-4: [16 bits: immediate or address]
```

## Symbols:
- Imm - immediate operand or address
- Reg - register operand (R0-R15)

## Opcode Table

### Control Flow

| Mnemonic           | Instruction                          | Opcode |
|--------------------|--------------------------------------|--------|
| [NOP](#nop)        | No operation                         | 0x00   |
| [HLT](#hlt)        | Stop execution                       | 0x01   |
| [CMPR](#cmpr)      | Compare values and set flags         | 0x02   |
| [CMPI](#cmpi)      | -                                    | 0x03   |
| [JMP](#jmp)        | Unconditional jump                   | 0x04   |
| [JZ](#jz)          | Jump if Z flag is set                | 0x05   |
| [JNZ](#jnz)        | Jump if not Z                        | 0x06   |
| [JC](#jc)          | Jump if C                            | 0x07   |
| [JS](#js)          | Jump if S                            | 0x08   |
| [CALL](#call)      | Save PC to stack and jump            | 0x09   |
| [RET](#ret)        | Retrieve PC from stack               | 0x0A   |

### Memory

| Mnemonic           | Instruction                          | Opcode |
|--------------------|--------------------------------------|--------|
| [MOVR](#movr)      | Copy word from src to dst            | 0x10   |
| [MOVI](#movi)      | -                                    | 0x11   |
| [STOR](#stor)      | Store word to memory                 | 0x12   |
| [LOAD](#load)      | Loads word from memory to dst        | 0x15   |
| [PUSH](#push)      | Pushes word to stack                 | 0x17   |
| [POP](#pop)        | Pops word from stack                 | 0x18   |
| [STORB](#storb)    | Stores byte from src in memory       | 0x19   |
| [LOADB](#loadb)    | Loads byte from memory to dst        | 0x1B   |

### Arithmetics

| Mnemonic           | Instruction                          | Opcode |
|--------------------|--------------------------------------|--------|
| [ADDR](#addr)      | Adds src to dst                      | 0x20   |
| [ADDI](#addi)      | -                                    | 0x21   |
| [SUBR](#subr)      | Subs src from dst                    | 0x22   |
| [SUBI](#subi)      | -                                    | 0x23   |
| [INC](#inc)        | Increments by 1                      | 0x24   |
| [DEC](#dec)        | Decrements by 1                      | 0x25   |
| [MULR](#mulr)      | Multiplies R by R                    | 0x26   |
| [MULI](#muli)      | Multiplies R by I                    | 0x27   |
| [DIVR](#divr)      | Divides R by R                       | 0x28   |
| [DIVI](#divi)      | Divides R by I                       | 0x29   |

### Bit ops

| Mnemonic           | Instruction                          | Opcode |
|--------------------|--------------------------------------|--------|
| [ANDR](#andr)      | Bitwise AND                          | 0x30   |
| [ANDI](#andi)      | -                                    | 0x31   |
| [ORR](#orr)        | Bitwise OR                           | 0x32   |
| [ORI](#ori)        | -                                    | 0x33   |
| [XORR](#xorr)      | Bitwise XOR                          | 0x34   |
| [XORI](#xori)      | -                                    | 0x35   |
| [NOT](#not)        | Bitwise NOT                          | 0x36   |
| [SHR](#shr)        | Shift right                          | 0x37   |
| [SHL](#shl)        | Shift left                           | 0x38   |

### SP and BP ops

| Mnemonic           | Instruction                          | Opcode |
|--------------------|--------------------------------------|--------|
| [SETSP](#setsp)    | Set SP                               | 0x40   |
| [GETSP](#getsp)    | Get SP value                         | 0x41   |
| [ADDSP](#addsp)    | Add SP                               | 0x42   |
| [SUBSP](#subsp)    | Subtract SP                          | 0x43   |
| [SETBP](#setbp)    | Set BP                               | 0x44   |
| [GETBP](#getbp)    | Get BP value                         | 0x45   |
| [ADDBP](#addbp)    | Add BP                               | 0x46   |
| [SUBBP](#subbp)    | Subtract BP                          | 0x47   |

## Opcodes

### NOP

**Description:**

No operation. Does nothing.

**Encoding:**
```
byte1: 0x00
```

**Operands:**

None

**Flags affected:**

None

**Example:** 

NOP

### HLT

**Description:**

Stop execution, halt VM.

**Encoding:**
```
byte1: 0x01
```

**Operands:**
- None

**Flags affected:**

None

**Example:** 

HLT

### CMPR

CMPR reg1, reg2

**Description:**

Compare 2 registers and set flags.

**Operation:**

```
Z = reg1 - reg2 == 0:
S = (reg1 - reg2) & 0x8000
C = reg < reg2
```

**Encoding:**
```
byte1: 0x02
byte2: reg1 | reg2
```

**Operands:**
- reg1
- reg2

**Flags affected:**

Z, C, S

**Example:** 

CMPR R0, R1

### CMPI

CMPI reg1, imm

**Description:**

Compare register with immediate value and set flags.

**Operation:**

```
Z = reg1 - imm == 0:
S = (reg1 - imm) & 0x8000
C = reg < imm
```

**Encoding:**
```
byte1: 0x03
byte2: reg1 | 0000
byte3, byte4: imm
```

**Operands:**
- reg1
- imm

**Flags affected:**

Z, C, S

**Example:** 

CMPI R0, 10

### JMP

JMP imm

**Description:**

Uncoditional jump to address. Sets PC to imm.

**Operation:**

```
PC = imm
```

**Encoding:**
```
byte1: 0x04
byte2, byte3: imm
```

**Operands:**
- imm

**Flags affected:**

None

**Example:** 

JMP label

### JZ

JZ imm

**Description:**

Jump to address if Zero flag is set. Sets PC to imm.

**Operation:**

```
if Zero:
    PC = imm
```

**Encoding:**
```
byte1: 0x05
byte2, byte3: imm
```

**Operands:**
- imm

**Flags affected:**

None

**Example:** 

JZ label

### JNZ

JNZ imm

**Description:**

Jump to address if Zero flag is not set. Sets PC to imm.

**Operation:**

```
if !Zero:
    PC = imm
```

**Encoding:**
```
byte1: 0x06
byte2, byte3: imm
```

**Operands:**
- imm

**Flags affected:**

None

**Example:** 

JNZ label

### JC

JC imm

**Description:**

Jump to address if Carry flag is set. Sets PC to imm.

**Operation:**

```
if Carry:
    PC = imm
```

**Encoding:**
```
byte1: 0x07
byte2, byte3: imm
```

**Operands:**
- imm

**Flags affected:**

None

**Example:** 

JC label

### JS

JS imm

**Description:**

Jump to address if Sign flag is set. Sets PC to imm.

**Operation:**

```
if Sign:
    PC = imm
```

**Encoding:**
```
byte1: 0x08
byte2, byte3: imm
```

**Operands:**
- imm

**Flags affected:**

None

**Example:** 

JS label

### CALL

CALL imm

**Description:**

Call function. Jump to address and push PC to stack.

**Operation:**

```
push PC
PC = imm
```

**Encoding:**
```
byte1: 0x09
byte2, byte3: imm
```

**Operands:**
- imm

**Flags affected:**

None

**Example:** 

CALL label

### RET

RET

**Description:**

Return from function. Pop PC from stack.

**Operation:**

```
pop PC
```

**Encoding:**
```
byte1: 0x0A
```

**Flags affected:**

None

**Example:** 

RET