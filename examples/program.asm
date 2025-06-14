; set reg 0 to 16
MOVRI 0 16

; decrementing loop to print characters
MOVRR 1 0
ADDRI 1 48
STORDR 1 65281
DECR 0
JNZ 4

HLT