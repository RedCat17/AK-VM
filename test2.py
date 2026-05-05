class TokenTypes:
    NUMBER = 0
    IDENT = 1
    OP = 2
    STRING = 3
# Token format: (TYPE, VALUE)

SINGLE_CHAR_OPERATORS = ['+', '-', '*', '/', '(', ')', '&', '|', '^', '!']
DOUBLE_CHAR_OPERATORS = ['<<', '>>']

OPERATOR_PRIORITIES = { # higher = lower priority
    '!': 0,
    '*': 1,
    '/': 1,
    '+': 2,
    '-': 2,
    '<<': 3,
    '>>': 3,
    '^': 4,
    '&': 5,
    '|': 6
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
    if not value.isdigit():
        raise ValueError(f'Invalid number: {value}')

def parse_imm(token):
    # print(f"Parsing {value}")
    token_type = token[0]
    token_value = token[1]
    if token_type == TokenTypes.IDENT:
        if token_value in labels:
            return labels[token_value]
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

def tokenize(string: str):
    def flush_token():
        if i > last_i:
            token = string[last_i:i]
            if not token.isalnum():
                raise ValueError(f"Invalid characters in token: {token}")
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
        # print(last_i, i, string[i])
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
    print('evaluating:', tokens)
    if len(tokens) == 1:
        print('parsed imm:', parse_imm(tokens[0]))
        return parse_imm(tokens[0])
    
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
    print('min par', min_parenthesis)
    if min_parenthesis > 0 and min_parenthesis < 999:
        for i in range(min_parenthesis):
            print('whole expression is in parenthesis')
            tokens = tokens[1:-1]
            if lowest_i > 0:
                lowest_i -= 1
            print(f'cleared expression: {tokens}')
    print('lowest i', lowest_i)
    if lowest_i == -1:
        print('no operators!')
        if values_count == 1:
            print('parsed imm:', parse_imm(tokens[0]))
            return parse_imm(tokens[0])
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

        

if __name__ == '__main__':
    print(recursive_eval(tokenize('2+2')))
    print(recursive_eval(tokenize('2 + 2 * 2')))
    print(recursive_eval(tokenize('2 * 2 + 2')))
    print(recursive_eval(tokenize('2 + 2 + 2')))
    print(recursive_eval(tokenize('(2 + 2)')))
    print(recursive_eval(tokenize('2 * (2 + 2)')))
    # print(recursive_eval(tokenize('(3+2)) + 1')))
    print(recursive_eval(tokenize('-1 + 1')))
    print(recursive_eval(tokenize('-(1 + 1)')))
    print(recursive_eval(tokenize('-(! 1 + (-1))')))
    print(recursive_eval(tokenize('(((2+1)))')))
    print(recursive_eval(tokenize('(((2)))')))
    # print(recursive_eval(tokenize('1 - -1')))
    print(recursive_eval(tokenize('1 - !1')))
    # print(recursive_eval(tokenize('12b')))
    print(recursive_eval(tokenize('0b0100')))
    print(recursive_eval(tokenize('0x0100')))