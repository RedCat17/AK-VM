; This program repeats a string
; It tests input and RAM
JMP start
msg1:
.STR "Enter a string: "
msg2:
.STR "You entered: "

start:
MOVRI 0 msg1

msg_loop_1:
LOADBRM 1 0
STORBDR 1 0xFF01
INCR 0
CMPRI 0 msg2
JNZ msg_loop_1

MOVRI 0 0x4000
input_loop:
LOADBRD 1 0xFF00
STORBMR 0 1
INCR 0
CMPRI 1 10
JNZ input_loop

MOVRI 0 msg2
msg_loop_2:
LOADBRM 1 0
STORBDR 1 0xFF01
INCR 0
CMPRI 0 start
JNZ msg_loop_2

MOVRI 0 0x4000
output_loop:
LOADBRM 1 0
STORBDR 1 0xFF01
INCR 0
CMPRI 1 10
JNZ output_loop

HLT