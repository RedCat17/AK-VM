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

class RecordTypes:
    INSTRUCTION = 0
    DATA_BYTES = 1
    DATA_STRING = 2
    DIRECTIVE = 3

class Record:
    def __init__(self, type, address, size, payload):
        self.address = address
        self.payload = payload
        self.size = size
        self.type = type
        self.encoded_bytes = bytearray()

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
        # print(f"Eval {token}")
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
    # print('evaluating:', tokens)
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
    # print('first half:', first_half)
    # print('second half:', second_half)
    # print('operator:', operator)
    if first_half and second_half:
        first_half_eval = recursive_eval(first_half)
        second_half_eval = recursive_eval(second_half)
        # print('now evaluating:', first_half_eval, operator, second_half_eval)

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
            # print('unary operator')
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

def encode_instruction(record, verbose=False):
    opcode_info = opcode_table[record.payload['mnemonic']]
    opcode = opcode_info['opcode']
    format = opcode_info['format']

    operands = record.payload['operands']

    record.encoded_bytes.append(opcode)
    match format:
        case EncodingFormat.FORMAT_NONE:
            pass
        case EncodingFormat.FORMAT_REG:
            reg_byte = recursive_eval(tokenize_expr(operands[0])) << 4
            
            record.encoded_bytes.append(reg_byte)
        case EncodingFormat.FORMAT_REG_REG:
            reg_byte = recursive_eval(tokenize_expr(operands[0])) << 4 | recursive_eval(tokenize_expr(operands[1]))

            record.encoded_bytes.append(reg_byte)
        case EncodingFormat.FORMAT_IMM:
            value = recursive_eval(tokenize_expr(operands[0]))

            lower = value & LOWER_BYTE
            higher = (value & HIGHER_BYTE) >> 8

            record.encoded_bytes.append(lower)
            record.encoded_bytes.append(higher)
        case EncodingFormat.FORMAT_REG_IMM:
            reg_byte = recursive_eval(tokenize_expr(operands[0])) << 4
            record.encoded_bytes.append(reg_byte)

            value = recursive_eval(tokenize_expr(operands[1]))

            lower = value & LOWER_BYTE
            higher = (value & HIGHER_BYTE) >> 8

            record.encoded_bytes.append(lower)
            record.encoded_bytes.append(higher)
        case _:
            raise ValueError("Unknown encoding format!")

def encode_data_bytes(record, verbose=False):
    values = record.payload['values']
    
    for value_expr in values:
        value = recursive_eval(tokenize_expr(value_expr))
        byte = value & 0xFF
        record.encoded_bytes.append(byte)

def encode_data_string(record, verbose=False):
    string = record.payload['string']

    for ch in string:
        record.encoded_bytes.append(ord(ch))  

def generate_listing(records):
    lines = []

    for record in records:
        addr_col = f"{(record.address):05X}"
        hex_bytes = ' '.join(f"{b:02X}" for b in record.encoded_bytes)
        hex_col = f"{hex_bytes}".ljust(45)
            
        match record.type:
            case RecordTypes.INSTRUCTION:       
                mnemonic = record.payload['mnemonic']
                operands = ' '.join(record.payload['operands'])
                text_col = f"{mnemonic} {operands}"
                pass
            case RecordTypes.DATA_BYTES:   
                values = record.payload['values']
                text_col = ' '.join(values)
            case RecordTypes.DATA_STRING:   
                text_col = record.payload['string']
            case RecordTypes.DIRECTIVE:
                raise NotImplementedError("Directives are not implemented yet!")
        lines.append(f"{addr_col}: {hex_col} {text_col}")
    
    return '\n'.join(lines)

def generate_binary(records):
    output = bytearray()
    for record in records:
        for byte in record.encoded_bytes:
            output.append(byte)

labels = {}
macros = {}
extern = {}

records = []

def main():
    # Console argument parsing
    parser = argparse.ArgumentParser(description='Assembler for AK-VM-1')

    parser.add_argument("input_file", help="Path to input source file")
    parser.add_argument("-o", "--output", help="Path to assembled output file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # File reading and splitting into lines
    with open(args.input_file, 'r') as file:
        lines = [line.strip() for line in file.readlines() if (line.strip() and not line.startswith(';'))]

    # First pass:
    # 1. produce symbol tables
    # 2. produce instruction/data records list with addresses and sizes
    cur_address = 0
    for line in lines:
        # if label
        if line.endswith(':'):
            labels[line[:-1]] = cur_address
        # if instruction or data
        else:
            raw = line.split(';')[0].strip() # remove comments
            instruction, *rest = raw.split(None, 1)
            # if instruction
            if instruction in opcode_table:
                operands = []
                if rest:
                    operands = [op.strip() for op in rest[0].split(',')]
                # print(tokenize_expr(operands))
                opcode = opcode_table[instruction]
                size = FORMAT_LENGTHS[opcode['format']]
                records.append(Record(
                    RecordTypes.INSTRUCTION, 
                    cur_address, 
                    size, 
                    {
                        "mnemonic": instruction,
                        "operands": operands
                    }))
                cur_address += size
            # if data
            elif instruction == '.DB':
                values = [v.strip() for v in rest[0].split(',')]
                size = len(values)
                records.append(Record(
                    RecordTypes.DATA_BYTES, 
                    cur_address, 
                    size, 
                    {
                        "bytes": values
                    }))
                cur_address += size
            elif instruction == '.STR':
                string = rest[0].strip('"')
                size = len(string)
                records.append(Record(
                    RecordTypes.DATA_STRING, 
                    cur_address, 
                    size, 
                    {
                        "string": string
                    }))
                cur_address += size
            elif instruction == '.DEF':
                parts = rest[0].split(None, 1)
                name = parts[0]
                value = parts[1]
                macros[name] = value
            else:
                raise ValueError(f"Unknown instruction: {instruction}")
                break
    
    # Verbose outout
    if args.verbose:
        print("Labels: ", labels)
        print("Macros: ", macros)
        print("Records:")
        for record in records:
            print(f"{record.address}: type={record.type} size={record.size}, payload={record.payload}")

    # Second pass:
    # 1. resolve expressions and operands using labels & macros
    # 2. encode instructions into bytes
    # 3. produce enriched records
    for record in records:
        match record.type:
            case RecordTypes.INSTRUCTION:                
                encode_instruction(record, args.verbose)
            case RecordTypes.DATA_BYTES:   
                encode_data_bytes(record, args.verbose)
            case RecordTypes.DATA_STRING:   
                encode_data_string(record, args.verbose)
            case RecordTypes.DIRECTIVE:
                raise NotImplementedError("Directives are not implemented yet!")

    
    # Show listing
    if args.verbose:
        print("\nListing:")   
        print(generate_listing(records))

    # Encode binary
    output = generate_binary(records)

    output_path = args.output or args.input_file + '.bin'
    for byte in output:
        print(f"{hex(byte)}", end=', ')

    print(f"\n{len(output)} bytes total.")
    
    with open(output_path, 'wb') as file:
        file.write(output)

if __name__ == '__main__':
    main()