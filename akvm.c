#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>

#define REG_COUNT 16
#define MEMORY_SIZE 0x10000 // 64 KB

// Memory layout
#define HEAP_ADDRESS        0x4000
#define STACK_BEGIN         0xFFFE
#define STACK_END           0xF900

#define RX_ADDRESS              0xF800 // Writing to this address prints to console
#define TX_ADDRESS              0xF801 // Reading from here reads from console

// FLAGS register is split into bits using these bitmasks:
#define ZERO_FLAG  0b10000000
#define CARRY_FLAG 0b01000000
#define SIGN_FLAG  0b00100000
// WIP

// Masks for register encoding in bytecode:
#define REG1 0b11110000
#define REG2 0b00001111

// Opcodes
// Control flow
#define OPCODE_NOP     0x00
#define OPCODE_HLT     0x01
#define OPCODE_CMPR   0x02
#define OPCODE_CMPI   0x03
#define OPCODE_JMP     0x04
#define OPCODE_JMZ     0x05
#define OPCODE_JNZ     0x06
#define OPCODE_JC     0x07
#define OPCODE_JS     0x08
#define OPCODE_CALL    0x09
#define OPCODE_RET     0x0A

// Memory
#define OPCODE_MOVR   0x10
#define OPCODE_MOVI   0x11
#define OPCODE_STORDR  0x12
#define OPCODE_STORMI  0x13
#define OPCODE_STORMR  0x14
#define OPCODE_LOADRD  0x15
#define OPCODE_LOADRM  0x16
#define OPCODE_PUSH   0x17
#define OPCODE_POP    0x18
#define OPCODE_STORBDR  0x19
#define OPCODE_STORBMI  0x1A
#define OPCODE_STORBMR  0x1B
#define OPCODE_LOADBRD  0x1C
#define OPCODE_LOADBRM  0x1D

// Arithmetics
#define OPCODE_ADDR   0x20
#define OPCODE_ADDI   0x21
#define OPCODE_SUBR   0x22
#define OPCODE_SUBI   0x23
#define OPCODE_INC    0x24
#define OPCODE_DEC    0x25
#define OPCODE_MULR   0x26
#define OPCODE_MULI   0x27
#define OPCODE_DIVR   0x28
#define OPCODE_DIVI   0x29

// Bit ops
#define OPCODE_ANDR   0x30
#define OPCODE_ANDI   0x31
#define OPCODE_ORR    0x32
#define OPCODE_ORI    0x33
#define OPCODE_XORR   0x34
#define OPCODE_XORI   0x35
#define OPCODE_NOT    0x36
#define OPCODE_SHR    0x37
#define OPCODE_SHL    0x38

// SP and BP ops
#define OPCODE_SETSP  0x40
#define OPCODE_GETSP  0x41
#define OPCODE_ADDSP  0x42
#define OPCODE_SUBSP  0x43
#define OPCODE_SETBP  0x44
#define OPCODE_GETBP  0x45
#define OPCODE_ADDBP  0x46
#define OPCODE_SUBBP  0x47

// Encoding formats enum
typedef enum {
    FORMAT_NONE,
    FORMAT_REG,
    FORMAT_REG_REG, 
    FORMAT_IMM, // can be either immediate or address
    FORMAT_REG_IMM, 
} EncodingFormat;

// Opcode struct for storing name and format
typedef struct {
    const char *name;
    EncodingFormat format;
} OpcodeData;

// Opcode table
OpcodeData opcode_table[256] = {
    // Control flow
    [OPCODE_NOP]   = {"NOP",   FORMAT_NONE},
    [OPCODE_HLT]   = {"HLT",   FORMAT_NONE},
    [OPCODE_CMPR] = {"CMPR", FORMAT_REG_REG},
    [OPCODE_CMPI] = {"CMPI", FORMAT_REG_IMM},
    [OPCODE_JMP]   = {"JMP",   FORMAT_IMM},
    [OPCODE_JMZ]   = {"JMZ",   FORMAT_IMM},
    [OPCODE_JNZ]   = {"JNZ",   FORMAT_IMM},
    [OPCODE_JC]   = {"JC",   FORMAT_IMM},
    [OPCODE_JS]   = {"JS",   FORMAT_IMM},
    [OPCODE_CALL]  = {"CALL",  FORMAT_IMM},
    [OPCODE_RET]   = {"RET",   FORMAT_NONE},
    // Memory
    [OPCODE_MOVR]  = {"MOVR",  FORMAT_REG_REG},
    [OPCODE_MOVI]  = {"MOVI",  FORMAT_REG_IMM},
    [OPCODE_STORDR] = {"STORDR", FORMAT_REG_IMM},  // STORDI not included as it would require 2 immediate values
    [OPCODE_STORMI] = {"STORMI", FORMAT_REG_IMM},
    [OPCODE_STORMR] = {"STORMR", FORMAT_REG_REG},
    [OPCODE_LOADRD] = {"LOADRD", FORMAT_REG_IMM},
    [OPCODE_LOADRM] = {"LOADRM", FORMAT_REG_REG},
    [OPCODE_PUSH]  = {"PUSH",  FORMAT_REG},
    [OPCODE_POP]   = {"POP",   FORMAT_REG},
    [OPCODE_STORBDR] = {"STORBDR", FORMAT_REG_IMM},
    [OPCODE_STORBMI] = {"STORBMI", FORMAT_REG_IMM},
    [OPCODE_STORBMR] = {"STORBMR", FORMAT_REG_REG},
    [OPCODE_LOADBRD] = {"LOADBRD", FORMAT_REG_IMM},
    [OPCODE_LOADBRM] = {"LOADBRM", FORMAT_REG_REG},
    // Arithmetics
    [OPCODE_ADDR]  = {"ADDR",  FORMAT_REG_REG},
    [OPCODE_ADDI]  = {"ADDI",  FORMAT_REG_IMM},
    [OPCODE_SUBR]  = {"SUBR",  FORMAT_REG_REG},
    [OPCODE_SUBI]  = {"SUBI",  FORMAT_REG_IMM},
    [OPCODE_INC]   = {"INC",   FORMAT_REG},
    [OPCODE_DEC]   = {"DEC",   FORMAT_REG},
    [OPCODE_MULR]  = {"MULR",  FORMAT_REG_REG},
    [OPCODE_MULI]  = {"MULI",  FORMAT_REG_IMM},
    [OPCODE_DIVR]  = {"DIVR",  FORMAT_REG_REG},
    [OPCODE_DIVI]  = {"DIVI",  FORMAT_REG_IMM},

    // Bit ops
    [OPCODE_ANDR]  = {"ANDR",  FORMAT_REG_REG},
    [OPCODE_ANDI]  = {"ANDI",  FORMAT_REG_IMM},
    [OPCODE_ORR]   = {"ORR",   FORMAT_REG_REG},
    [OPCODE_ORI]   = {"ORI",   FORMAT_REG_IMM},
    [OPCODE_XORR]  = {"XORR",  FORMAT_REG_REG},
    [OPCODE_XORI]  = {"XORI",  FORMAT_REG_IMM},
    [OPCODE_NOT]   = {"NOT",   FORMAT_REG},
    [OPCODE_SHR]   = {"SHR",   FORMAT_REG},
    [OPCODE_SHL]   = {"SHL",   FORMAT_REG},

    // SP and BP ops
    [OPCODE_SETSP]  = {"SETSP",  FORMAT_REG},
    [OPCODE_GETSP]  = {"GETSP",  FORMAT_REG},
    [OPCODE_ADDSP]  = {"ADDSP",  FORMAT_IMM},
    [OPCODE_SUBSP]  = {"SUBSP",  FORMAT_IMM},
    [OPCODE_SETBP]  = {"SETBP",  FORMAT_REG},
    [OPCODE_GETBP]  = {"GETBP",  FORMAT_REG},
    [OPCODE_ADDBP]  = {"ADDBP",  FORMAT_IMM},
    [OPCODE_SUBBP]  = {"SUBBP",  FORMAT_IMM},
};

// CPU struct stores CPU internal data: registers, PC, SP, BP and flags
typedef struct {
    uint16_t registers[REG_COUNT];
    uint16_t pc, sp, bp;
    uint8_t flags;
} CPU;

// VM struct stores CPU and RAM
typedef struct {
    CPU cpu;
    uint8_t memory[MEMORY_SIZE]; // 64 KB RAM
} VM;

// initialize CPU, set all registers to zero
void init_cpu(CPU *cpu) {
    memset(cpu->registers, 0, sizeof(cpu->registers));
    cpu->pc = 0; 
    cpu->sp = STACK_BEGIN;
    cpu->bp = STACK_BEGIN;
    cpu->flags = 0;
}

// initialize whole VM, reset CPU and memory
void init_vm(VM *vm) {
    init_cpu(&vm->cpu);
    memset(vm->memory, 0, sizeof(vm->memory));
}

// Opens program from file and executes it byte-by-byte
int exec_load_program(VM *vm, const char *filename) {
    FILE *file = fopen(filename, "rb");

    if (!file) {
        perror("Failed to open progam file");
        return -1;
    }

    int byte = fgetc(file);
    size_t i = 0;
    while (byte != EOF && i < sizeof(vm->memory)) {
        vm->memory[i++] = byte;
        byte = fgetc(file);
    }
    fclose(file);
    return 0;
}

// dump CPU state to console
void dump_cpu(CPU *cpu) {
    fprintf(stderr, "PC: %X; SP: %X; BP: %X; Flags: %b;\n", cpu->pc, cpu->sp, cpu->bp, cpu->flags);
    fprintf(stderr, "Registers: ");
    for (uint8_t i = 0; i < REG_COUNT; i++) {
        fprintf(stderr, "%d ", cpu->registers[i]);
    }
    fprintf(stderr, "\n");
}

// dump VM state to console
void dump_vm(VM *vm) {
    dump_cpu(&vm->cpu);
    fprintf(stderr, "\nRAM: ");
    for (int i = 0; i < 256; i++) {
        fprintf(stderr, "%d ", vm->memory[HEAP_ADDRESS + i]);
    }    
    fprintf(stderr, "\nStack (top 64 bytes): ");
    for (int i = MEMORY_SIZE - 1; i > MEMORY_SIZE - 64; i--) {
        fprintf(stderr, "%d, ", vm->memory[i]);
    }
    fprintf(stderr, "\n");
}

// dump VM state to console
void dump_vm_verbose(VM *vm) {
    dump_cpu(&vm->cpu);
    fprintf(stderr, "\nProgram space: ");
    for (int i = 0; i < 1024; i++) {
        fprintf(stderr, "%d ", vm->memory[i]);
    }
    fprintf(stderr, "\nRAM: ");
    for (int i = 0; i < 256; i++) {
        fprintf(stderr, "%d ", vm->memory[HEAP_ADDRESS + i]);
    }    
    fprintf(stderr, "\nStack (top 64 bytes): ");
    for (int i = MEMORY_SIZE - 1; i > MEMORY_SIZE - 64; i--) {
        fprintf(stderr, "%X: %d, ", i, vm->memory[i]);
    }
    fprintf(stderr, "\n");
}

// set flags after substraction
void set_flags_sub(CPU *cpu, uint16_t a, uint16_t b, uint16_t result) { 
    cpu->flags &= ~(ZERO_FLAG | CARRY_FLAG | SIGN_FLAG);   
    if (result == 0) {
        cpu->flags |= ZERO_FLAG;
    }
    if (result & 0x8000) { // MSB
        cpu->flags |= SIGN_FLAG;
    }
    if (a < b) {
        cpu->flags |= CARRY_FLAG;
    }
}

// set flags after addition
void set_flags_add(CPU *cpu, uint16_t a, uint16_t b, uint16_t result) { 
    cpu->flags &= ~(ZERO_FLAG | CARRY_FLAG | SIGN_FLAG);   
    if (result == 0) {
        cpu->flags |= ZERO_FLAG;
    }
    if (result & 0x8000) { // MSB
        cpu->flags |= SIGN_FLAG;
    }
    if (result < a || result < b) {
        cpu->flags |= CARRY_FLAG;
    }
}

uint16_t cpu_add(CPU *cpu, uint16_t value1, uint16_t value2) {
    uint16_t result = value1 + value2;
    set_flags_add(cpu, value1, value2, result);
    return result;
}

uint16_t cpu_sub(CPU *cpu, uint16_t value1, uint16_t value2) {
    uint16_t result = value1 - value2;
    set_flags_sub(cpu, value1, value2, result);
    return result;
}

uint16_t cpu_mul(CPU *cpu, uint16_t value1, uint16_t value2) {
    uint16_t result = value1 * value2;
    set_flags_add(cpu, value1, value2, result);
    return result;
}

uint16_t cpu_div(CPU *cpu, uint16_t value1, uint16_t value2) {
    uint16_t result;
    if (value2 == 0) {
        result = 0;
    } else {
        result = value1 / value2;        
    }
    set_flags_add(cpu, value1, value2, result);
    return result;
}

int exec_stor(VM *vm, uint16_t address, uint16_t value) {
    if (address < HEAP_ADDRESS) {
        fprintf(stderr, "Address out of bounds! Can't write into program space.\n");
        return -1;
    }
    if (address >= STACK_END) {
        fprintf(stderr, "Address out of bounds! Can't write into stack.\n");
        return -1;
    }
    if (address == TX_ADDRESS) {
        if (value > 0xFF) { // > 1 byte
            fprintf(stderr, "Can't print > 1 byte!");
            return -1;
        }
        fprintf(stderr, "Printing %c (ASCII %d)\n", value, value);
        putchar(value);
    } else {
    vm->memory[address] = value & 0x00FF;
    vm->memory[address + 1] = (value & 0xFF00) >> 8;
    }
    return 0;
}

int exec_load(VM *vm, uint8_t reg, uint16_t address) {
    if (address == RX_ADDRESS) {
        vm->cpu.registers[reg] = getchar();
    } else {
    vm->cpu.registers[reg] = (vm->memory[address+1] << 8) | vm->memory[address];
    }
    return 0;
}

int exec_storb(VM *vm, uint16_t address, uint8_t value) {
    if (address < HEAP_ADDRESS) {
        fprintf(stderr, "Address out of bounds! Can't write into program space.\n");
        return -1;
    }
    if (address >= STACK_END) {
        fprintf(stderr, "Address out of bounds! Can't write into stack.\n");
        return -1;
    }
    if (address == TX_ADDRESS) {
        fprintf(stderr, "Printing %c (ASCII %d)\n", value, value);
        putchar(value);
    } else {
    vm->memory[address] = value & 0x00FF;
    }
    return 0;
}

int exec_loadb(VM *vm, uint8_t reg, uint16_t address) {
    if (address == RX_ADDRESS) {
        vm->cpu.registers[reg] = getchar();
    } else {
    vm->cpu.registers[reg] = vm->memory[address];
    }
    return 0;
}

int exec_push(VM *vm, uint16_t value) {
    if (vm->cpu.sp - 2 < STACK_END) {
        fprintf(stderr, "Stack overflow!\n");
        return -1;
    }
    vm->memory[vm->cpu.sp] = value & 0x00FF;
    vm->memory[vm->cpu.sp + 1] = (value >> 8);
    vm->cpu.sp -= 2;
    return 0;
}

int exec_pop(VM *vm, uint8_t reg) {
    if (vm->cpu.sp > MEMORY_SIZE - 2) {
        fprintf(stderr, "Stack underflow!\n");
        return -1;
    }
    vm->cpu.sp += 2;
    vm->cpu.registers[reg] = vm->memory[vm->cpu.sp] | (vm->memory[vm->cpu.sp - 1] << 8) ;
    return 0;
}

int exec_call(VM *vm, uint16_t address) {
    if (vm->cpu.sp - 2  < STACK_END) {
        fprintf(stderr, "Stack overflow!\n");
        return -1;
    }
    vm->memory[vm->cpu.sp] = vm->cpu.pc & 0x00FF;
    vm->memory[vm->cpu.sp - 1] = (vm->cpu.pc >> 8);
    vm->cpu.sp -= 2;
    vm->cpu.pc = address;
    return 0;
}

int exec_ret(VM *vm) {
    if (vm->cpu.sp > MEMORY_SIZE - 2) {
        fprintf(stderr, "Stack underflow!\n");
        return -1;
    }
    vm->cpu.sp += 2;
    vm->cpu.pc = vm->memory[vm->cpu.sp] | (vm->memory[vm->cpu.sp - 1] << 8) ;
    return 0;
}

// fetch-decode-execute loop
void run_vm(VM *vm) {
    for (;;) {
        uint8_t opcode = vm->memory[vm->cpu.pc++];
        uint8_t reg_byte; uint8_t reg1 = 0, reg2 = 0; uint16_t value = 0;
        uint16_t result; 
        OpcodeData opcode_data = opcode_table[opcode];
        switch (opcode_data.format) {
            case FORMAT_NONE:
                break;
            case FORMAT_REG:
                reg_byte = vm->memory[vm->cpu.pc++];
                reg1 = (reg_byte & REG1) >> 4;
                break;
            case FORMAT_REG_REG:
                reg_byte = vm->memory[vm->cpu.pc++];
                reg1 = (reg_byte & REG1) >> 4;
                reg2 = (reg_byte & REG2);
                break;
            case FORMAT_IMM:
                value = vm->memory[vm->cpu.pc++] | (vm->memory[vm->cpu.pc++] << 8);
                break;
            case FORMAT_REG_IMM:
                reg_byte = vm->memory[vm->cpu.pc++];
                reg1 = (reg_byte & REG1) >> 4;
                value = vm->memory[vm->cpu.pc++] | (vm->memory[vm->cpu.pc++] << 8);
                break;
        }
        fprintf(stderr, "opcode: 0x%02X; reg1: %d; reg2: %d; value: %d\n", opcode, reg1, reg2, value);
        switch (opcode) {
            // Control flow
            case OPCODE_NOP: 
                fprintf(stderr, "NOP...\n");
                break;
            case OPCODE_HLT: 
                fprintf(stderr, "Halting.\n");
                return;
            case OPCODE_CMPR: 
                fprintf(stderr, "CMP reg %d reg %d\n", reg1, reg2);
                cpu_sub(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                break;
            case OPCODE_CMPI: 
                fprintf(stderr, "CMP reg %d imm %d\n", reg1, value);
                cpu_sub(&vm->cpu, vm->cpu.registers[reg1], value);
                break;
            case OPCODE_JMP: 
                fprintf(stderr, "JMP adr %X\n", value);
                vm->cpu.pc = value;
                break;
            case OPCODE_JMZ: 
                fprintf(stderr, "JMZ adr %X\n", value);
                if (vm->cpu.flags & ZERO_FLAG) {
                    fprintf(stderr, "jumped\n");
                    vm->cpu.pc = value;
                }
                break;
            case OPCODE_JNZ: 
                fprintf(stderr, "JNZ adr %X\n", value);
                if (!(vm->cpu.flags & ZERO_FLAG)) {
                    fprintf(stderr, "jumped\n");
                    vm->cpu.pc = value;
                }
                break;
            case OPCODE_JC: 
                fprintf(stderr, "JC adr %X\n", value);
                if (vm->cpu.flags & CARRY_FLAG) {
                    fprintf(stderr, "jumped\n");
                    vm->cpu.pc = value;
                }
                break;
            case OPCODE_JS: 
                fprintf(stderr, "JC adr %X\n", value);
                if (vm->cpu.flags & SIGN_FLAG) {
                    fprintf(stderr, "jumped\n");
                    vm->cpu.pc = value;
                }
                break;
            case OPCODE_CALL: 
                fprintf(stderr, "CALL adr %X\n", value);
                exec_call(vm, value);
                break;
            case OPCODE_RET: 
                fprintf(stderr, "RET\n");
                exec_ret(vm);
                break;

            // Memory
            case OPCODE_MOVR: 
                fprintf(stderr, "MOV reg %d <- reg %d\n", reg1, reg2);
                vm->cpu.registers[reg1] = vm->cpu.registers[reg2];
                break;
            case OPCODE_MOVI: 
                fprintf(stderr, "MOV reg %d <- imm %d\n", reg1, value);
                vm->cpu.registers[reg1] = value;
                break;
            case OPCODE_STORDR: 
                fprintf(stderr, "STOR adr %X <- reg %d\n", value, reg1);
                exec_stor(vm, value, vm->cpu.registers[reg1]);
                break;
            case OPCODE_STORMI: 
                fprintf(stderr, "STOR ind %d <- imm %d\n", reg1, value);
                exec_stor(vm, vm->cpu.registers[reg1], value);
                break;
            case OPCODE_STORMR: 
                fprintf(stderr, "STOR ind %d <- reg2 %d\n", reg1, reg2);
                exec_stor(vm, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                break;
            case OPCODE_LOADRD: 
                fprintf(stderr, "LOAD reg %d <- adr %X\n", value, reg1);
                exec_load(vm, reg1, value);
                break;
            case OPCODE_LOADRM: 
                fprintf(stderr, "LOAD reg %d <- ind %d\n", reg1, reg2);
                exec_load(vm, reg1, vm->cpu.registers[reg2]);
                break;
            case OPCODE_PUSH: 
                fprintf(stderr, "PUSH reg %d\n", reg1);
                exec_push(vm, vm->cpu.registers[reg1]);
                break;
            case OPCODE_POP: 
                fprintf(stderr, "POP to reg %d\n", reg1);
                exec_pop(vm, reg1);
                break;
            case OPCODE_STORBDR: 
                fprintf(stderr, "STORB adr %X <- reg %d\n", value, reg1);
                exec_storb(vm, value, vm->cpu.registers[reg1]);
                break;
            case OPCODE_STORBMI: 
                fprintf(stderr, "STORB ind %d <- imm %d\n", reg1, value);
                exec_storb(vm, vm->cpu.registers[reg1], value);
                break;
            case OPCODE_STORBMR: 
                fprintf(stderr, "STORB ind %d <- reg2 %d\n", reg1, reg2);
                exec_storb(vm, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                break;
            case OPCODE_LOADBRD: 
                fprintf(stderr, "LOADB reg %d <- adr %X\n", value, reg1);
                exec_loadb(vm, reg1, value);
                break;
            case OPCODE_LOADBRM: 
                fprintf(stderr, "LOADB reg %d <- ind %d\n", reg1, reg2);
                exec_loadb(vm, reg1, vm->cpu.registers[reg2]);
                break;

            // Arithmetics
            case OPCODE_ADDR: 
                fprintf(stderr, "ADD reg %d <- reg %d\n", reg1, reg2);
                result = cpu_add(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_ADDI: 
                fprintf(stderr, "ADD reg %d <- imm %d\n", reg1, value);
                result = cpu_add(&vm->cpu, vm->cpu.registers[reg1], value);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_SUBR: 
                fprintf(stderr, "SUB reg %d <- reg %d\n", reg1, reg2);
                result = cpu_sub(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_SUBI: 
                fprintf(stderr, "SUB reg %d <- imm %d\n", reg1, value);
                result = cpu_sub(&vm->cpu, vm->cpu.registers[reg1], value);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_INC: 
                fprintf(stderr, "INC reg %d\n", reg1);
                result = cpu_add(&vm->cpu, vm->cpu.registers[reg1], 1);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_DEC: 
                fprintf(stderr, "DEC reg %d\n", reg1);
                result = cpu_sub(&vm->cpu, vm->cpu.registers[reg1], 1);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_MULR: 
                fprintf(stderr, "MUL reg %d <- reg %d\n", reg1, reg2);
                result = cpu_mul(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_MULI: 
                fprintf(stderr, "MUL reg %d <- imm %d\n", reg1, value);
                result = cpu_mul(&vm->cpu, vm->cpu.registers[reg1], value);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_DIVR: 
                fprintf(stderr, "DIV reg %d <- reg %d\n", reg1, reg2);
                result = cpu_div(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_DIVI: 
                fprintf(stderr, "DIV reg %d <- imm %d\n", reg1, value);
                result = cpu_div(&vm->cpu, vm->cpu.registers[reg1], value);
                vm->cpu.registers[reg1] = result;
                break;

            // Bit ops
            case OPCODE_ANDR:
                fprintf(stderr, "AND reg %d reg %d.\n", reg1, reg2);
                vm->cpu.registers[reg1] &= vm->cpu.registers[reg2];
                break;
            case OPCODE_ANDI: 
                fprintf(stderr, "AND reg %d imm %d.\n", value, reg1);
                vm->cpu.registers[reg1] &= value;
                break;
            case OPCODE_ORR: 
                fprintf(stderr, "OR reg %d reg %d.\n", reg1, reg2);
                vm->cpu.registers[reg1] |= vm->cpu.registers[reg2];
                break;
            case OPCODE_ORI: 
                fprintf(stderr, "OR reg %d imm %d.\n", value, reg1);
                vm->cpu.registers[reg1] |= value;
                break;
            case OPCODE_XORR: 
                fprintf(stderr, "XOR reg %d reg %d.\n", reg1, reg2);
                vm->cpu.registers[reg1] ^= vm->cpu.registers[reg2];
                break;
            case OPCODE_XORI: 
                fprintf(stderr, "XOR reg %d imm %d.\n", value, reg1);
                vm->cpu.registers[reg1] ^= value;
                break;
            case OPCODE_NOT: 
                fprintf(stderr, "NOT reg %d.\n", reg1);
                vm->cpu.registers[reg1] = ~vm->cpu.registers[reg1];
                break;
            case OPCODE_SHR: 
                fprintf(stderr, "SHR reg %d.\n", reg1);
                vm->cpu.registers[reg1] >>= 1;
                break;
            case OPCODE_SHL: 
                fprintf(stderr, "SHL reg %d.\n", reg1);
                vm->cpu.registers[reg1] <<= 1;
                break;

            // SP and BP ops
            case OPCODE_SETSP: 
                fprintf(stderr, "MOV SP <- reg %d\n", reg1);
                vm->cpu.sp = vm->cpu.registers[reg1];
                break;
            case OPCODE_GETSP: 
                fprintf(stderr, "MOV reg %d <- SP\n", reg1);
                vm->cpu.registers[reg1] = vm->cpu.sp;
                break;
            case OPCODE_ADDSP: 
                fprintf(stderr, "ADD SP <- imm %d\n", value);
                vm->cpu.sp = vm->cpu.sp + value;
                break;
            case OPCODE_SUBSP: 
                fprintf(stderr, "SUB SP <- imm %d\n", value);
                vm->cpu.sp = vm->cpu.sp - value;
                break;
            case OPCODE_SETBP: 
                fprintf(stderr, "MOV BP <- reg %d\n", reg1);
                vm->cpu.bp = vm->cpu.registers[reg1];
                break;
            case OPCODE_GETBP: 
                fprintf(stderr, "MOV reg %d <- BP\n", reg1);
                vm->cpu.registers[reg1] = vm->cpu.bp;
                break;
            case OPCODE_ADDBP: 
                fprintf(stderr, "ADD BP <- imm %d\n", value);
                vm->cpu.bp = vm->cpu.bp + value;
                break;
            case OPCODE_SUBBP: 
                fprintf(stderr, "SUB BP <- imm %d\n", value);
                vm->cpu.bp = vm->cpu.bp - value;
                break;

            default:
                fprintf(stderr, "UNKNOWN OPCODE: %X! Halting.\n", opcode);
                return;

        }
        if (vm->cpu.pc >= HEAP_ADDRESS) {
            fprintf(stderr, "PC is outside program space! Halting.\n");
            return;
        }
        // dump_cpu(&vm->cpu);
        dump_vm(vm);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Program file not specified!\n");
        return 1;
    }

    char *program_path = argv[1];
    VM vm;
    init_vm(&vm);

    // // loop and output test
    // uint8_t program[] = {
    //     0x0C, // MOVI
    //     0b00000000, 
    //     0x0F, 0x00, 
    //     0x0B, // MOVR
    //     0b00010000,
    //     0x15, // ADDI
    //     0b00010000,
    //     48, 0x00,
    //     0x0D, // STORDR
    //     0b00010000,
    //     0x01, 0xFF,
    //     0x19, // DEC
    //     0b00000000,
    //     0x06, // JNZ
    //     0x04, 0x00, 
    //     0x01 // HLT
    // };
    // memcpy(vm.memory, program, sizeof(program));

    if (exec_load_program(&vm, program_path) == -1) {
        return 1;
    }
    
    dump_vm(&vm);
    run_vm(&vm);
    dump_vm(&vm);
    
    printf("\n");
    return 0;
}