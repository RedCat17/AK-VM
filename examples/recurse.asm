; This program tests functions, SP and BP. Arguments are passed via stack and referenced via BP offsets.

.DEF OUT_ADDRESS 0xF801
.DEF ASCII_0 48

JMP start

_sub: 
; prologue
GETBP R15
PUSH R15 ; = PUSH BP

GETSP R15
SETBP R15 ; = MOV BP, SP
; now R15 = BP

; arg1
MOVR R14, R15
ADDI R14, 6
LOADRM R14, R14; = LOAD BP + 6

; actual function
MOVR R13, R14

ADDI R13, ASCII_0
STORBDR R13, OUT_ADDRESS

DEC R14
JZ epilogue

PUSH R14
CALL _sub
ADDSP 2 ; fix stack

epilogue: 
; epilogue
GETBP R15
SETSP R15 ; = MOV SP, BP 

POP R15
SETBP R15 ; = POP BP
RET

start:

; arg1 push
MOVI R0, 7
PUSH R0

CALL _sub
ADDSP 2 ; fix stack 

HLT