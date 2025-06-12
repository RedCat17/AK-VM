program = [
    0x0C, # MOVRI
    0b00000000, 
    0x0F, 0x00, 
    0x0B, # MOVRR
    0b00010000,
    0x15, # ADDRI
    0b00010000,
    48, 0x00,
    0x0D, # STORDR
    0b00010000,
    0x01, 0xFF,
    0x19, # DECR
    0b00000000,
    0x06, # JNZ
    0x04, 0x00, 
    0x01 # HLT    
]

with open("program.bin", 'wb') as f:
    f.write(bytes(program))