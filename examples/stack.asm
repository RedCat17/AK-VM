; This program tests stack, PUSH and POP opcodes.

.DEF OUT_ADDRESS 0xF801

MOVRI R0, 79
PUSHR R0
MOVRI R0, 76
PUSHR R0
MOVRI R0, 76
PUSHR R0
MOVRI R0, 69
PUSHR R0
MOVRI R0, 72
PUSHR R0

MOVRI R0, 0

loop:
POPR R1 ; pop byte from stack to reg 1
STORBDR R1, OUT_ADDRESS ; send byte to TX address
INCR R0 ; increment pointer
CMPRI R0, 5 ; test if we reached end of string
JNZ loop

HLT