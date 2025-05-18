def parse_arg(a):
    if a.startswith('..'):
        arg = data[data[int(a[2:])]]
    elif a.startswith('.'):
        arg = data[int(a[1:])]
    else:
        arg = int(a)
    return arg

def parse_reg(a):
    if a.startswith('..'):
        arg = data[int(a[2:])]
    else:
        arg = int(a[1:])
    return arg

data = [0 for _ in range(256)]
# 0: program counter

code = """
print 49 вывод

set .1 10 задание данных
set .2 5 
add .1 .2 сложение
print .1 вывод результата

add .0 1 переходим на строку вниз
print 999 это не выведется
print 1000 это выведется

set .3 10
ifz .3 если .3 равен 0
add .0 3 переходим за пределы цикла
sub .3 1
print .3
sub .0 5

set .10 11
set ..10 20
print .10
print ..10

dump

halt
"""

lines = code.splitlines()
while True:
    pc = data[0]
    data[0] += 1
    line = lines[pc]
    tokens = line.split()
    # print("tokens:", tokens)
    if not tokens:
        continue    
    elif tokens[0] == "print":
        arg = parse_arg(tokens[1])
        print(arg)
    elif tokens[0] == "set":
        arg = parse_arg(tokens[2])
        data[parse_reg(tokens[1])] = arg
    elif tokens[0] == "add":
        arg = parse_arg(tokens[2])
        data[parse_reg(tokens[1])] += arg
    elif tokens[0] == "sub":
        arg = parse_arg(tokens[2])
        data[parse_reg(tokens[1])] -= arg
    elif tokens[0] == "ifz":
        if data[int(tokens[1][1:])] == 0:
            pass
        else:
            data[0] += 1
    elif tokens[0] == "dump":
        print("data:", ' '.join([str(a) for a in data]))
    elif tokens[0] == "halt":
        break


