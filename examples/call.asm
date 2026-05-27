; This program tests functions. Arguments are passed via registers.

.DEF OUT_ADDRESS 0xF801
.DEF ASCII_0 48

JMP start
_add: 
ADDR 15, 14
RET

start:
MOVI 14, 2
MOVI 15, 3
CALL _add

ADDI 15, ASCII_0
STORBDR 15, OUT_ADDRESS 

HLT