; This program should test expressions
; should output 6

.DEF OUT_ADDRESS 0xF801

.DEF A 4

MOV R0, A + 2
ADD R0, 48
STORB R0, [OUT_ADDRESS]

HLT