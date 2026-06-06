; This program tests functions. Arguments are passed via registers.

.DEF OUT_ADDRESS 0xF801
.DEF ASCII_0 48

JMP start
_add: 
ADD R15, R14
RET

start:
MOV R14, 2
MOV R15, 3
CALL _add

ADD R15, ASCII_0
STOR R15, [OUT_ADDRESS] 

HLT