.DEF HEAP_ADDRESS 0x4000
.DEF OUT_ADDRESS 0xF801

; set reg 0 to 16
MOV R0, 16

; decrementing loop to print characters
MOV R1, R0
ADD R1, 48
STOR R1, [OUT_ADDRESS]
DEC R0
JNZ 4

HLT