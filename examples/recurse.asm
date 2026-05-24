; This program tests functions, SP and BP. Arguments are passed via stack and referenced via BP offsets.

.DEF OUT_ADDRESS 0xF801
.DEF ASCII_0 48

JMP start

_sub: 
; prologue
MOVRBP R15
PUSHR R15 ; = PUSH BP

MOVRSP R15
MOVBPR R15 ; = MOV BP, SP
; now R15 = BP

; arg1
MOVRR R14, R15
ADDRI R14, 6
LOADRM R14, R14; = LOAD BP + 6

; actual function
MOVRR R13, R14

ADDRI R13, ASCII_0
STORBDR R13, OUT_ADDRESS

DECR R14
JMZ epilogue

PUSHR R14
CALL _sub
ADDSPI 2 ; fix stack

epilogue: 
; epilogue
MOVRBP R15
MOVSPR R15 ; = MOV SP, BP 

POPR R15
MOVBPR R15 ; = POP BP
RET

start:

; arg1 push
MOVRI R0, 7
PUSHR R0

CALL _sub
ADDSPI 2 ; fix stack 

HLT