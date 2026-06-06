; This program repeats a string
; It tests input and RAM
.DEF RX_ADDR 0xF800
.DEF TX_ADDR 0xF801
.DEF HEAP_ADDR 0x4000

JMP start
msg1:
.STR "Enter a string: "
msg2:
.STR "You entered: "

start:
MOV R0, msg1

; output first message
msg_loop_1:
LOADB R1, [R0]
STORB R1, [TX_ADDR]
INC R0
CMP R0, msg2
JNZ msg_loop_1

; input string
MOV R0, HEAP_ADDR
input_loop:
LOADB R1, [RX_ADDR]
STORB R1, [R0]
INC R0
CMP R1, 10 ; zero-terminated
JNZ input_loop

; output second message
MOV R0, msg2
msg_loop_2:
LOADB R1, [R0]
STORB R1, [TX_ADDR]
INC R0
CMP R0, start
JNZ msg_loop_2

; output string
MOV R0, HEAP_ADDR
output_loop:
LOADB R1, [R0]
STORB R1, [TX_ADDR]
INC R0
CMP R1, 10 ; zero-terminated
JNZ output_loop

HLT