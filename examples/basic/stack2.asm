; This program tests stack, PUSH and POP opcodes.

.DEF HEAP_ADDR 0x4000

MOV R0, 1
PUSH R0
MOV R0, 50
PUSH R0
MOV R0, 100
PUSH R0
MOV R0, 500
PUSH R0
MOV R0, 1000
PUSH R0

MOV R0, 0

loop:
POP R1 ; pop byte from stack to reg 1
MOV R2, HEAP_ADDR
ADD R2, R0
ADD R2, R0
STOR R1, [R2] 
INC R0 ; increment pointer
CMP R0, 5 ; test if we reached end of string
JNZ loop

HLT