; This program outputs "Hello world!" 
; It tests memory, I/O, loops, labels
JMP start
.STR Hello world!

start:
MOVRI 0 3

loop:
LOADBRM 1 0
STORBDR 1 0xFF01
INCR 0
CMPRI 0 start
JNZ loop

HLT