import argparse
from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class OperandImm:
    expr: list

@dataclass
class OperandReg:
    reg: int

# @dataclass
# class OperandAddr:
#     symbol: str
#     offset: int

# class EncodingFormat(Enum):
#     R = opcode | rd | rs1 | rs2 | funct
#     I = opcode | rd | rs | immediate
#     LS = opcode | rd | offset | rs(base)

class EncodingFormat(Enum):
    NONE = auto()
    REG = auto()
    REG_REG = auto()
    IMM = auto()
    REG_IMM = auto()

FORMAT_LENGTHS = {
    EncodingFormat.NONE: 1,
    EncodingFormat.REG: 2,
    EncodingFormat.REG_REG: 2,
    EncodingFormat.IMM: 3,
    EncodingFormat.REG_IMM: 4
}

LOWER_BYTE  = 0x00FF
HIGHER_BYTE = 0xFF00

@dataclass
class InstructionSpec:
    mnemonic: str
    opcode: int
    format: EncodingFormat
    # relocatable_operands: tuple[int]

instruction_table = {
    # Control flow
    'NOP': InstructionSpec(mnemonic='NOP', opcode=0x00, format=EncodingFormat.NONE),
    'HLT': InstructionSpec(mnemonic='HLT', opcode=0x01, format=EncodingFormat.NONE),
    'CMPRR': InstructionSpec(mnemonic='CMPRR', opcode=0x02, format=EncodingFormat.REG_REG),
    'CMPRI': InstructionSpec(mnemonic='CMPRI', opcode=0x03, format=EncodingFormat.REG_IMM),
    'JMP': InstructionSpec(mnemonic='JMP', opcode=0x04, format=EncodingFormat.IMM),
    'JMZ': InstructionSpec(mnemonic='JMZ', opcode=0x05, format=EncodingFormat.IMM),
    'JNZ': InstructionSpec(mnemonic='JNZ', opcode=0x06, format=EncodingFormat.IMM),
    'JMC': InstructionSpec(mnemonic='JMC', opcode=0x07, format=EncodingFormat.IMM),
    'JMS': InstructionSpec(mnemonic='JMS', opcode=0x08, format=EncodingFormat.IMM),
    'CALL': InstructionSpec(mnemonic='CALL', opcode=0x09, format=EncodingFormat.IMM),
    'RET': InstructionSpec(mnemonic='RET', opcode=0x0A, format=EncodingFormat.NONE),

    # Memory
    'MOVRR': InstructionSpec(mnemonic='MOVRR', opcode=0x10, format=EncodingFormat.REG_REG),
    'MOVRI': InstructionSpec(mnemonic='MOVRI', opcode=0x11, format=EncodingFormat.REG_IMM),
    'STORDR': InstructionSpec(mnemonic='STORDR', opcode=0x12, format=EncodingFormat.REG_IMM),
    'STORMI': InstructionSpec(mnemonic='STORMI', opcode=0x13, format=EncodingFormat.REG_IMM),
    'STORMR': InstructionSpec(mnemonic='STORMR', opcode=0x14, format=EncodingFormat.REG_REG),
    'LOADRD': InstructionSpec(mnemonic='LOADRD', opcode=0x15, format=EncodingFormat.REG_IMM),
    'LOADRM': InstructionSpec(mnemonic='LOADRM', opcode=0x16, format=EncodingFormat.REG_REG),
    'PUSHR': InstructionSpec(mnemonic='PUSHR', opcode=0x17, format=EncodingFormat.REG),
    'POPR': InstructionSpec(mnemonic='POPR', opcode=0x18, format=EncodingFormat.REG),
    'STORBDR': InstructionSpec(mnemonic='STORBDR', opcode=0x19, format=EncodingFormat.REG_IMM),
    'STORBMI': InstructionSpec(mnemonic='STORBMI', opcode=0x1A, format=EncodingFormat.REG_IMM),
    'STORBMR': InstructionSpec(mnemonic='STORBMR', opcode=0x1B, format=EncodingFormat.REG_REG),
    'LOADBRD': InstructionSpec(mnemonic='LOADBRD', opcode=0x1C, format=EncodingFormat.REG_IMM),
    'LOADBRM': InstructionSpec(mnemonic='LOADBRM', opcode=0x1D, format=EncodingFormat.REG_REG),

    # Arithmetics
    'ADDRR': InstructionSpec(mnemonic='ADDRR', opcode=0x20, format=EncodingFormat.REG_REG),
    'ADDRI': InstructionSpec(mnemonic='ADDRI', opcode=0x21, format=EncodingFormat.REG_IMM),
    'SUBRR': InstructionSpec(mnemonic='SUBRR', opcode=0x22, format=EncodingFormat.REG_REG),
    'SUBRI': InstructionSpec(mnemonic='SUBRI', opcode=0x23, format=EncodingFormat.REG_IMM),
    'INCR': InstructionSpec(mnemonic='INCR', opcode=0x24, format=EncodingFormat.REG),
    'DECR': InstructionSpec(mnemonic='DECR', opcode=0x25, format=EncodingFormat.REG),
    'MULRR': InstructionSpec(mnemonic='MULRR', opcode=0x26, format=EncodingFormat.REG_REG),
    'MULRI': InstructionSpec(mnemonic='MULRI', opcode=0x27, format=EncodingFormat.REG_IMM),
    'DIVRR': InstructionSpec(mnemonic='DIVRR', opcode=0x28, format=EncodingFormat.REG_REG),
    'DIVRI': InstructionSpec(mnemonic='DIVRI', opcode=0x29, format=EncodingFormat.REG_IMM),

    # Bit ops
    'ANDRR': InstructionSpec(mnemonic='ANDRR', opcode=0x30, format=EncodingFormat.REG_REG),
    'ANDRI': InstructionSpec(mnemonic='ANDRI', opcode=0x31, format=EncodingFormat.REG_IMM),
    'ORRR': InstructionSpec(mnemonic='ORRR', opcode=0x32, format=EncodingFormat.REG_REG),
    'ORRI': InstructionSpec(mnemonic='ORRI', opcode=0x33, format=EncodingFormat.REG_IMM),
    'XORRR': InstructionSpec(mnemonic='XORRR', opcode=0x34, format=EncodingFormat.REG_REG),
    'XORRI': InstructionSpec(mnemonic='XORRI', opcode=0x35, format=EncodingFormat.REG_IMM),
    'NOTR': InstructionSpec(mnemonic='NOTR', opcode=0x36, format=EncodingFormat.REG),
    'SHRR': InstructionSpec(mnemonic='SHRR', opcode=0x37, format=EncodingFormat.REG),
    'SHLR': InstructionSpec(mnemonic='SHLR', opcode=0x38, format=EncodingFormat.REG),

    # SP and BP ops
    'MOVSPR': InstructionSpec(mnemonic='MOVSPR', opcode=0x40, format=EncodingFormat.REG),
    'MOVRSP': InstructionSpec(mnemonic='MOVRSP', opcode=0x41, format=EncodingFormat.REG),
    'ADDSPI': InstructionSpec(mnemonic='ADDSPI', opcode=0x42, format=EncodingFormat.IMM),
    'SUBSPI': InstructionSpec(mnemonic='SUBSPI', opcode=0x43, format=EncodingFormat.IMM),
    'MOVBPR': InstructionSpec(mnemonic='MOVBPR', opcode=0x44, format=EncodingFormat.REG),
    'MOVRBP': InstructionSpec(mnemonic='MOVRBP', opcode=0x45, format=EncodingFormat.REG),
    'ADDBPI': InstructionSpec(mnemonic='ADDBPI', opcode=0x46, format=EncodingFormat.IMM),
    'SUBBPI': InstructionSpec(mnemonic='SUBBPI', opcode=0x47, format=EncodingFormat.IMM),
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

class ExprTypes:
    ILLEGAL = 0
    LOCAL = 1
    EXTERN = 2
    EXTERN_CONST = 3

# class ExprTypes:
#     ABSOLUTE = auto()
#     RELOCATABLE = auto()
#     INVALID = auto()

@dataclass
class InstructionPayload:
    mnemonic: str
    operands: list[str]

class Record:
    def __init__(self, type, address, size, payload):
        self.address = address
        self.payload = payload
        self.size = size
        self.type = type
        self.encoded_bytes = bytearray()
        self.relocations = [] # format: ('symbol', offset)

@dataclass
class ObjectHeader:
    name: str 
    length: int

@dataclass
class ODefineRecord:
    name: str
    address: int

@dataclass
class OReferenceRecord:
    name: str

@dataclass
class OTextRecord:
    address: int 
    data: bytearray

@dataclass
class OModificationRecord:
    address: int
    symbol: str

@dataclass
class OEndRecord:
    entry_point: int

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

def verify_register(value: str):
    if not value.startswith('R'):
        raise ValueError(f'Invalid register name: {value}')
    value = value[1:]
    if not value.isdigit():
        raise ValueError(f'Invalid register name: {value}')
    return int(value)

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

def check_expr(tokens):
    local = True
    for token in tokens:
        if token[0] == TokenTypes.IDENT:
            if token[1] in externs:
                local = False
                break
    # local expression (no external symbols)
    if local:
        return ExprTypes.LOCAL
    # single external symbol
    if len(tokens) == 1:
        return ExprTypes.EXTERN 
    # symbol +- constant
    if len(tokens) == 3:
        if (tokens[0][0] == TokenTypes.IDENT and (tokens[0][1] in externs)) and \
        (tokens[1][1] in ('+', '-')) and \
        ((tokens[2][0] in (TokenTypes.IDENT, TokenTypes.NUMBER)) and (tokens[2][1] not in externs)):
            return ExprTypes.EXTERN_CONST
    return ExprTypes.ILLEGAL

def encode_instruction(record, verbose=False):
    opcode_info = instruction_table[record.payload.mnemonic]
    opcode = opcode_info.opcode
    format = opcode_info.format

    operands = record.payload.operands

    record.encoded_bytes.append(opcode)
    match format:
        case EncodingFormat.NONE:
            pass
        case EncodingFormat.REG:
            tokens = tokenize_expr(operands[0])
            match check_expr(tokens):
                case ExprTypes.ILLEGAL:
                    raise ValueError("Illegal expression.")
                case ExprTypes.LOCAL:
                    reg_byte = recursive_eval(tokens) << 4
                    record.encoded_bytes.append(reg_byte)
                case ExprTypes.EXTERN | ExprTypes.EXTERN_CONST:
                    raise ValueError("Can't use external for register name.")

        case EncodingFormat.REG_REG:
            tokens1 = tokenize_expr(operands[0])
            match check_expr(tokens1):
                case ExprTypes.ILLEGAL:
                    raise ValueError("Illegal expression.")
                case ExprTypes.EXTERN | ExprTypes.EXTERN_CONST:
                    raise ValueError("Can't use external for register name.")
            tokens2 = tokenize_expr(operands[1])
            match check_expr(tokens2):
                case ExprTypes.ILLEGAL:
                    raise ValueError("Illegal expression.")
                case ExprTypes.EXTERN | ExprTypes.EXTERN_CONST:
                    raise ValueError("Can't use external for register name.")

            reg_byte = recursive_eval(tokens1) << 4 | recursive_eval(tokens2)

            record.encoded_bytes.append(reg_byte)
        case EncodingFormat.IMM:
            tokens = tokenize_expr(operands[0])
            match check_expr(tokens):
                case ExprTypes.ILLEGAL:
                    raise ValueError("Illegal expression.")
                case ExprTypes.LOCAL:
                    value = recursive_eval(tokens)

                    lower = value & LOWER_BYTE
                    higher = (value & HIGHER_BYTE) >> 8

                    record.encoded_bytes.append(lower)
                    record.encoded_bytes.append(higher)
                case ExprTypes.EXTERN:
                    print(f"relocations in: {tokens}")
                    record.relocations.append((tokens2[0][1], 0))
                    record.encoded_bytes.append(0)
                    record.encoded_bytes.append(0)
                case ExprTypes.EXTERN_CONST:
                    raise ValueError("Offset not yet implemented.")

        case EncodingFormat.REG_IMM:
            tokens1 = tokenize_expr(operands[0])
            match check_expr(tokens1):
                case ExprTypes.ILLEGAL:
                    raise ValueError("Illegal expression.")
                case ExprTypes.EXTERN | ExprTypes.EXTERN_CONST:
                    raise ValueError("Can't use external for register name.")
                case ExprTypes.LOCAL:
                    reg_byte = recursive_eval(tokens1) << 4
                    record.encoded_bytes.append(reg_byte)
            
            tokens2 = tokenize_expr(operands[1])
            match check_expr(tokens2):
                case ExprTypes.ILLEGAL:
                    raise ValueError("Illegal expression.")
                case ExprTypes.LOCAL:
                    value = recursive_eval(tokens2)

                    lower = value & LOWER_BYTE
                    higher = (value & HIGHER_BYTE) >> 8

                    record.encoded_bytes.append(lower)
                    record.encoded_bytes.append(higher)
                case ExprTypes.EXTERN:
                    print(f"relocations in: {tokens}")
                    record.relocations.append((tokens[0][1], 0))
                    record.encoded_bytes.append(0)
                    record.encoded_bytes.append(0)
                case ExprTypes.EXTERN_CONST:
                    raise ValueError("Offset not yet implemented.")
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
                mnemonic = record.payload.mnemonic
                operands = ' '.join(record.payload.operands)
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
    return output

def generate_object(records):
    object = []

    # H record
    object.append(ObjectHeader("program", 999))

    # D record
    for symbol in exports:
        if symbol in labels:
            address = labels[symbol]
            object.append(ODefineRecord(symbol, address))
        else:
            raise ValueError("Exported symbol is undefined!")
    # R records
    for symbol in externs:
        object.append(OReferenceRecord(symbol))

    # T records
    # no text record limits yet
    bytes = generate_binary(records)
    object.append(OTextRecord(0, bytes))

    # M records
    for record in records:
        if record.relocations:
            reloc = record.relocations[0]
            object.append(OModificationRecord(record.address + 1, reloc[0])) # address should be remade

    # E record
    object.append(OEndRecord(0))

    return object

def generate_object_listing(object):
    lines = []
    for record in object:
        match record:
            case ObjectHeader():
                lines.append(f"H | {record.name:<10}")
            case ODefineRecord():
                lines.append(f"D | {record.name:<10} | {record.address}")
            case OReferenceRecord():
                lines.append(f"R | {record.name:<10}")
            case OTextRecord():
                hex_bytes = ' '.join(f"{b:02X}" for b in record.data)
                lines.append(f"T | {record.address:<10} | {hex_bytes}")
            case OModificationRecord():
                lines.append(f"M | {record.address:<10} | {record.symbol}")
            case OEndRecord():
                lines.append(f"E | {record.entry_point:<10}")
    listing = '\n'.join(lines)
    return listing

labels = {}
macros = {}
externs = []
exports = []

records = []

def main():
    # Console argument parsing
    parser = argparse.ArgumentParser(description='Assembler for AK-VM-1')

    parser.add_argument("input_file", help="Path to input source file")
    parser.add_argument("-o", "--output", help="Path to assembled output file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "-f", "--format", 
        choices=["bin", "obj"],
        help="Output format",
        required=True)

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
            match instruction:
                # data
                case '.DB':
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
                case '.STR':
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
                # constants
                case '.DEF':
                    parts = rest[0].split(None, 1)
                    name = parts[0]
                    value = parts[1]
                    macros[name] = value
                # external symbol 
                case '.EXTERN':
                    ident = rest[0]
                    externs.append(ident)
                # global symbol definition
                case '.EXPORT':
                    ident = rest[0]
                    exports.append(ident)
                case _:
                    # if instruction
                    if instruction in instruction_table:
                        operands = []
                        if rest:
                            operands = [op.strip() for op in rest[0].split(',')]
                        # print(tokenize_expr(operands))
                        opcode = instruction_table[instruction]
                        size = FORMAT_LENGTHS[opcode.format]
                        records.append(Record(
                            RecordTypes.INSTRUCTION, 
                            cur_address, 
                            size, 
                            InstructionPayload(instruction, operands)
                            ))
                        cur_address += size                    
                    else:
                        raise ValueError(f"Unknown instruction: {instruction}")
                        break
    
    # Verbose outout
    if args.verbose:
        print("Labels: ", labels)
        print("Macros: ", macros)
        print("External: ", externs)
        print("Exports: ", exports)
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

    # Verbose outout
    if args.verbose:
        print("\nEnriched records:")
        for record in records:
            string = f"{record.address}: type={record.type} size={record.size}, payload={record.payload}, bytes={record.encoded_bytes}"
            if record.relocations:
                string += f", relocations={record.relocations}"
            print(string)

    
    # Show listing
    if args.verbose:
        print("\nListing:")   
        print(generate_listing(records))

    match args.format:
        case "bin":
            # Encode binary
            output = generate_binary(records)

            output_path = args.output or args.input_file + '.bin'
            for byte in output:
                print(f"{hex(byte)}", end=', ')

            print(f"\n{len(output)} bytes total.")
            
            with open(output_path, 'wb') as file:
                file.write(output)
        case "obj":
            # Generate object
            object = generate_object(records)

            if args.verbose:
                print("\nObject listing:")   
                print(generate_object_listing(object))

if __name__ == '__main__':
    main()