class EncodingFormat:
    FORMAT_NONE = 0
    FORMAT_REG = 1
    FORMAT_REG_REG = 2
    FORMAT_IMM = 3
    FORMAT_REG_IMM = 4

REG1 = 0b11110000
REG2 = 0b00001111

BYTE1 = 0x00FF
BYTE2 = 0xFF00

opcode_table = {
    # Control flow
    'NOP': {'opcode': 0x00,
            'format': EncodingFormat.FORMAT_NONE},
    'HLT': {'opcode': 0x01,
            'format': EncodingFormat.FORMAT_NONE},
    'CMPRR': {'opcode': 0x02,
            'format': EncodingFormat.FORMAT_REG_REG},
    'CMPRI': {'opcode': 0x03,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'JMP': {'opcode': 0x04,
            'format': EncodingFormat.FORMAT_IMM},
    'JMZ': {'opcode': 0x05,
            'format': EncodingFormat.FORMAT_IMM},
    'JNZ': {'opcode': 0x06,
            'format': EncodingFormat.FORMAT_IMM},
    'JMC': {'opcode': 0x07,
            'format': EncodingFormat.FORMAT_IMM},
    'JMS': {'opcode': 0x08,
            'format': EncodingFormat.FORMAT_IMM},
    'CALL': {'opcode': 0x09,
            'format': EncodingFormat.FORMAT_IMM},
    'RET': {'opcode': 0x0A,
            'format': EncodingFormat.FORMAT_NONE},
    # Memory
    'MOVRR': {'opcode': 0x0B,
            'format': EncodingFormat.FORMAT_REG_REG},
    'MOVRI': {'opcode': 0x0C,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'STORDR': {'opcode': 0x0D,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'STORMI': {'opcode': 0x0E,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'STORMR': {'opcode': 0x0F,
            'format': EncodingFormat.FORMAT_REG_REG},
    'LOADRD': {'opcode': 0x10,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'LOADRM': {'opcode': 0x11,
            'format': EncodingFormat.FORMAT_REG_REG},
    'PUSHR': {'opcode': 0x12,
            'format': EncodingFormat.FORMAT_REG},
    'POPR': {'opcode': 0x13,
            'format': EncodingFormat.FORMAT_REG},
    
    # Arithmetics
    'ADDRR': {'opcode': 0x14,
            'format': EncodingFormat.FORMAT_REG_REG},
    'ADDRI': {'opcode': 0x15,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'SUBRR': {'opcode': 0x16,
            'format': EncodingFormat.FORMAT_REG_REG},
    'SUBRI': {'opcode': 0x17,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'INCR': {'opcode': 0x18,
            'format': EncodingFormat.FORMAT_REG},
    'DECR': {'opcode': 0x19,
            'format': EncodingFormat.FORMAT_REG},
    'MULRR': {'opcode': 0x1A,
            'format': EncodingFormat.FORMAT_REG_REG},
    'MULRI': {'opcode': 0x1B,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'DIVRR': {'opcode': 0x1C,
            'format': EncodingFormat.FORMAT_REG_REG},
    'DIVRI': {'opcode': 0x1D,
            'format': EncodingFormat.FORMAT_REG_IMM},

    # Bit ops
    'ANDRR': {'opcode': 0x1E,
            'format': EncodingFormat.FORMAT_REG_REG},
    'ANDRI': {'opcode': 0x1F,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'ORRR': {'opcode': 0x20,
            'format': EncodingFormat.FORMAT_REG_REG},
    'ORRI': {'opcode': 0x21,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'XORRR': {'opcode': 0x22,
            'format': EncodingFormat.FORMAT_REG_REG},
    'XORRI': {'opcode': 0x23,
            'format': EncodingFormat.FORMAT_REG_IMM},
    'NOTR': {'opcode': 0x24,
            'format': EncodingFormat.FORMAT_REG},
    'SHRR': {'opcode': 0x25,
            'format': EncodingFormat.FORMAT_REG},
    'SHLR': {'opcode': 0x26,
            'format': EncodingFormat.FORMAT_REG},

}

with open("program.asm", 'r') as file:
    instruction_bits = bytearray([])
    for line in file:
        tokens = line.strip().split()
        if not tokens:  # empty line
            continue
        if line.startswith(';'): # comment
            continue
        
        opcode_name = tokens[0]
        print(opcode_name)
        opcode = opcode_table[opcode_name]
        print(opcode)
        instruction_bits.append(opcode['opcode'])
        match opcode['format']:
            case EncodingFormat.FORMAT_NONE:
                pass
            case EncodingFormat.FORMAT_REG:
                reg_byte = int(tokens[1]) << 4
                print(bin(reg_byte))
                instruction_bits.append(reg_byte)
            case EncodingFormat.FORMAT_REG_REG:
                reg_byte = int(tokens[1]) << 4 | int(tokens[2])
                print(bin(reg_byte))
                instruction_bits.append(reg_byte)
            case EncodingFormat.FORMAT_IMM:
                value = int(tokens[1])
                instruction_bits.append(value & BYTE1)
                instruction_bits.append((value & BYTE2) >> 8)
            case EncodingFormat.FORMAT_REG_IMM:
                reg_byte = int(tokens[1]) << 4
                print(bin(reg_byte))
                instruction_bits.append(reg_byte)
                value = int(tokens[2])
                instruction_bits.append(value & BYTE1)
                instruction_bits.append((value & BYTE2) >> 8)
            case _:
                print("Unknown encoding format!")
                break
            
            
            
    print(instruction_bits)

with open('program.bin', 'wb') as file:
    file.write(instruction_bits)