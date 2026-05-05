; This program tests functions, SP and BP. Arguments are passed via stack and references via BP offsets.

.DEF OUT_ADDRESS 0xF801
.DEF ASCII_0 48

JMP start

_add: 
; prologue
MOVRBP 15
PUSHR 15 ; = PUSH BP

MOVRSP 15
MOVBPR 15 ; = MOV BP, SP
; now R15 = BP

; arg1
MOVRR 14, 15
ADDRI 14, 6
LOADRM 14, 14; = LOAD BP + 6

; arg2
MOVRR 13, 15
ADDRI 13, 8
LOADRM 13, 13; = LOAD BP + 8

; actual function
MOVRR 0, 14
ADDRR 0, 13

; epilogue
MOVRBP 15
MOVSPR 15 ; = MOV SP, BP 

POPR 15
MOVBPR 15 ; = POP BP
RET

start:

; arg1 push
MOVRI 0, 2
PUSHR 0

; arg2 push
MOVRI 0, 3
PUSHR 0

CALL _sub
ADDSPI 4 ; fix stack

ADDRI 0, ASCII_0
STORBDR 0, OUT_ADDRESS 

HLT