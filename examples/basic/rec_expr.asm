; This program should test recursive expressions

.DEF OUT_ADDRESS 0xF801

.DEF A 1
.DEF B A + 2
.DEF C A + B

MOVI R0, C + 2
ADDI R0, 48
STORBDR R0, OUT_ADDRESS 

HLT