; This program tests stack, PUSH and POP opcodes.

.DEF OUT_ADDRESS 0xF801

MOVRI 0, 79
PUSHR 0
MOVRI 0, 76
PUSHR 0
MOVRI 0, 76
PUSHR 0
MOVRI 0, 69
PUSHR 0
MOVRI 0, 72
PUSHR 0

MOVRI 0, 0

loop:
POPR 1 ; pop byte from stack to reg 1
STORBDR 1, OUT_ADDRESS ; send byte to TX address
INCR 0 ; increment pointer
CMPRI 0, 5 ; test if we reached end of string
JNZ loop

HLT