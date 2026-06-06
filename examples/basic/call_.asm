; This program tests functions, SP and BP. Arguments are passed via stack and references via BP offsets.

.DEF OUT_ADDRESS 0xF801
.DEF ASCII_0 48

JMP start

_add: 
; prologue
GETBP 15
PUSH 15 ; = PUSH BP

GETSP 15
SETBP 15 ; = MOV BP, SP
; now R15 = BP

; arg1
MOVR 14, 15
ADDI 14, 6
LOADRM 14, 14; = LOAD BP + 6

; arg2
MOVR 13, 15
ADDI 13, 8
LOADRM 13, 13; = LOAD BP + 8

; actual function
MOVR 0, 14
ADDR 0, 13

; epilogue
GETBP 15
SETSP 15 ; = MOV SP, BP 

POP 15
SETBP 15 ; = POP BP
RET

start:

; arg1 push
MOVI 0, 2
PUSH 0

; arg2 push
MOVI 0, 3
PUSH 0

CALL _sub
ADDSP 4 ; fix stack

ADDI 0, ASCII_0
STORBDR 0, OUT_ADDRESS 

HLT