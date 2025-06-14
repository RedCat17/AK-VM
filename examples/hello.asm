; This program outputs "Hello world!" 
; It tests memory, I/O, loops, labels
JMP start
msg:
.STR Hello world!

start:
MOVRI 0 msg ; load msg address to reg 0

loop:
LOADBRM 1 0 ; load byte from memory to reg 1
STORBDR 1 0xF801 ; send byte to TX address
INCR 0 ; increment pointer
CMPRI 0 start ; test if we reached end of string
JNZ loop

HLT