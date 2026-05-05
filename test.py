SINGLE_CHAR_OPERATORS = ['+', '-', '*', '/', '(', ')', '&', '|', '^']
DOUBLE_CHAR_OPERATORS = ['<<', '>>']

def tokenize(string: str):
    def flush_token():
        if i > last_i:
            tokens.append(string[last_i:i])
    tokens = []
    last_i = 0
    i = 0
    while i < len(string):
        print(last_i, i, string[i])
        if string[i].isspace():
            flush_token()
            i += 1
            last_i = i
            continue

        if i + 1 < len(string) and string[i:i+2] in DOUBLE_CHAR_OPERATORS:
            flush_token()
            tokens.append(string[i:i+2])
            i += 2
            last_i = i
            continue

        if string[i] in SINGLE_CHAR_OPERATORS:
            flush_token()
            tokens.append(string[i])
            i += 1
            last_i = i
            continue

        i += 1
    if i > last_i:
        tokens.append(string[last_i:i])
    return tokens

if __name__ == '__main__':
    print(tokenize('cat+dog'))
    print(tokenize('cat+dog*meow'))
    print(tokenize('*meow'))
    print(tokenize('meow+'))
    print(tokenize('(meow)*( kittens +  cats)'))
    print(tokenize('14 <<    35'))
    