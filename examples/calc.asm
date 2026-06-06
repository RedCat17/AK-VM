; This is a calculator.
; It sums two numbers.
.DEF RX_ADDR 0xF800
.DEF TX_ADDR 0xF801
.DEF HEAP_ADDR 0x4000

JMP start

; ============================================================================================
; READ_STRING
; Arguments: R0 - write address
; Uses: R0-R2
; Operation: writes string to memory, R1 - string length, R0 - final address
; ============================================================================================
readStr: 
MOV R1, 0           ; string length
input_loop:
LOADB R2, [RX_ADDR]

CMP R2, 10 ; check for EoL
JZ _input_str_epilogue

STORB R2, [R0]
INC R0
INC R1
JMP input_loop

_input_str_epilogue:
MOV R2, 0
STORB R2, [R0] ; zero-termination
RET

; ============================================================================================
; PRINT_STRING
; Arguments: R0 - string address
; Uses: R0-R1
; Operation: prints string to console, zero-terminated
; ============================================================================================
printStr: 
LOADB R1, [R0]

CMP R1, 0 ; check for EoS
JZ _print_str_epilogue

STORB R1, [TX_ADDR]
INC R0
JMP printStr

_print_str_epilogue:
RET

; ============================================================================================
; NEW_LINE
; Uses: R15
; Operation: prints new line
; ============================================================================================
newLine: 

MOV R15, 10
STORB R15, [TX_ADDR]
RET

; ============================================================================================
; PARSE_NUMBER
; Arguments: R0 - string address, R1 - string length
; Uses: R0-R4
; Operation: R2 - number
; ============================================================================================
parseNumber: 
MOV R2, 0 ; clear output register

ADD R1, R0 
DEC R1 ; now R1 contains address of string end
MOV R3, 1 ; digit multiplier

parse_loop:
LOADB R4, [R1] ; load digit char
SUB R4, 48
MUL R4, R3 ; now R4 contains current digit (e.g. 800)
MUL R3, 10

ADD R2, R4 ; add current digit to number

CMP R1, R0 ; check for EoS
JZ _parse_number_epilogue

DEC R1
JMP parse_loop

_parse_number_epilogue:
RET

; ============================================================================================
; PRINT_NUMBER
; Arguments: R0 - number
; Uses: R0-R3
; Operation: prints number to console
; ============================================================================================
printNumber: 
MOV R3, 0  ; digits

print_number_loop:
MOV R1, R0
MOV R2, R0

DIV R1, 10
MUL R1, 10
SUB R2, R1 ; now R2 contains a % 10

ADD R2, 48 ; convert to char
PUSH R2 
INC R3

DIV R0, 10 ; reduce number by 1 digit

CMP R0, 0 ; while number > 0
JNZ print_number_loop

print_digits_loop:
CMP R3, 0
JZ _print_number_epilogue

POP R2
STORB R2, [TX_ADDR]
DEC R3
JMP print_digits_loop

_print_number_epilogue:
RET

; ============================================================================================
start:

; enter first number
MOV R0, HEAP_ADDR   ; address to save input
CALL readStr

MOV R0, HEAP_ADDR   ; address of string
CALL parseNumber

MOV R5, R2 ; store number in R5 so it won't get corrupted

; enter second number
MOV R0, HEAP_ADDR   ; address to save input
CALL readStr

MOV R0, HEAP_ADDR   ; address of string
CALL parseNumber

; calculate sum
ADD R5, R2 

; output result
MOV R0, R5
CALL printNumber

HLT