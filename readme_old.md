### Memory Model
- pc: program counter
- sp: stack pointer
- fp: frame pointer
- flags: logic flags (zero, carry, etc.)
- reg[8]: registers
- stack[128]: stack
- memory[1024]: heap / general-purpose memory

### Instructions
#### Basic
- hlt: halt / stop execution
- dump: dumps current VM state
- lbl name: label at current line

#### Registers and Arithmetics
- set reg val: assign value
- add reg reg: reg1 += reg2
- sub reg reg: reg1 -= reg2 

#### Memory
- load reg adr: load value from memory address to register 
- loadi reg reg: load value from indirect memory address in reg2 to reg1 
- store adr reg: store value to memory address from register
- storei reg reg: store value to indirect memory address in reg1 from reg2

#### Stack
- push reg: push value from register to stack
- pop reg: pop value from stack to register

#### I/O
- out reg: print value from register to console converted to char
- print reg: print value from register to console
- input reg: input value from keyboard to register 

#### Control flow
- jmp lbl: jumps (sets PC) to label
- jmpr reg: jumps (sets PC) to register value
- cmp reg reg: sets FLAGS register to True if equal
- jmpz lbl: jumps (sets PC) to label if FLAGS == True
- jmpzr reg: jumps (sets PC) to register value if FLAGS == True
