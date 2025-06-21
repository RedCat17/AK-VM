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
MOVRI 0 msg1

msg_loop_1:
LOADBRM 1 0
STORBDR 1 OUT_ADDRESS
INCR 0
CMPRI 0 msg2
JNZ msg_loop_1

MOVRI 0 HEAP_ADDRESS
input_loop:
LOADBRD 1 0xF800
STORBMR 0 1
INCR 0
CMPRI 1 10
JNZ input_loop

MOVRI 0 msg2
msg_loop_2:
LOADBRM 1 0
STORBDR 1 OUT_ADDRESS
INCR 0
CMPRI 0 start
JNZ msg_loop_2

MOVRI 0 HEAP_ADDRESS
output_loop:
LOADBRM 1 0
STORBDR 1 OUT_ADDRESS
INCR 0
CMPRI 1 10
JNZ output_loop

HLT