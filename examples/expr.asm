; This program should test expressions
; should output 6

.DEF OUT_ADDRESS 0xF801

.DEF A 4

MOVRI 0, A + 2
ADDRI 0, 48
STORBDR 0, OUT_ADDRESS

HLT