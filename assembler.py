import argparse

class EncodingFormat:
    FORMAT_NONE = 0
    FORMAT_REG = 1
    FORMAT_REG_REG = 2
    FORMAT_IMM = 3
    FORMAT_REG_IMM = 4

FORMAT_LENGTHS = {
    EncodingFormat.FORMAT_NONE: 1,
    EncodingFormat.FORMAT_REG: 2,
    EncodingFormat.FORMAT_REG_REG: 2,
    EncodingFormat.FORMAT_IMM: 3,
    EncodingFormat.FORMAT_REG_IMM: 4
}

REG1 = 0b11110000
REG2 = 0b00001111

LOWER_BYTE  = 0x00FF
HIGHER_BYTE = 0xFF00

# Control flow
OPCODE_NOP     = 0x00
OPCODE_HLT     = 0x01
OPCODE_CMPRR   = 0x02
OPCODE_CMPRI   = 0x03
OPCODE_JMP     = 0x04
OPCODE_JMZ     = 0x05
OPCODE_JNZ     = 0x06
OPCODE_JMC     = 0x07
OPCODE_JMS     = 0x08
OPCODE_CALL    = 0x09
OPCODE_RET     = 0x0A

# Memory
OPCODE_MOVRR   = 0x10
OPCODE_MOVRI   = 0x11
OPCODE_STORDR  = 0x12
OPCODE_STORMI  = 0x13
OPCODE_STORMR  = 0x14
OPCODE_LOADRD  = 0x15
OPCODE_LOADRM  = 0x16
OPCODE_PUSHR   = 0x17
OPCODE_POPR    = 0x18
OPCODE_STORBDR = 0x19
OPCODE_STORBMI = 0x1A
OPCODE_STORBMR = 0x1B
OPCODE_LOADBRD = 0x1C
OPCODE_LOADBRM = 0x1D

# Arithmetics
OPCODE_ADDRR   = 0x20
OPCODE_ADDRI   = 0x21
OPCODE_SUBRR   = 0x22
OPCODE_SUBRI   = 0x23
OPCODE_INCR    = 0x24
OPCODE_DECR    = 0x25
OPCODE_MULRR   = 0x26
OPCODE_MULRI   = 0x27
OPCODE_DIVRR   = 0x28
OPCODE_DIVRI   = 0x29

# Bit ops
OPCODE_ANDRR   = 0x30
OPCODE_ANDRI   = 0x31
OPCODE_ORRR    = 0x32
OPCODE_ORRI    = 0x33
OPCODE_XORRR   = 0x34
OPCODE_XORRI   = 0x35
OPCODE_NOTR    = 0x36
OPCODE_SHRR    = 0x37
OPCODE_SHLR    = 0x38

opcode_table = {
    # Control flow
    'NOP': {'opcode': OPCODE_NOP,       
            'format': EncodingFormat.FORMAT_NONE},
    'HLT': {'opcode': OPCODE_HLT,       
            'format': EncodingFormat.FORMAT_NONE},
    'CMPRR': {'opcode': OPCODE_CMPRR,   
              'format': EncodingFormat.FORMAT_REG_REG},
    'CMPRI': {'opcode': OPCODE_CMPRI,   
              'format': EncodingFormat.FORMAT_REG_IMM},
    'JMP': {'opcode': OPCODE_JMP,       
            'format': EncodingFormat.FORMAT_IMM},
    'JMZ': {'opcode': OPCODE_JMZ,       
            'format': EncodingFormat.FORMAT_IMM},
    'JNZ': {'opcode': OPCODE_JNZ,       
            'format': EncodingFormat.FORMAT_IMM},
    'JMC': {'opcode': OPCODE_JMC,       
            'format': EncodingFormat.FORMAT_IMM},
    'JMS': {'opcode': OPCODE_JMS,       
            'format': EncodingFormat.FORMAT_IMM},
    'CALL': {'opcode': OPCODE_CALL,     
             'format': EncodingFormat.FORMAT_IMM},
    'RET': {'opcode': OPCODE_RET,       
            'format': EncodingFormat.FORMAT_NONE},
    
    # Memory 
    'MOVRR': {'opcode': OPCODE_MOVRR,   
              'format': EncodingFormat.FORMAT_REG_REG},
    'MOVRI': {'opcode': OPCODE_MOVRI,   
              'format': EncodingFormat.FORMAT_REG_IMM},
    'STORDR': {'opcode': OPCODE_STORDR, 
               'format': EncodingFormat.FORMAT_REG_IMM},
    'STORMI': {'opcode': OPCODE_STORMI, 
               'format': EncodingFormat.FORMAT_REG_IMM},
    'STORMR': {'opcode': OPCODE_STORMR, 
               'format': EncodingFormat.FORMAT_REG_REG},
    'LOADRD': {'opcode': OPCODE_LOADRD, 
               'format': EncodingFormat.FORMAT_REG_IMM},
    'LOADRM': {'opcode': OPCODE_LOADRM, 
               'format': EncodingFormat.FORMAT_REG_REG},
    'PUSHR': {'opcode': OPCODE_PUSHR,   
              'format': EncodingFormat.FORMAT_REG},
    'POPR': {'opcode': OPCODE_POPR,     
             'format': EncodingFormat.FORMAT_REG},
    'STORBDR': {'opcode': OPCODE_STORBDR, 
               'format': EncodingFormat.FORMAT_REG_IMM},
    'STORBMI': {'opcode': OPCODE_STORBMI, 
               'format': EncodingFormat.FORMAT_REG_IMM},
    'STORBMR': {'opcode': OPCODE_STORBMR, 
               'format': EncodingFormat.FORMAT_REG_REG},
    'LOADBRD': {'opcode': OPCODE_LOADBRD, 
               'format': EncodingFormat.FORMAT_REG_IMM},
    'LOADBRM': {'opcode': OPCODE_LOADBRM, 
               'format': EncodingFormat.FORMAT_REG_REG},
    
    # Arithmetics
    'ADDRR': {'opcode': OPCODE_ADDRR,   
              'format': EncodingFormat.FORMAT_REG_REG},
    'ADDRI': {'opcode': OPCODE_ADDRI,   
              'format': EncodingFormat.FORMAT_REG_IMM},
    'SUBRR': {'opcode': OPCODE_SUBRR,   
              'format': EncodingFormat.FORMAT_REG_REG},
    'SUBRI': {'opcode': OPCODE_SUBRI,   
              'format': EncodingFormat.FORMAT_REG_IMM},
    'INCR': {'opcode': OPCODE_INCR,     
             'format': EncodingFormat.FORMAT_REG},
    'DECR': {'opcode': OPCODE_DECR,     
             'format': EncodingFormat.FORMAT_REG},
    'MULRR': {'opcode': OPCODE_MULRR,   
              'format': EncodingFormat.FORMAT_REG_REG},
    'MULRI': {'opcode': OPCODE_MULRI,   
              'format': EncodingFormat.FORMAT_REG_IMM},
    'DIVRR': {'opcode': OPCODE_DIVRR,   
              'format': EncodingFormat.FORMAT_REG_REG},
    'DIVRI': {'opcode': OPCODE_DIVRI,   
              'format': EncodingFormat.FORMAT_REG_IMM},

    # Bit ops
    'ANDRR': {'opcode': OPCODE_ANDRR,   
              'format': EncodingFormat.FORMAT_REG_REG},
    'ANDRI': {'opcode': OPCODE_ANDRI,   
              'format': EncodingFormat.FORMAT_REG_IMM},
    'ORRR': {'opcode': OPCODE_ORRR,     
             'format': EncodingFormat.FORMAT_REG_REG},
    'ORRI': {'opcode': OPCODE_ORRI,     
             'format': EncodingFormat.FORMAT_REG_IMM},
    'XORRR': {'opcode': OPCODE_XORRR,   
              'format': EncodingFormat.FORMAT_REG_REG},
    'XORRI': {'opcode': OPCODE_XORRI,   
              'format': EncodingFormat.FORMAT_REG_IMM},
    'NOTR': {'opcode': OPCODE_NOTR,     
             'format': EncodingFormat.FORMAT_REG},
    'SHRR': {'opcode': OPCODE_SHRR,     
             'format': EncodingFormat.FORMAT_REG},
    'SHLR': {'opcode': OPCODE_SHLR,     
             'format': EncodingFormat.FORMAT_REG},
}

labels = {}
macros = {}

def parse_imm(value: str):
    # print(f"Parsing {value}")
    if value in labels:
        return labels[value]
    if value.startswith('0x'):
        return int(value, 16)
    if value.startswith('0b'):
        return int(value, 2)
    if value.startswith("'") and value.endswith("'"):
        return ord(value)
    try:
        return int(value, 10)
    except:
        raise ValueError("Invalid value!")
        
def main():
    parser = argparse.ArgumentParser(description='Assembler for AK-VM-1')

    parser.add_argument("input_file", help="Path to input source file")
    parser.add_argument("-o", "--output", help="Path to assembled output file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        lines = [line.strip() for line in file.readlines() if (line.strip() and not line.startswith(';'))]

    # label collecting
    cur_address = 0
    for line in lines:
        if line.endswith(':'):
            labels[line[:-1]] = cur_address
        else:
            instruction, *instr_args = line.split()
            if instruction in opcode_table:
                opcode = opcode_table[instruction]
                cur_address += FORMAT_LENGTHS[opcode['format']]
            elif instruction == '.DB':
                cur_address += len(instr_args)
            elif instruction == '.STR':
                cur_address += len(' '.join(instr_args).strip('"'))
            elif instruction == '.DEF':
                macros[instr_args[0]] = ' '.join(instr_args[1:])
            else:
                raise ValueError(f"Unknown instruction: {instruction}")
                break
    print(labels)
    print(macros)


    # actual assebmling
    cur_address = 0
    instruction_bits = bytearray([])
    for line in lines:
        print(line)
        line = line.strip()
        if line.startswith(';'): # comment
            continue
        tokens = line.split()                
        if not tokens:  # empty line
            continue
        new_tokens = []
        for token in tokens:
            if token in macros:
                new_tokens.append(macros[token])
            else:
                new_tokens.append(token)
        tokens = new_tokens  

        instruction, *instr_args = tokens
        instruction = instruction.upper()

        if instruction in opcode_table:
            opcode = opcode_table[instruction]
            instruction_bits.append(opcode['opcode'])
            match opcode['format']:
                case EncodingFormat.FORMAT_NONE:
                    if args.verbose: 
                        print(f"{hex(cur_address)}: {hex(opcode['opcode'])}")
                case EncodingFormat.FORMAT_REG:
                    reg_byte = parse_imm(instr_args[0]) << 4
                    instruction_bits.append(reg_byte)
                    if args.verbose: 
                        print(f"{hex(cur_address)}: {hex(opcode['opcode'])} {reg_byte}")
                case EncodingFormat.FORMAT_REG_REG:
                    reg_byte = parse_imm(instr_args[0]) << 4 | parse_imm(instr_args[1])
                    instruction_bits.append(reg_byte)
                    if args.verbose: 
                        print(f"{hex(cur_address)}: {hex(opcode['opcode'])} {reg_byte}")
                case EncodingFormat.FORMAT_IMM:
                    value = parse_imm(instr_args[0])
                    instruction_bits.append(value & LOWER_BYTE)
                    instruction_bits.append((value & HIGHER_BYTE) >> 8)
                    if args.verbose: 
                        print(f"{hex(cur_address)}: {hex(opcode['opcode'])} {value & LOWER_BYTE} {(value & HIGHER_BYTE) >> 8}")
                case EncodingFormat.FORMAT_REG_IMM:
                    reg_byte = parse_imm(instr_args[0]) << 4
                    instruction_bits.append(reg_byte)
                    value = parse_imm(instr_args[1])
                    instruction_bits.append(value & LOWER_BYTE)
                    instruction_bits.append((value & HIGHER_BYTE) >> 8)
                    if args.verbose: 
                        print(f"{hex(cur_address)}: {hex(opcode['opcode'])} {reg_byte} {value & LOWER_BYTE} {(value & HIGHER_BYTE) >> 8}")
                case _:
                    raise ValueError("Unknown encoding format!")
                    break
            cur_address += FORMAT_LENGTHS[opcode['format']]
        else: 
            match instruction:
                case '.DB':
                    for arg in instr_args:
                        byte = parse_imm(arg)
                        if args.verbose: 
                            print(f"{hex(cur_address)}: {byte}")
                        instruction_bits.append(byte)
                        cur_address += 1
                case '.STR':
                    string = ' '.join(instr_args).strip('"')
                    print(f"string: {string}")
                    for char in string:
                        byte = ord(char)
                        if args.verbose: 
                            print(f"{hex(cur_address)}: {byte}")
                        instruction_bits.append(byte)
                        cur_address += 1


            

    output_path = args.output or args.input_file + '.bin'
    with open(output_path, 'wb') as file:
        file.write(instruction_bits)

if __name__ == '__main__':
    main()