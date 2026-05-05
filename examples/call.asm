; This program tests functions. Arguments are passed via registers.

.DEF OUT_ADDRESS 0xF801
.DEF ASCII_0 48

JMP start
_add: 
ADDRR 15, 14
RET

start:
MOVRI 14, 2
MOVRI 15, 3
CALL _add

ADDRI 15, ASCII_0
STORBDR 15, OUT_ADDRESS 

HLT