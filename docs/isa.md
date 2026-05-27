# ISA

## Symbols:
Imm - immediate operand or address
Reg - register operand (R0-R15)

## Control Flow

| Mnemonic           | Instruction                          | Opcode |
|--------------------|--------------------------------------|--------|
| [NOP](#nop)        | No operation                         | 0x00   |
| [HLT](#hlt)        | Stop execution                       | 0x01   |
| [CMPR](#cmp)       | Compare values and set flags         | 0x02   |
| [CMPI](#cmp)       | -                                    | 0x03   |
| [JMP](#jmp)        | Uncoditional jump                    | 0x04   |
| [JZ](#jz)          | Jump if Z flag is set                | 0x05   |
| [JNZ](#jnz)        | Jump if not Z                        | 0x06   |
| [JMC](#jmc)        | Jump if C                            | 0x07   |
| [JMS](#jms)        | Jump if S                            | 0x08   |
| [CALL](#call)      | Save PC to stack and jump            | 0x09   |
| [RET](#ret)        | Retrieve PC from stack               | 0x0A   |

## Memory

| Mnemonic           | Instruction                          | Opcode |
|--------------------|--------------------------------------|--------|
| [MOVR](#movi)      | Copy word from src to dst            | 0x10   |
| [MOVI](#movi)      | -                                    | 0x11   |
| [STOR](#stor)      | Store word to memory                 | 0x12   |
| [LOAD](#load)      | Loads word from memory to dst        | 0x15   |
| [PUSH](#push)      | Pushes word to stack                 | 0x17   |
| [POP](#pop)        | Pops word from stack                 | 0x18   |
| [STORB](#stor)     | Stores byte from src in memory       | 0x19   |
| [LOADB](#load)     | Loads byte from memory to dst        | 0x1B   |

## Arithmetics

| Mnemonic           | Instruction                          | Opcode |
|--------------------|--------------------------------------|--------|
| [ADDR](#addri)     | Adds src to dst                      | 0x20   |
| [ADDI](#addri)     | -                                    | 0x21   |
| [SUBR](#subri)     | Subs src from dst                    | 0x22   |
| [SUBI](#subri)     | -                                    | 0x23   |
| [INC](#inc)        | Increments by 1                      | 0x24   |
| [DEC](#dec)        | Decrements by 1                      | 0x25   |
| [MULR](#mul)       | Multiplies R by R                    | 0x26   |
| [MULI](#mul)       | Multiplies R by I                    | 0x27   |
| [DIVR](#div)       | Divides R by R                       | 0x28   |
| [DIVI](#div)       | Divides R by   I                     | 0x29   |

## Bit ops

| Mnemonic           | Instruction                          | Opcode |
|--------------------|--------------------------------------|--------|
| [ANDR](#and)       | Bitwise AND                          | 0x30   |
| [ANDI](#and)       | -                                    | 0x31   |
| [ORR](#or)         | Bitwise OR                           | 0x32   |
| [ORI](#or)         | -                                    | 0x33   |
| [XORR](#xor)       | Bitwise XOR                          | 0x34   |
| [XORI](#xor)       | -                                    | 0x35   |
| [NOT](#not)        | Bitwise NOT                          | 0x36   |
| [SHR](#shr)        | Shift right                          | 0x37   |
| [SHL](#shr)        | Shift left                           | 0x38   |

## SP and BP ops

| Mnemonic           | Instruction                          | Opcode |
|--------------------|--------------------------------------|--------|
| [SETSP](#setsp)    | Set SP                               | 0x30   |
| [GETSP](#getsp)    | Get SP value                         | 0x31   |
| [ADDSP](#addsp)    | Add SP                               | 0x32   |
| [SUBSP](#subsp)    | Substract SP                         | 0x33   |
| [SETBP](#setbp)    | Set BP                               | 0x34   |
| [GETBP](#getbp)    | Get BP value                         | 0x35   |
| [ADDBP](#addbp)    | Add BP                               | 0x36   |
| [SUBBP](#subbp)    | Substract BP                         | 0x37   |

## NOP

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

## HLT

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

## CMPR

CMPR reg1, reg2

**Description:**

Compare 2 registers and set flags.

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

## CMPI

CMPI reg1, imm

**Description:**

Compare register with immediate value and set flags.

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

CMPR R0, 10