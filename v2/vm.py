import sys

# Basic
def op_hlt(vm, args):
    vm.running = False

def op_dump(vm, args):
    print(f"PC: {vm.pc}, SP: {vm.sp}, FP: {vm.fp}, FLAGS: {vm.flags}")
    reg = ' '.join([str(a) for a in vm.reg])
    print(f"Reg: {reg}")
    stack = ' '.join([str(a) for a in vm.stack])
    print(f"Stack: {stack}")
    # mem = ' '.join([str(a) for a in vm.mem])
    mem = vm.mem
    print(f"Mem:", *vm.mem)

# Register and Arithmetics
def op_set(vm, args):
    dest, val = args
    vm.reg[dest] = val

def op_add(vm, args):
    dest, src = args
    vm.reg[dest] += vm.reg[src]

def op_sub(vm, args):
    dest, src = args
    vm.reg[dest] -= vm.reg[src]

# Memory
def op_load(vm, args):
    dest, addr = args
    vm.reg[dest] = vm.mem[addr]

def op_store(vm, args):
    addr, src = args
    vm.mem[addr] = vm.reg[src]

def op_loadi(vm, args):
    dest, ptr_reg = args
    addr = vm.reg[ptr_reg]
    vm.reg[dest] = vm.mem[addr]

def op_storei(vm, args):
    ptr_reg, src = args
    addr = vm.reg[ptr_reg]
    vm.mem[addr] = vm.reg[src]

# Stack
def op_push(vm, args):
    src = args[0]
    if vm.sp >= len(vm.stack) - 1:
        raise RuntimeError("Stack overflow")
    vm.sp += 1
    vm.stack[vm.sp] = vm.reg[src]

def op_pop(vm, args):
    if vm.sp < 0:
        raise RuntimeError("Stack underflow")
    dest = args[0]
    vm.reg[dest] = vm.stack[vm.sp]
    vm.sp -= 1

# I/O
def op_out(vm, args):
    src = args[0]
    print(chr(vm.reg[src]), end="")

def op_print(vm, args):
    src = args[0]
    print(vm.reg[src])

def op_input(vm, args):
    dest = args[0]
    val = ord(input())
    vm.reg[dest] = val

# Control flow
def op_jmp(vm, args):
    dest = args[0]
    vm.pc = dest

def op_jmpr(vm, args):
    destv = args[0]
    vm.pc = vm.reg[dest]

def op_cmp(vm, args):
    reg1, reg2 = args
    vm.flags = (vm.reg[reg1] == vm.reg[reg2])

def op_jmz(vm, args):
    dest = args[0]
    if vm.flags:
        vm.pc = dest

def op_jmzv(vm, args):
    destv = args[0]
    if vm.flags:
        vm.pc = destv
    
def dispatch(vm, instr):
    opcode, *args = instr
    args = list(map(int, args))
    print(">", opcode, *args)
    vm.op_table[opcode](vm, args)
    # op_dump(vm)

class VM:
    def __init__(self):
        self.pc = 0
        self.sp = -1
        self.fp = 0
        self.flags = 0
        self.reg = [0] * 8
        self.stack = [0] * 128
        self.mem = [0] * 1024

        self.labels = {}

        self.running = True
        
        self.code = [] 

        self.op_table = {
            "hlt": op_hlt,
            "dump": op_dump,

            "set": op_set,
            "add": op_add,
            "sub": op_sub,

            "load": op_load,
            "store": op_store,
            "loadi": op_loadi,
            "storei": op_storei,

            "push": op_push,
            "pop": op_pop,

            "print": op_print,
            "input": op_input,
            
            "jmp": op_jmp,
            "jmpr": op_jmpr,
            "cmp": op_cmp,
            "jmz": op_jmz,
            "jmzv": op_jmzv
        }
    
    def fetch_line(self):
        # print('pc', self.pc, self.code)
        line = self.code[self.pc]
        self.pc += 1
        return line

    def load_code(self, code):
        self.code = []        # reset code
        self.labels = {}      # reset labels

        lines = code.splitlines()

        for line in lines:
            tokens = line.strip().split()
            if not tokens:
                continue
            if tokens[0] == "lbl":
                label_name = tokens[1]
                self.labels[label_name] = len(self.code)
            else:
                self.code.append(tokens)

        for instr in self.code:
            opcode = instr[0]
            for i in range(1, len(instr)):
                arg = instr[i]
                if arg in self.labels:
                    instr[i] = str(self.labels[arg])
        
        for instr in self.code:
            print(instr)
        print("Labels:", self.labels)


    def run_code(self):
        while self.running:
            line = self.fetch_line()
            dispatch(self, line)
        

if __name__ == '__main__':
    vm = VM()
    codefile = sys.argv[1]
    with open(codefile, "r") as file:
        code = file.read() 
        vm.load_code(code)
    vm.run_code()