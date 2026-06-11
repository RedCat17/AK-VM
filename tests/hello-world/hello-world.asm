; This program outputs "Hello world!" 
; It tests memory, I/O, loops, labels
JMP start

msg: .STR "Hello world!"

start:
    MOV R0, msg         ; load msg address to reg R0

loop:
    LOADB R1, [R0]      ; load byte from memory to R1
    CMP R1, 0           ; check for null terminator
    JZ done

    STORB R1, [0xF801]  ; send byte to TX address
    INC R0              ; increment pointer
    JMP loop

done:
    HLT                 ; stop execution