; This program repeats a string
; It tests input and RAM
JMP start
msg1:
.STR "Enter a string: "
msg2:
.STR "You entered: "

start:
MOV R0, msg1

msg_loop_1:
LOADB R1, [R0]
STORB R1, [0xF801]
INC R0
CMP R0, msg2
JNZ msg_loop_1

MOV R0, 0x4000
input_loop:
LOADB R1, [0xF800]
STORB R0, [R1]
INC R0
CMP R1, 10
JNZ input_loop

MOV R0, msg2
msg_loop_2:
LOADB R1, [R0]
STORB R1, [0xF801]
INC R0
CMP R0, start
JNZ msg_loop_2

MOV R0, 0x4000
output_loop:
LOADB R1, [R0]
STORB R1, [0xF801]
INC R0
CMP R1, 10
JNZ output_loop

HLT