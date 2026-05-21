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

# SP and BP ops
OPCODE_MOVSPR  = 0x40
OPCODE_MOVRSP  = 0x41
OPCODE_ADDSPI  = 0x42
OPCODE_SUBSPI  = 0x43
OPCODE_MOVBPR  = 0x44
OPCODE_MOVRBP  = 0x45
OPCODE_ADDBPI  = 0x46
OPCODE_SUBBPI  = 0x47

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

    # SP and BP ops
    'MOVSPR': {'opcode': OPCODE_MOVSPR,   
            'format': EncodingFormat.FORMAT_REG},
    'MOVRSP': {'opcode': OPCODE_MOVRSP,   
            'format': EncodingFormat.FORMAT_REG},
    'ADDSPI': {'opcode': OPCODE_ADDSPI,   
            'format': EncodingFormat.FORMAT_IMM},
    'SUBSPI': {'opcode': OPCODE_SUBSPI,   
            'format': EncodingFormat.FORMAT_IMM},
    'MOVBPR': {'opcode': OPCODE_MOVBPR,   
            'format': EncodingFormat.FORMAT_REG},
    'MOVRBP': {'opcode': OPCODE_MOVRBP,   
            'format': EncodingFormat.FORMAT_REG},
    'ADDBPI': {'opcode': OPCODE_ADDBPI,   
            'format': EncodingFormat.FORMAT_IMM},
    'SUBBPI': {'opcode': OPCODE_SUBBPI,   
            'format': EncodingFormat.FORMAT_IMM},
}

class TokenTypes:
    NUMBER = 0
    IDENT = 1
    OP = 2
    STRING = 3
# Token format: (TYPE, VALUE)

SINGLE_CHAR_OPERATORS = ['+', '-', '*', '/', '(', ')', '&', '|', '^', '!', '>', '<']
DOUBLE_CHAR_OPERATORS = ['<<', '>>', '==', '!=', '>=', '<=']

OPERATOR_PRIORITIES = { # higher = lower priority
    '!': 0,
    '*': 1,
    '/': 1,
    '+': 2,
    '-': 2,
    '<<': 3,
    '>>': 3,
    '^': 4,
    '>': 5,
    '<': 5,
    '>=': 5,
    '<=': 5,
    '==': 6,
    '!=': 6,
    '&': 7,
    '|': 7,
}

UNARY_OPERATORS = ['!', '-', '+']

def verify_ident(value: str):
    if value[0].isnumeric():
        raise ValueError(f'Ident cant begin with number: {value}')
    for char in value:
        if not (char.isalnum() or char == '_'):
            raise ValueError(f'Illegal characters in ident: {value}')

def verify_number(value: str):
    if value.startswith(('0x', '0b')):
        value = value[2:]
    elif not value.isdigit():
        raise ValueError(f'Invalid number: {value}')

def tokenize_expr(string: str):
    def flush_token():
        if i > last_i:
            token = string[last_i:i]
            if token[0].isdigit():
                verify_number(token)
                tokens.append((TokenTypes.NUMBER, token))
            else:
                verify_ident(token)
                tokens.append((TokenTypes.IDENT, token))
    tokens = []
    last_i = 0
    i = 0
    while i < len(string):
        if string[i].isspace():
            flush_token()
            i += 1
            last_i = i
            continue

        if i + 1 < len(string) and string[i:i+2] in DOUBLE_CHAR_OPERATORS:
            flush_token()
            tokens.append((TokenTypes.OP, string[i:i+2]))
            i += 2
            last_i = i
            continue

        if string[i] in SINGLE_CHAR_OPERATORS:
            flush_token()
            tokens.append((TokenTypes.OP, string[i]))
            i += 1
            last_i = i
            continue

        i += 1
    flush_token()
    return tokens

def recursive_eval(tokens):
    def eval_atom(token):
        print(f"Eval {token}")
        token_type = token[0]
        token_value = token[1]
        if token_type == TokenTypes.IDENT:
            if token_value in labels:
                return labels[token_value]
            elif token_value in macros:
                return recursive_eval(tokenize_expr(macros[token_value]))
            else:
                raise ValueError(f"Unknown label: {token_value}")
        if token_type == TokenTypes.NUMBER:
            try:
                if token_value.startswith('0x'):
                    return int(token_value, 16)
                if token_value.startswith('0b'):
                    return int(token_value, 2)
                return int(token_value, 10)
            except:
                raise ValueError(f"Invalid value: {token_value}")
        # if token_value.startswith("'") and token_value.endswith("'"):
        #     return ord(token_value)
        raise ValueError(f"Invalid value: {token_value}")
    print('evaluating:', tokens)
    if len(tokens) == 1:
        return eval_atom(tokens[0])
    
    lowest_priority = -1
    lowest_i = -1
    lowest_op_parenthesis = 999
    min_parenthesis = 999
    values_count = 0

    current_parenthesis = 0

    i = 0
    while i < len(tokens):
        token = tokens[i]
            # print('token:', token[1])
        if token[1] == '(':
            current_parenthesis += 1
        elif token[1] == ')':
            current_parenthesis -= 1           
            if current_parenthesis < 0:
                raise ValueError("Mismatched right parenthesis!")
        else:
            if current_parenthesis < min_parenthesis:
                min_parenthesis = current_parenthesis
            if token[0] == TokenTypes.OP:
                if token[1] in OPERATOR_PRIORITIES and (current_parenthesis < lowest_op_parenthesis or current_parenthesis == lowest_op_parenthesis and OPERATOR_PRIORITIES[token[1]] > lowest_priority or OPERATOR_PRIORITIES[token[1]] == lowest_priority and current_parenthesis == lowest_op_parenthesis and i > lowest_i):
                    lowest_priority = OPERATOR_PRIORITIES[token[1]]
                    lowest_i = i
                    lowest_op_parenthesis = current_parenthesis
            else:
                values_count += 1
        i += 1
    if current_parenthesis > 0:
        raise ValueError("Mismatched left parenthesis!")
    if min_parenthesis > 0 and min_parenthesis < 999:
        for i in range(min_parenthesis):
            # print('whole expression is in parenthesis')
            tokens = tokens[1:-1]
            if lowest_i > 0:
                lowest_i -= 1
    if lowest_i == -1:
        # print('no operators!')
        if values_count == 1:
            return eval_atom(tokens[0])
        else:
            raise ValueError('No operators found')
    
    first_half = tokens[:lowest_i]
    second_half = tokens[lowest_i + 1:]
    operator = tokens[lowest_i][1]
    print('first half:', first_half)
    print('second half:', second_half)
    print('operator:', operator)
    if first_half and second_half:
        first_half_eval = recursive_eval(first_half)
        second_half_eval = recursive_eval(second_half)
        print('now evaluating:', first_half_eval, operator, second_half_eval)

        if operator == '+':
            return first_half_eval + second_half_eval
        if operator == '-':
            return first_half_eval - second_half_eval
        if operator == '*':
            return first_half_eval * second_half_eval
        if operator == '/':
            return first_half_eval // second_half_eval
        if operator == '==':
            return first_half_eval == second_half_eval
        if operator == '!=':
            return first_half_eval != second_half_eval
        if operator == '>':
            return first_half_eval > second_half_eval
        if operator == '<':
            return first_half_eval < second_half_eval
        if operator == '>=':
            return first_half_eval >= second_half_eval
        if operator == '<=':
            return first_half_eval <= second_half_eval
        else: 
            raise ValueError(f"Operator not implemented: {operator}")
    elif second_half:
        if operator in UNARY_OPERATORS:
            print('unary operator')
            second_half_eval = recursive_eval(second_half)
            if operator == '!':
                return 0 if second_half_eval else 1
            if operator == '-':
                return -second_half_eval
            if operator == '+':
                return second_half_eval
            else: 
                raise ValueError(f"Operator not implemented: {operator}")
        else:
            raise ValueError('Mismatched operator!')
        
labels = {}
macros = {}

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
    if args.verbose:
        print("Labels: ", labels)
        print("Macros: ", macros)

    # actual assebmling
    cur_address = 0
    instruction_bits = bytearray([])
    for line in lines:
        print(line)
        line = line.strip()
        if line.startswith(';'): # comment
            continue
        # if line.startswith('.'): # preprocessor instruction
        #     continue
        parts = line.split(';')[0].split(None, 1)                
        if not parts:  # empty line
            continue

        instruction = parts[0]
        instr_args = []
        if len(parts) > 1:
            for token in parts[1].split(','):
                token = token.strip()
                if token == ';':
                    break
                else:
                    instr_args.append(token)

        instruction = instruction.upper()
        if instruction in opcode_table:
            opcode = opcode_table[instruction]
            instruction_bits.append(opcode['opcode'])
            match opcode['format']:
                case EncodingFormat.FORMAT_NONE:
                    if args.verbose: 
                        print(f"{hex(cur_address)}: {hex(opcode['opcode'])}")
                case EncodingFormat.FORMAT_REG:
                    reg_byte = recursive_eval(tokenize_expr(instr_args[0])) << 4
                    instruction_bits.append(reg_byte)
                    if args.verbose: 
                        print(f"{hex(cur_address)}: {hex(opcode['opcode'])} {reg_byte}")
                case EncodingFormat.FORMAT_REG_REG:
                    reg_byte = recursive_eval(tokenize_expr(instr_args[0])) << 4 | recursive_eval(tokenize_expr(instr_args[1]))
                    instruction_bits.append(reg_byte)
                    if args.verbose: 
                        print(f"{hex(cur_address)}: {hex(opcode['opcode'])} {reg_byte}")
                case EncodingFormat.FORMAT_IMM:
                    print(instr_args[0])
                    value = recursive_eval(tokenize_expr(instr_args[0]))
                    instruction_bits.append(value & LOWER_BYTE)
                    instruction_bits.append((value & HIGHER_BYTE) >> 8)
                    if args.verbose: 
                        print(f"{hex(cur_address)}: {hex(opcode['opcode'])} {value & LOWER_BYTE} {(value & HIGHER_BYTE) >> 8}")
                case EncodingFormat.FORMAT_REG_IMM:
                    reg_byte = recursive_eval(tokenize_expr(instr_args[0])) << 4
                    instruction_bits.append(reg_byte)
                    value = recursive_eval(tokenize_expr(instr_args[1]))
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
                        byte = recursive_eval(tokenize_expr(arg))
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
    for bit in instruction_bits:
        print(f"{hex(bit)}", end=', ')
    print()
    print(f"{len(instruction_bits)} bytes total.")
    with open(output_path, 'wb') as file:
        file.write(instruction_bits)

if __name__ == '__main__':
    main()