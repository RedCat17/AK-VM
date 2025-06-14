; This program outputs "Helloworld!" 
; It tests memory, I/O, loops, labels
JMP start
.DB H e l l o 32 w o r l d !

start:
MOVRI 0 3

loop:
LOADBRM 1 0
STORBDR 1 0xFF01
INCR 0
CMPRI 0 start
JNZ loop