; This program outputs "Hello world!" 
; It tests memory, I/O, loops, labels
JMP start
msg:
.STR "Hello world!"

start:
MOVRI R0, msg ; load msg address to reg 0

loop:
LOADBRM R1, R0 ; load byte from memory to reg 1
STORBDR R1, 0xF801 ; send byte to TX address
INCR R0 ; increment pointer
CMPRI R0, start ; test if we reached end of string
JNZ loop

HLT