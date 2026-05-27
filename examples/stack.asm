; This program tests stack, PUSH and POP opcodes.

.DEF OUT_ADDRESS 0xF801

MOVI R0, 79
PUSH R0
MOVI R0, 76
PUSH R0
MOVI R0, 76
PUSH R0
MOVI R0, 69
PUSH R0
MOVI R0, 72
PUSH R0

MOVI R0, 0

loop:
POP R1 ; pop byte from stack to reg 1
STORBDR R1, OUT_ADDRESS ; send byte to TX address
INC R0 ; increment pointer
CMPI R0, 5 ; test if we reached end of string
JNZ loop

HLT