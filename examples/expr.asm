; This program should test expressions
; should output 6

.DEF OUT_ADDRESS 0xF801

.DEF A 4

MOVI R0, A + 2
ADDI R0, 48
STORBDR R0, OUT_ADDRESS

HLT