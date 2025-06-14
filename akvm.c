#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define REG_COUNT 16
#define MEMORY_SIZE 0x10000

#define RAM_ADDRESS      0x4000
#define STACK_ADDRESS    0xDEFF
#define VRAM_ADDRESS     0xDF00
#define IO_ADDRESS       0xFF00

#define RX_ADDRESS              0xFF00
#define TX_ADDRESS              0xFF01
#define IO_STATUS_ADDRESS       0xFF02
#define REFRESH_SCREEN_ADDRESS  0xFF03

#define ZERO_FLAG  0b10000000
#define CARRY_FLAG 0b01000000
#define SIGN_FLAG  0b00100000
// WIP

#define REG1 0b11110000
#define REG2 0b00001111

// Control flow
#define OPCODE_NOP     0x00
#define OPCODE_HLT     0x01
#define OPCODE_CMPRR   0x02
#define OPCODE_CMPRI   0x03
#define OPCODE_JMP     0x04
#define OPCODE_JMZ     0x05
#define OPCODE_JNZ     0x06
#define OPCODE_JMC     0x07
#define OPCODE_JMS     0x08
#define OPCODE_CALL    0x09
#define OPCODE_RET     0x0A

// Memory
#define OPCODE_MOVRR   0x10
#define OPCODE_MOVRI   0x11
#define OPCODE_STORDR  0x12
#define OPCODE_STORMI  0x13
#define OPCODE_STORMR  0x14
#define OPCODE_LOADRD  0x15
#define OPCODE_LOADRM  0x16
#define OPCODE_PUSHR   0x17
#define OPCODE_POPR    0x18
#define OPCODE_STORBDR  0x19
#define OPCODE_STORBMI  0x1A
#define OPCODE_STORBMR  0x1B
#define OPCODE_LOADBRD  0x1C
#define OPCODE_LOADBRM  0x1D

// Arithmetics
#define OPCODE_ADDRR   0x20
#define OPCODE_ADDRI   0x21
#define OPCODE_SUBRR   0x22
#define OPCODE_SUBRI   0x23
#define OPCODE_INCR    0x24
#define OPCODE_DECR    0x25
#define OPCODE_MULRR   0x26
#define OPCODE_MULRI   0x27
#define OPCODE_DIVRR   0x28
#define OPCODE_DIVRI   0x29

// Bit ops
#define OPCODE_ANDRR   0x30
#define OPCODE_ANDRI   0x31
#define OPCODE_ORRR    0x32
#define OPCODE_ORRI    0x33
#define OPCODE_XORRR   0x34
#define OPCODE_XORRI   0x35
#define OPCODE_NOTR    0x36
#define OPCODE_SHRR    0x37
#define OPCODE_SHLR    0x38

typedef enum {
    FORMAT_NONE,
    FORMAT_REG,
    FORMAT_REG_REG, 
    FORMAT_IMM, // can be either immediate or address
    FORMAT_REG_IMM, 
} EncodingFormat;

typedef struct {
    const char *name;
    EncodingFormat format;
} OpcodeData;

OpcodeData opcode_table[256] = {
    // Control flow
    [OPCODE_NOP]   = {"NOP",   FORMAT_NONE},
    [OPCODE_HLT]   = {"HLT",   FORMAT_NONE},
    [OPCODE_CMPRR] = {"CMPRR", FORMAT_REG_REG},
    [OPCODE_CMPRI] = {"CMPRI", FORMAT_REG_IMM},
    [OPCODE_JMP]   = {"JMP",   FORMAT_IMM},
    [OPCODE_JMZ]   = {"JMZ",   FORMAT_IMM},
    [OPCODE_JNZ]   = {"JNZ",   FORMAT_IMM},
    [OPCODE_JMC]   = {"JMC",   FORMAT_IMM},
    [OPCODE_JMS]   = {"JMS",   FORMAT_IMM},
    [OPCODE_CALL]  = {"CALL",  FORMAT_IMM},
    [OPCODE_RET]   = {"RET",   FORMAT_NONE},
    // Memory
    [OPCODE_MOVRR]  = {"MOVRR",  FORMAT_REG_REG},
    [OPCODE_MOVRI]  = {"MOVRI",  FORMAT_REG_IMM},
    [OPCODE_STORDR] = {"STORDR", FORMAT_REG_IMM},  // STORDI not included as it would require 2 immediate values
    [OPCODE_STORMI] = {"STORMI", FORMAT_REG_IMM},
    [OPCODE_STORMR] = {"STORMR", FORMAT_REG_REG},
    [OPCODE_LOADRD] = {"LOADRD", FORMAT_REG_IMM},
    [OPCODE_LOADRM] = {"LOADRM", FORMAT_REG_REG},
    [OPCODE_PUSHR]  = {"PUSHR",  FORMAT_REG},
    [OPCODE_POPR]   = {"POPR",   FORMAT_REG},
    [OPCODE_STORBDR] = {"STORBDR", FORMAT_REG_IMM},
    [OPCODE_STORBMI] = {"STORBMI", FORMAT_REG_IMM},
    [OPCODE_STORBMR] = {"STORBMR", FORMAT_REG_REG},
    [OPCODE_LOADBRD] = {"LOADBRD", FORMAT_REG_IMM},
    [OPCODE_LOADBRM] = {"LOADBRM", FORMAT_REG_REG},
    // Arithmetics
    [OPCODE_ADDRR]  = {"ADDRR",  FORMAT_REG_REG},
    [OPCODE_ADDRI]  = {"ADDRI",  FORMAT_REG_IMM},
    [OPCODE_SUBRR]  = {"SUBRR",  FORMAT_REG_REG},
    [OPCODE_SUBRI]  = {"SUBRI",  FORMAT_REG_IMM},
    [OPCODE_INCR]   = {"INCR",   FORMAT_REG},
    [OPCODE_DECR]   = {"DECR",   FORMAT_REG},
    [OPCODE_MULRR]  = {"MULRR",  FORMAT_REG_REG},
    [OPCODE_MULRI]  = {"MULRI",  FORMAT_REG_IMM},
    [OPCODE_DIVRR]  = {"DIVRR",  FORMAT_REG_REG},
    [OPCODE_DIVRI]  = {"DIVRI",  FORMAT_REG_IMM},

    // Bit ops
    [OPCODE_ANDRR]  = {"ANDRR",  FORMAT_REG_REG},
    [OPCODE_ANDRI]  = {"ANDRI",  FORMAT_REG_IMM},
    [OPCODE_ORRR]   = {"ORRR",   FORMAT_REG_REG},
    [OPCODE_ORRI]   = {"ORRI",   FORMAT_REG_IMM},
    [OPCODE_XORRR]  = {"XORRR",  FORMAT_REG_REG},
    [OPCODE_XORRI]  = {"XORRI",  FORMAT_REG_IMM},
    [OPCODE_NOTR]   = {"NOTR",   FORMAT_REG},
    [OPCODE_SHRR]   = {"SHRR",   FORMAT_REG},
    [OPCODE_SHLR]   = {"SHLR",   FORMAT_REG},
};

typedef struct {
    uint16_t registers[REG_COUNT];
    uint16_t pc, sp;
    uint8_t flags;
} CPU;

typedef struct {
    CPU cpu;
    uint8_t memory[MEMORY_SIZE]; // 64 KB RAM
} VM;

// initialize CPU, set all registers to zero
void init_cpu(CPU *cpu) {
    memset(cpu->registers, 0, sizeof(cpu->registers));
    cpu->pc = 0; 
    cpu->sp = STACK_ADDRESS;
    cpu->flags = 0;
}

// initialize whole VM, reset CPU and memory
void init_vm(VM *vm) {
    init_cpu(&vm->cpu);
    memset(vm->memory, 0, sizeof(vm->memory));
}

int exec_load_program(VM *vm, const char *filename) {
    FILE *file = fopen(filename, "rb");

    if (!file) {
        perror("Failed to open progam file");
        return -1;
    }

    int byte = fgetc(file);
    int i = 0;
    while (byte != EOF && i < sizeof(vm->memory)) {
        vm->memory[i++] = byte;
        byte = fgetc(file);
    }
    fclose(file);
    return 0;
}

// dump CPU state to console
void dump_cpu(CPU *cpu) {
    fprintf(stderr, "PC: %X; SP: %X; Flags: %d;\n", cpu->pc, cpu->sp, cpu->flags);
    fprintf(stderr, "Registers: ");
    for (uint8_t i = 0; i < REG_COUNT; i++) {
        fprintf(stderr, "%d ", cpu->registers[i]);
    }
    fprintf(stderr, "\n");
}

// dump VM state to console
void dump_vm(VM *vm) {
    dump_cpu(&vm->cpu);
    fprintf(stderr, "\nProgram space: ");
    for (int i = 0; i < 1024; i++) {
        fprintf(stderr, "%d ", vm->memory[i]);
    }
    fprintf(stderr, "\nRAM: ");
    for (int i = 0; i < 1024; i++) {
        fprintf(stderr, "%d ", vm->memory[RAM_ADDRESS + i]);
    }    
    fprintf(stderr, "\n");
}

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

uint16_t add(CPU *cpu, uint16_t value1, uint16_t value2) {
    uint16_t result = value1 + value2;
    set_flags_add(cpu, value1, value2, result);
    return result;
}

uint16_t sub(CPU *cpu, uint16_t value1, uint16_t value2) {
    uint16_t result = value1 - value2;
    set_flags_sub(cpu, value1, value2, result);
    return result;
}

uint16_t mul(CPU *cpu, uint16_t value1, uint16_t value2) {
    uint16_t result = value1 * value2;
    set_flags_add(cpu, value1, value2, result);
    return result;
}

uint16_t div(CPU *cpu, uint16_t value1, uint16_t value2) {
    uint16_t result = value1 / value2;
    set_flags_add(cpu, value1, value2, result);
    return result;
}

int exec_stor(VM *vm, uint16_t address, uint16_t value) {
    if (address < RAM_ADDRESS) {
        fprintf(stderr, "Segfault! Can't write into program space.\n");
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
    if (address < RAM_ADDRESS) {
        fprintf(stderr, "Segfault! Can't write into program space.\n");
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
    if (vm->cpu.sp > STACK_ADDRESS) {
        fprintf(stderr, "Stack underflow!\n");
        return -1;
    }
    vm->memory[vm->cpu.sp--] = value & 0x00FF;
    vm->memory[vm->cpu.sp--] = (value & 0xFF00) >> 8;
    return 0;
}

int exec_pop(VM *vm, uint8_t reg) {
    if (vm->cpu.sp > STACK_ADDRESS) {
        fprintf(stderr, "Stack underflow!\n");
        return -1;
    }
    vm->cpu.registers[reg] = vm->memory[++vm->cpu.sp] | (vm->memory[++vm->cpu.sp] << 8) ;
    return 0;
}

int exec_call(VM *vm, uint16_t address) {
    if (vm->cpu.sp > STACK_ADDRESS) {
        fprintf(stderr, "Stack underflow!\n");
        return -1;
    }
    vm->memory[vm->cpu.sp--] = vm->cpu.pc & 0x00FF;
    vm->memory[vm->cpu.sp--] = (vm->cpu.pc & 0xFF00) >> 8;
    vm->cpu.pc = address;
    return 0;
}

int exec_ret(VM *vm) {
    if (vm->cpu.sp > STACK_ADDRESS) {
        fprintf(stderr, "Stack underflow!\n");
        return -1;
    }
    vm->cpu.pc = vm->memory[++vm->cpu.sp] | (vm->memory[++vm->cpu.sp] << 8) ;
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
            case OPCODE_CMPRR: 
                fprintf(stderr, "CMP reg %d reg %d\n", reg1, reg2);
                sub(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                break;
            case OPCODE_CMPRI: 
                fprintf(stderr, "CMP reg %d imm %d\n", reg1, value);
                sub(&vm->cpu, vm->cpu.registers[reg1], value);
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
            case OPCODE_JMC: 
                fprintf(stderr, "JMC adr %X\n", value);
                if (vm->cpu.flags & CARRY_FLAG) {
                    fprintf(stderr, "jumped\n");
                    vm->cpu.pc = value;
                }
                break;
            case OPCODE_JMS: 
                fprintf(stderr, "JMC adr %X\n", value);
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
            case OPCODE_MOVRR: 
                fprintf(stderr, "MOV reg %d <- reg %d\n", reg1, reg2);
                vm->cpu.registers[reg1] = vm->cpu.registers[reg2];
                break;
            case OPCODE_MOVRI: 
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
            case OPCODE_PUSHR: 
                fprintf(stderr, "PUSH reg %d\n", reg1);
                exec_push(vm, vm->cpu.registers[reg1]);
                break;
            case OPCODE_POPR: 
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
            case OPCODE_ADDRR: 
                fprintf(stderr, "ADD reg %d <- reg %d\n", reg1, reg2);
                result = add(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_ADDRI: 
                fprintf(stderr, "ADD reg %d <- imm %d\n", reg1, value);
                result = add(&vm->cpu, vm->cpu.registers[reg1], value);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_SUBRR: 
                fprintf(stderr, "SUB reg %d <- reg %d\n", reg1, reg2);
                result = sub(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_SUBRI: 
                fprintf(stderr, "SUB reg %d <- imm %d\n", reg1, value);
                result = sub(&vm->cpu, vm->cpu.registers[reg1], value);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_INCR: 
                fprintf(stderr, "INC reg %d\n", reg1);
                result = add(&vm->cpu, vm->cpu.registers[reg1], 1);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_DECR: 
                fprintf(stderr, "DEC reg %d\n", reg1);
                result = sub(&vm->cpu, vm->cpu.registers[reg1], 1);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_MULRR: 
                fprintf(stderr, "MUL reg %d <- reg %d\n", reg1, reg2);
                result = mul(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_MULRI: 
                fprintf(stderr, "MUL reg %d <- imm %d\n", reg1, value);
                result = mul(&vm->cpu, vm->cpu.registers[reg1], value);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_DIVRR: 
                fprintf(stderr, "DIV reg %d <- reg %d\n", reg1, reg2);
                result = div(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                vm->cpu.registers[reg1] = result;
                break;
            case OPCODE_DIVRI: 
                fprintf(stderr, "DIV reg %d <- imm %d\n", reg1, value);
                result = div(&vm->cpu, vm->cpu.registers[reg1], value);
                vm->cpu.registers[reg1] = result;
                break;

            // Bit ops
            case OPCODE_ANDRR:
                fprintf(stderr, "AND reg %d reg %d.\n", reg1, reg2);
                vm->cpu.registers[reg1] &= vm->cpu.registers[reg2];
                break;
            case OPCODE_ANDRI: 
                fprintf(stderr, "AND reg %d imm %d.\n", value, reg1);
                vm->cpu.registers[reg1] &= value;
                break;
            case OPCODE_ORRR: 
                fprintf(stderr, "OR reg %d reg %d.\n", reg1, reg2);
                vm->cpu.registers[reg1] |= vm->cpu.registers[reg2];
                break;
            case OPCODE_ORRI: 
                fprintf(stderr, "OR reg %d imm %d.\n", value, reg1);
                vm->cpu.registers[reg1] |= value;
                break;
            case OPCODE_XORRR: 
                fprintf(stderr, "XOR reg %d reg %d.\n", reg1, reg2);
                vm->cpu.registers[reg1] ^= vm->cpu.registers[reg2];
                break;
            case OPCODE_XORRI: 
                fprintf(stderr, "XOR reg %d imm %d.\n", value, reg1);
                vm->cpu.registers[reg1] ^= value;
                break;
            case OPCODE_NOTR: 
                fprintf(stderr, "NOT reg %d.\n", reg1);
                vm->cpu.registers[reg1] = ~vm->cpu.registers[reg1];
                break;
            case OPCODE_SHRR: 
                fprintf(stderr, "SHR reg %d.\n", reg1);
                vm->cpu.registers[reg1] >>= 1;
                break;
            case OPCODE_SHLR: 
                fprintf(stderr, "SHL reg %d.\n", reg1);
                vm->cpu.registers[reg1] <<= 1;
                break;

            default:
                fprintf(stderr, "UNKNOWN OPCODE: %X! Halting.\n", opcode);
                return;

        }
        if (vm->cpu.pc >= RAM_ADDRESS) {
            fprintf(stderr, "PC is outside program space! Halting.\n");
            return;
        }
        dump_cpu(&vm->cpu);
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
    //     0x0C, // MOVRI
    //     0b00000000, 
    //     0x0F, 0x00, 
    //     0x0B, // MOVRR
    //     0b00010000,
    //     0x15, // ADDRI
    //     0b00010000,
    //     48, 0x00,
    //     0x0D, // STORDR
    //     0b00010000,
    //     0x01, 0xFF,
    //     0x19, // DECR
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