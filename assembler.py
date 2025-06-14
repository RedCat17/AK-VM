import argparse

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

def parse_imm(value: str):
    if value.startswith('0x'):
        return int(value, 16)
    elif value.startswith('0b'):
        return int(value, 2)
    else:
        try:
            return int(value, 10)
        except:
            try:
                return ord(value)
            except:
                raise ValueError("Invalid value!")
        
def main():
    parser = argparse.ArgumentParser(description='Assembler for AK-VM-1')

    parser.add_argument("input_file", help="Path to input source file")
    parser.add_argument("-o", "--output", help="Path to assembled output file")

    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        instruction_bits = bytearray([])
        for line in file:
            line = line.strip().upper()
            if line.startswith(';'): # comment
                continue
            tokens = line.split()
            if not tokens:  # empty line
                continue

            instruction, *instr_args = tokens

            if instruction in opcode_table:
                opcode = opcode_table[instruction]
                instruction_bits.append(opcode['opcode'])
                match opcode['format']:
                    case EncodingFormat.FORMAT_NONE:
                        pass
                    case EncodingFormat.FORMAT_REG:
                        reg_byte = parse_imm(instr_args[0]) << 4
                        instruction_bits.append(reg_byte)
                    case EncodingFormat.FORMAT_REG_REG:
                        reg_byte = parse_imm(instr_args[0]) << 4 | parse_imm(instr_args[1])
                        instruction_bits.append(reg_byte)
                    case EncodingFormat.FORMAT_IMM:
                        value = parse_imm(instr_args[0])
                        instruction_bits.append(value & BYTE1)
                        instruction_bits.append((value & BYTE2) >> 8)
                    case EncodingFormat.FORMAT_REG_IMM:
                        reg_byte = parse_imm(instr_args[0]) << 4
                        instruction_bits.append(reg_byte)
                        value = parse_imm(instr_args[1])
                        instruction_bits.append(value & BYTE1)
                        instruction_bits.append((value & BYTE2) >> 8)
                    case _:
                        raise ValueError("Unknown encoding format!")
                        break
            else: 
                match instruction:
                    case '. DB':
                        for arg in instr_args:
                            instruction_bits.append(parse_imm(arg))


            

    output_path = args.output or args.input_file + '.bin'
    with open(output_path, 'wb') as file:
        file.write(instruction_bits)

if __name__ == '__main__':
    main()