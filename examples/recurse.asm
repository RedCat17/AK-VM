; This program tests functions, SP and BP. Arguments are passed via stack and referenced via BP offsets.

.DEF OUT_ADDRESS 0xF801
.DEF ASCII_0 48

JMP start

_sub: 
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

; actual function
MOVRR 13, 14

ADDRI 13, ASCII_0
STORBDR 13, OUT_ADDRESS

DECR 14
JMZ epilogue

PUSHR 14
CALL _sub
ADDSPI 2 ; fix stack

epilogue: 
; epilogue
MOVRBP 15
MOVSPR 15 ; = MOV SP, BP 

POPR 15
MOVBPR 15 ; = POP BP
RET

start:

; arg1 push
MOVRI 0, 7
PUSHR 0

CALL _sub
ADDSPI 2 ; fix stack 

HLT