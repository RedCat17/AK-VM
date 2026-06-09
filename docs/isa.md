# ISA

## Features

- 16 general purpose 16-bit registers
- PC, SP, flags (Z, C, S) registers
- 64 KB flat byte-addressable memory
- Stack (grows downwards)
- Variable-length instructions (1, 2, 4-byte)
- Functions (via CALL, args passed via stack or registers)
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
| [STORDR](#stordr)  | Store word to memory                 | 0x12   |
| [STORMI](#stormi)  | Store word to memory                 | 0x13   |
| [STORMR](#stormt)  | Store word to memory                 | 0x14   |
| [LOADRD](#loadrd)  | Load word from memory                | 0x15   |
| [LOADRM](#loadrm)  | Load word from memory                | 0x16   |
| [PUSH](#push)      | Push word to stack                   | 0x17   |
| [POP](#pop)        | Pop word from stack                  | 0x18   |
| [STORBDR](#storbdr)| Store byte to memory                 | 0x19   |
| [STORBMI](#storbmi)| Store byte to memory                 | 0x1A   |
| [STORBMR](#storbmr)| Store byte to memory                 | 0x1B   |
| [LOADBRD](#loadbrd)| Loads byte from memory               | 0x1C   |
| [LOADBRM](#loadbrd)| Loads byte from memory               | 0x1D   |

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

### Bit Operations

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

### Control flow

#### NOP

**Description:** No operation. Does nothing.

**Encoding:**
```
byte1: 0x00
```

**Operands:** None

**Flags affected:** None

**Example:** `NOP`

---

#### HLT

**Description:** Stop execution, halt VM.

**Encoding:**
```
byte1: 0x01
```

**Operands:** None

**Flags affected:** None

**Example:** `HLT`

---

#### CMPR

CMPR reg1, reg2

**Description:** Compare 2 registers and set flags.

**Operation:** `Z ← (reg1 - reg2 == 0), S ← (reg1 - reg2) & 0x8000, C ← (reg < reg2)`

**Encoding:**
```
byte1: 0x02
byte2: reg1 | reg2
```

**Operands:** reg1, reg2

**Flags affected:** Z, C, S

**Example:** `CMPR R0, R1`

---

#### CMPI

CMPI reg1, imm

**Description:** Compare register with immediate value and set flags.

**Operation:** `Z ← (reg1 - reg2 == 0), S ← (reg1 - reg2) & 0x8000, C ← (reg < reg2)`

**Encoding:**
```
byte1: 0x03
byte2: reg1 | 0000
byte3, byte4: imm
```

**Operands:** reg1, imm

**Flags affected:** Z, C, S

**Example:** `CMPI R0, 10`

---

#### JMP

JMP imm

**Description:** Uncoditional jump to address. Sets PC to imm.

**Operation:** `PC ← imm`

**Encoding:**
```
byte1: 0x04
byte2, byte3: imm
```

**Operands:** imm

**Flags affected:** None

**Example:** `JMP label`

---

#### JZ

JZ imm

**Description:** Jump to address if Zero flag is set. Sets PC to imm.

**Operation:** `PC ← imm if Z`

**Encoding:**
```
byte1: 0x05
byte2, byte3: imm
```

**Operands:** imm

**Flags affected:** None

**Example:** `JZ label`

---

#### JNZ

JNZ imm

**Description:** Jump to address if Zero flag is not set. Sets PC to imm.

**Operation:** `PC ← imm if !Z`

**Encoding:**
```
byte1: 0x06
byte2, byte3: imm
```

**Operands:** imm

**Flags affected:** None

**Example:** `JNZ label`

---

#### JC

JC imm

**Description:**

Jump to address if Carry flag is set. Sets PC to imm.

**Operation:** `PC ← imm if C`


**Encoding:**
```
byte1: 0x07
byte2, byte3: imm
```

**Operands:** imm

**Flags affected:** None

**Example:** `JC label`

---

#### JS

JS imm

**Description:** Jump to address if Sign flag is set. Sets PC to imm.

**Operation:** `PC ← imm if S`

**Encoding:**
```
byte1: 0x08
byte2, byte3: imm
```

**Operands:** imm

**Flags affected:** None

**Example:** `JS label`

---

#### CALL

CALL imm

**Description:** Call function. Jump to address and push PC to stack.

**Operation:** `push PC, PC ← imm`

**Encoding:**
```
byte1: 0x09
byte2, byte3: imm
```

**Operands:** imm

**Flags affected:** None

**Example:** `CALL label`

---

#### RET

RET

**Description:** Return from function. Pop PC from stack.

**Operation:** `pop PC`

**Encoding:**
```
byte1: 0x0A
```

**Flags affected:** None

**Example:** `RET`

---

### Memory

#### MOVR

**Description:** Copy word from source register to destination register.

**Operation:** `dst ← src`

**Encoding:**
```
byte1: 0x10
byte2: dst (4 bits) | src (4 bits)
```

**Flags affected:** None

**Example:** `MOVR R1, R0`

---

#### MOVI

**Description:** Move immediate word value to destination register.

**Operation:** `dst ← imm`

**Encoding:**
```
byte1: 0x11
byte2: dst (4 bits) | 0 (4 bits)
byte3: imm (low byte)
byte4: imm (high byte)
```

**Flags affected:** None

**Example:** `MOVI R2, 0x1234`

---

#### STORDR

**Description:** Store word from source register to immediate memory address.

**Operation:** `src -> mem[base]`

**Encoding:**
```
byte1: 0x12
byte2: src (4 bits) | 0 (4 bits)
byte3: imm
byte4: imm
```

**Flags affected:** None

**Example:** `STORDR R3, 0xF801`

---

#### STORMI

**Description:** Store word from immediate to memory address in base register.

**Operation:** `src -> mem[base]`

**Encoding:**
```
byte1: 0x13
byte2: src (4 bits) | 0 (4 bits)
byte3: imm
byte4: imm
```

**Flags affected:** None

**Example:** `STORMI 42, R1`

---

#### STORMR

**Description:** Store word from source register to memory address in base register.

**Operation:** `src -> mem[base]`

**Encoding:**
```
byte1: 0x14
byte2: src (4 bits) | base (4 bits)
```

**Flags affected:** None

**Example:** `STORMR R3, R1`

---

#### LOADRD

**Description:** Load word from immediate memory address to destination register.

**Operation:** `dst ← mem[base]`

**Encoding:**
```
byte1: 0x15
byte2: dst (4 bits) | 0 (4 bits)
byte3: imm
byte4: imm
```

**Flags affected:** None

**Example:** `LOADRD R2, 0xF800`

---

#### LOADRM

**Description:** Load word from memory address in base register to destination register.

**Operation:** `dst ← mem[base]`

**Encoding:**
```
byte1: 0x16
byte2: dst (4 bits) | base (4 bits)
```

**Flags affected:** None

**Example:** `LOADRM R2, R0`

---

#### PUSH

**Description:** Push word from register onto stack. Store, then decrement stack pointer by 2.

**Operation:** `mem[SP] ← src, SP ← SP - 2`

**Encoding:**
```
byte1: 0x17
byte2: src (4 bits) | 0 (4 bits)
```

**Flags affected:** None

**Example:** `PUSH R5`

---

#### POP

**Description:** Pop word from stack to register. Increment stack pointer by 2, then load from stack pointer.

**Operation:** `SP ← SP + 2, dst ← mem[SP]`

**Encoding:**
```
byte1: 0x18
byte2: dst (4 bits) | 0 (4 bits)
```

**Flags affected:** None

**Example:** `POP R6`

---

#### STORBDR

**Description:** Store byte from source register (lowest byte) to immediate memory address.

**Operation:** `src & 0xFF -> mem[base]`

**Encoding:**
```
byte1: 0x19
byte2: src (4 bits) | 0 (4 bits)
byte3: imm
byte4: imm
```

**Flags affected:** None

**Example:** `STORBDR R3, 0x13`

---

#### STORBMI

**Description:** Store byte from immediate to memory address in base register.

**Operation:** `src & 0xFF -> mem[base]`

**Encoding:**
```
byte1: 0x1A
byte2: src (4 bits) | 0 (4 bits)
byte3: imm
byte4: imm
```

**Flags affected:** None

**Example:** `STORBMI 42, R1`

---

#### STORBMR

**Description:** Store byte from source register (lowest byte) to memory address in base register.

**Operation:** `src & 0xFF -> mem[base]`

**Encoding:**
```
byte1: 0x1B
byte2: src (4 bits) | base (4 bits)
```

**Flags affected:** None

**Example:** `STORBMR R3, R1`

---

#### LOADBRD

**Description:** Load byte from immediate memory address to destination register (zero-extended).

**Operation:** `dst ← 0x00FF & mem[base]`

**Encoding:**
```
byte1: 0x1C
byte2: dst (4 bits) | 0 (4 bits)
byte3: imm
byte4: imm
```

**Flags affected:** None

**Example:** `LOADBRD R2, 0xF800`

---

#### LOADBRM

**Description:** Load byte from memory address in base register to destination register (zero-extended).

**Operation:** `dst ← 0x00FF & mem[base]`

**Encoding:**
```
byte1: 0x1D
byte2: dst (4 bits) | base (4 bits)
```

**Flags affected:** None

**Example:** `LOADBRM R2, R0`

---

### Arithmetics

#### ADDR

**Description:** Adds source register to destination register.

**Operation:** `dst ← dst + src`

**Encoding:**
```
byte1: 0x20
byte2: dst (4 bits) | src (4 bits)
```

**Flags affected:** Zero, Sign, Carry

**Example:** `ADDR R1, R0`

---

#### ADDI

**Description:** Add immediate value to destination register.

**Operation:** `dst ← dst + imm`

**Encoding:**
```
byte1: 0x21
byte2: dst (4 bits) | 0 (4 bits)
byte3: imm (low byte)
byte4: imm (high byte)
```

**Flags affected:** Zero, Sign, Carry

**Example:** `ADDI R2, 0x0010`

---

#### SUBR

**Description:** Subtract source register from destination register.

**Operation:** `dst ← dst - src`

**Encoding:**
```
byte1: 0x22
byte2: dst (4 bits) | src (4 bits)
```

**Flags affected:** Zero, Sign, Carry

**Example:** `SUBR R3, R1`

---

#### SUBI

**Description:** Subtract immediate value from destination register.

**Operation:** `dst ← dst - imm`

**Encoding:**
```
byte1: 0x23
byte2: dst (4 bits) | 0 (4 bits)
byte3: imm (low byte)
byte4: imm (high byte)
```

**Flags affected:** Zero, Sign, Carry

**Example:** `SUBI R4, 0x0005`

---

#### INC

**Description:** Increment destination register by 1.

**Operation:** `dst ← dst + 1`

**Encoding:**
```
byte1: 0x24
byte2: dst (4 bits) | 0 (4 bits)
```

**Flags affected:** Zero, Sign, Carry

**Example:** `INC R2`

---

#### DEC

**Description:** Decrement destination register by 1.

**Operation:** `dst ← dst - 1`

**Encoding:**
```
byte1: 0x25
byte2: dst (4 bits) | 0 (4 bits)
```

**Flags affected:** Zero, Sign, Carry

**Example:** `DEC R3`

---

#### MULR

**Description:** Multiply destination register by source register.

**Operation:** `dst ← dst × src`

**Encoding:**
```
byte1: 0x26
byte2: dst (4 bits) | src (4 bits)
```

**Flags affected:** Zero, Sign, Carry

**Example:** `MULR R1, R0`

---

#### MULI

**Description:** Multiply destination register by immediate value.

**Operation:** `dst ← dst × imm`

**Encoding:**
```
byte1: 0x27
byte2: dst (4 bits) | 0 (4 bits)
byte3: imm (low byte)
byte4: imm (high byte)
```

**Flags affected:** Zero, Sign, Carry

**Example:** `MULI R5, 0x0004`

---

#### DIVR

**Description:** Divide destination register by source register.

**Operation:** `dst ← dst ÷ src`

**Encoding:**
```
byte1: 0x28
byte2: dst (4 bits) | src (4 bits)
```

**Flags affected:** Zero, Sign, Carry

**Example:** `DIVR R2, R1`

---

#### DIVI

**Description:** Divide destination register by immediate value.

**Operation:** `dst ← dst ÷ imm`

**Encoding:**
```
byte1: 0x29
byte2: dst (4 bits) | 0 (4 bits)
byte3: imm (low byte)
byte4: imm (high byte)
```

**Flags affected:** Zero, Sign, Carry

**Example:** `DIVI R3, 0x0002`

---

### Bit ops

#### ANDR

**Description:** Bitwise AND between source and destination registers, result stored in destination.

**Operation:** `dst ← dst & src`

**Encoding:**
```
byte1: 0x30
byte2: dst (4 bits) | src (4 bits)
```

**Flags affected:** None

**Example:** `ANDR R1, R0`

---

#### ANDI

**Description:** Bitwise AND between destination register and immediate value, result stored in destination.

**Operation:** `dst ← dst & imm`

**Encoding:**
```
byte1: 0x31
byte2: dst (4 bits) | 0 (4 bits)
byte3: imm (low byte)
byte4: imm (high byte)
```

**Flags affected:** None

**Example:** `ANDI R2, 0x00FF`

---

#### ORR

**Description:** Bitwise OR between source and destination registers, result stored in destination.

**Operation:** `dst ← dst | src`

**Encoding:**
```
byte1: 0x32
byte2: dst (4 bits) | src (4 bits)
```

**Flags affected:** None

**Example:** `ORR R1, R0`

---

#### ORI

**Description:** Bitwise OR between destination register and immediate value, result stored in destination.

**Operation:** `dst ← dst | imm`

**Encoding:**
```
byte1: 0x33
byte2: dst (4 bits) | 0 (4 bits)
byte3: imm (low byte)
byte4: imm (high byte)
```

**Flags affected:** None

**Example:** `ORI R2, 0x8000`

---

#### XORR

**Description:** Bitwise XOR between source and destination registers, result stored in destination.

**Operation:** `dst ← dst ^ src`

**Encoding:**
```
byte1: 0x34
byte2: dst (4 bits) | src (4 bits)
```

**Flags affected:** None

**Example:** `XORR R1, R0`

---

#### XORI

**Description:** Bitwise XOR between destination register and immediate value, result stored in destination.

**Operation:** `dst ← dst ^ imm`

**Encoding:**
```
byte1: 0x35
byte2: dst (4 bits) | 0 (4 bits)
byte3: imm (low byte)
byte4: imm (high byte)
```

**Flags affected:** None

**Example:** `XORI R3, 0xFFFF`

---

#### NOT

**Description:** Bitwise NOT of register.

**Operation:** `dst ← ~dst`

**Encoding:**
```
byte1: 0x36
byte2: dst (4 bits) | 0 (4 bits)
```

**Flags affected:** None

**Example:** `NOT R1`

---

#### SHR

**Description:** Shift destination register right by 1 bit.

**Operation:** `dst ← dst >> 1`

**Encoding:**
```
byte1: 0x37
byte2: dst (4 bits) | 0 (4 bits)
```

**Flags affected:** None

**Example:** `SHR R1`

---

#### SHL

**Description:** Shift destination register left by 1 bit.

**Operation:** `dst ← dst << 1`

**Encoding:**
```
byte1: 0x38
byte2: dst (4 bits) | 0 (4 bits)
```

**Flags affected:** None

**Example:** `SHL R1`

---

### SP and BP ops

#### SETSP

**Description:** Set stack pointer from source register.

**Operation:** `SP ← src`

**Encoding:**
```
byte1: 0x40
byte2: src (4 bits) | 0 (4 bits)
```

**Flags affected:** None

**Example:** `SETSP R5`

---

#### GETSP

**Description:** Get stack pointer value into destination register.

**Operation:** `dst ← SP`

**Encoding:**
```
byte1: 0x41
byte2: dst (4 bits) | 0 (4 bits)
```

**Flags affected:** None

**Example:** `GETSP R2`

---

#### ADDSP

**Description:** Add immediate value to stack pointer.

**Operation:** `SP ← SP + imm`

**Encoding:**
```
byte1: 0x42
byte2: imm (low byte)
byte3: imm (high byte)
```

**Flags affected:** None

**Example:** `ADDSP 0x0004`

---

#### SUBSP

**Description:** Subtract immediate value from stack pointer.

**Operation:** `SP ← SP - imm`

**Encoding:**
```
byte1: 0x43
byte2: imm (low byte)
byte3: imm (high byte)
```

**Flags affected:** None

**Example:** `SUBSP 0x0002`

---

#### SETBP

**Description:** Set base pointer from source register.

**Operation:** `BP ← src`

**Encoding:**
```
byte1: 0x44
byte2: src (4 bits) | 0 (4 bits)
```

**Flags affected:** None

**Example:** `SETBP R5`

---

#### GETBP

**Description:** Get base pointer value into destination register.

**Operation:** `dst ← BP`

**Encoding:**
```
byte1: 0x45
byte2: dst (4 bits) | 0 (4 bits)
```

**Flags affected:** None

**Example:** `GETBP R2`

---

#### ADDBP

**Description:** Add immediate value to base pointer.

**Operation:** `BP ← BP + imm`

**Encoding:**
```
byte1: 0x46
byte2: imm (low byte)
byte3: imm (high byte)
```

**Flags affected:** None

**Example:** `ADDBP 0x0004`

---

#### SUBBP

**Description:** Subtract immediate value from base pointer.

**Operation:** `BP ← BP - imm`

**Encoding:**
```
byte1: 0x47
byte2: imm (low byte)
byte3: imm (high byte)
```

**Flags affected:** None

**Example:** `SUBBP 0x0002`