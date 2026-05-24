; This program repeats a string
; It tests macros, input and RAM
.DEF HEAP_ADDRESS 0x4000
.DEF OUT_ADDRESS 0xF801

JMP start
msg1:
.STR "Enter a string: "
msg2:
.STR "You entered: "

start:
MOVRI R0, msg1

msg_loop_1:
LOADBRM R1, R0
STORBDR R1, OUT_ADDRESS
INCR R0
CMPRI R0, msg2
JNZ msg_loop_1

MOVRI R0, HEAP_ADDRESS
input_loop:
LOADBRD R1, 0xF800
STORBMR R0, R1
INCR R0
CMPRI R1, 10
JNZ input_loop

MOVRI R0, msg2
msg_loop_2:
LOADBRM R1, R0
STORBDR R1, OUT_ADDRESS
INCR R0
CMPRI R0, start
JNZ msg_loop_2

MOVRI R0, HEAP_ADDRESS
output_loop:
LOADBRM R1, R0
STORBDR R1, OUT_ADDRESS
INCR R0
CMPRI R1, 10
JNZ output_loop

HLT