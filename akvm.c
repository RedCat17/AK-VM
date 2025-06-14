#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define REG_COUNT 16
#define MEMORY_SIZE 0x10000

#define RAM_ADDRESS 0x4000
#define STACK_ADDRESS 0xDEFF
#define VRAM_ADDRESS 0xDF00
#define IO_ADDRESS 0xFF00

#define RX_ADDRESS 0xFF00
#define TX_ADDRESS 0xFF01
#define IO_STATUS_ADDRESS 0xFF02
#define REFRESH_SCREEN_ADDRESS 0xFF03

#define ZERO_FLAG 0b10000000
#define CARRY_FLAG 0b01000000
#define SIGN_FLAG 0b00100000
// WIP

#define REG1 0b11110000
#define REG2 0b00001111

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
    [0x00] = {"NOP", FORMAT_NONE},
    [0x01] = {"HLT", FORMAT_NONE},
    [0x02] = {"CMPRR", FORMAT_REG_REG},
    [0x03] = {"CMPRI", FORMAT_REG_IMM},
    [0x04] = {"JMP", FORMAT_IMM},
    [0x05] = {"JMZ", FORMAT_IMM},
    [0x06] = {"JNZ", FORMAT_IMM},
    [0x07] = {"JMC", FORMAT_IMM},
    [0x08] = {"JMS", FORMAT_IMM},
    [0x09] = {"CALL", FORMAT_IMM},
    [0x0A] = {"RET", FORMAT_NONE},
    // Memory
    [0x0B] = {"MOVRR", FORMAT_REG_REG},
    [0x0C] = {"MOVRI", FORMAT_REG_IMM},
    [0x0D] = {"STORDR", FORMAT_REG_IMM}, // STORDI not included as it would require 2 immediate values
    [0x0E] = {"STORMI", FORMAT_REG_IMM}, 
    [0x0F] = {"STORMR", FORMAT_REG_REG},
    [0x10] = {"LOADRD", FORMAT_REG_IMM},
    [0x11] = {"LOADRM", FORMAT_REG_REG},
    [0x12] = {"PUSHR", FORMAT_REG},
    [0x13] = {"POPR", FORMAT_REG},
    // Arithmetics
    [0x14] = {"ADDRR", FORMAT_REG_REG},
    [0x15] = {"ADDRI", FORMAT_REG_IMM},
    [0x16] = {"SUBRR", FORMAT_REG_REG},
    [0x17] = {"SUBRI", FORMAT_REG_IMM},
    [0x18] = {"INCR", FORMAT_REG},
    [0x19] = {"DECR", FORMAT_REG},
    [0x1A] = {"MULRR", FORMAT_REG_REG},
    [0x1B] = {"MULRI", FORMAT_REG_IMM},
    [0x1C] = {"DIVRR", FORMAT_REG_REG},
    [0x1D] = {"DIVRI", FORMAT_REG_IMM},
    // Bit ops
    [0x1E] = {"ANDRR", FORMAT_REG_REG},
    [0x1F] = {"ANDRI", FORMAT_REG_IMM},
    [0x20] = {"ORRR", FORMAT_REG_REG},
    [0x21] = {"ORRI", FORMAT_REG_IMM},
    [0x22] = {"XORRR", FORMAT_REG_REG},
    [0x23] = {"XORRI", FORMAT_REG_IMM},
    [0x24] = {"NOTR", FORMAT_REG},
    [0x25] = {"SHRR", FORMAT_REG},
    [0x26] = {"SHLR", FORMAT_REG},
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
        fprintf(stderr, "Printing %c (ASCII %d)", value, value);
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
            case 0x00: // NOP
                fprintf(stderr, "NOP...\n");
                break;
            case 0x01: // HLT
                fprintf(stderr, "Halting.\n");
                return;
            case 0x02: // CMPRR
                fprintf(stderr, "CMP reg %d reg %d\n", reg1, reg2);
                sub(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                break;
            case 0x03: // CMPRI
                fprintf(stderr, "CMP reg %d imm %d\n", reg1, value);
                sub(&vm->cpu, vm->cpu.registers[reg1], value);
                break;
            case 0x04: // JMP
                fprintf(stderr, "JMP adr %X\n", value);
                vm->cpu.pc = value;
                break;
            case 0x05: // JMZ
                fprintf(stderr, "JMZ adr %X\n", value);
                if (vm->cpu.flags & ZERO_FLAG) {
                    fprintf(stderr, "jumped\n");
                    vm->cpu.pc = value;
                }
                break;
            case 0x06: // JNZ
                fprintf(stderr, "JNZ adr %X\n", value);
                if (!(vm->cpu.flags & ZERO_FLAG)) {
                    fprintf(stderr, "jumped\n");
                    vm->cpu.pc = value;
                }
                break;
            case 0x07: // JMC
                fprintf(stderr, "JMC adr %X\n", value);
                if (vm->cpu.flags & CARRY_FLAG) {
                    fprintf(stderr, "jumped\n");
                    vm->cpu.pc = value;
                }
                break;
            case 0x08: // JMS
                fprintf(stderr, "JMC adr %X\n", value);
                if (vm->cpu.flags & SIGN_FLAG) {
                    fprintf(stderr, "jumped\n");
                    vm->cpu.pc = value;
                }
                break;
            case 0x09: // CALL
                fprintf(stderr, "CALL adr %X\n", value);
                exec_call(vm, value);
                break;
            case 0x0A: // RET
                fprintf(stderr, "RET\n");
                exec_ret(vm);
                break;

            // Memory
            case 0x0B: // MOVRR
                fprintf(stderr, "MOV reg %d <- reg %d\n", reg1, reg2);
                vm->cpu.registers[reg1] = vm->cpu.registers[reg2];
                break;
            case 0x0C: // MOVRI
                fprintf(stderr, "MOV reg %d <- imm %d\n", reg1, value);
                vm->cpu.registers[reg1] = value;
                break;
            case 0x0D: // STORDR
                fprintf(stderr, "STOR adr %X <- reg %d\n", value, reg1);
                exec_stor(vm, value, vm->cpu.registers[reg1]);
                break;
            case 0x0E: // STORMI
                fprintf(stderr, "STOR ind %d <- imm %d\n", reg1, value);
                exec_stor(vm, vm->cpu.registers[reg1], value);
                break;
            case 0x0F: // STORMR
                fprintf(stderr, "STOR ind %d <- reg2 %d\n", reg1, reg2);
                exec_stor(vm, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                break;
            case 0x10: // LOADRD
                fprintf(stderr, "LOAD reg %d <- adr %X\n", value, reg1);
                exec_load(vm, reg1, value);
                break;
            case 0x11: // LOADRM
                fprintf(stderr, "LOAD reg %d <- ind %d\n", reg1, reg2);
                exec_load(vm, reg1, vm->cpu.registers[reg2]);
                break;
            case 0x12: // PUSHR
                fprintf(stderr, "PUSH reg %d\n", reg1);
                exec_push(vm, vm->cpu.registers[reg1]);
                break;
            case 0x13: // POPR
                fprintf(stderr, "POP to reg %d\n", reg1);
                exec_pop(vm, reg1);
                break;

            // Arithmetics
            case 0x14: // ADDRR
                fprintf(stderr, "ADD reg %d <- reg %d\n", reg1, reg2);
                result = add(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                vm->cpu.registers[reg1] = result;
                break;
            case 0x15: // ADDRI
                fprintf(stderr, "ADD reg %d <- imm %d\n", reg1, value);
                result = add(&vm->cpu, vm->cpu.registers[reg1], value);
                vm->cpu.registers[reg1] = result;
                break;
            case 0x16: // SUBRR
                fprintf(stderr, "SUB reg %d <- reg %d\n", reg1, reg2);
                result = sub(&vm->cpu, vm->cpu.registers[reg1], vm->cpu.registers[reg2]);
                vm->cpu.registers[reg1] = result;
                break;
            case 0x17: // SUBRI
                fprintf(stderr, "SUB reg %d <- imm %d\n", reg1, value);
                result = sub(&vm->cpu, vm->cpu.registers[reg1], value);
                vm->cpu.registers[reg1] = result;
                break;
            case 0x18: // INCR
                fprintf(stderr, "INC reg %d\n", reg1);
                result = add(&vm->cpu, reg1, 1);
                vm->cpu.registers[reg1] = result;
                break;
            case 0x19: // DECR
                fprintf(stderr, "DEC reg %d\n", reg1);
                result = sub(&vm->cpu, vm->cpu.registers[reg1], 1);
                vm->cpu.registers[reg1] = result;
                break;
            case 0x1A: // MULRR
                fprintf(stderr, "NOT IMPLEMENTED! Halting.\n");
                return;
            case 0x1B: // MULRI
                fprintf(stderr, "NOT IMPLEMENTED! Halting.\n");
                return;
            case 0x1C: // DIVRR
                fprintf(stderr, "NOT IMPLEMENTED! Halting.\n");
                return;
            case 0x1D: // DIVRI
                fprintf(stderr, "NOT IMPLEMENTED! Halting.\n");
                return;

            // Bit ops
            case 0x1E: // ANDRR
                fprintf(stderr, "AND reg %d reg %d.\n", reg1, reg2);
                vm->cpu.registers[reg1] &= vm->cpu.registers[reg2];
                break;
            case 0x1F: // ANDRI
                fprintf(stderr, "AND reg %d imm %d.\n", value, reg1);
                vm->cpu.registers[reg1] &= value;
                break;
            case 0x20: // ORRR
                fprintf(stderr, "OR reg %d reg %d.\n", reg1, reg2);
                vm->cpu.registers[reg1] |= vm->cpu.registers[reg2];
                break;
            case 0x21: // ORRI
                fprintf(stderr, "OR reg %d imm %d.\n", value, reg1);
                vm->cpu.registers[reg1] |= value;
                break;
            case 0x22: // XORRR
                fprintf(stderr, "XOR reg %d reg %d.\n", reg1, reg2);
                vm->cpu.registers[reg1] ^= vm->cpu.registers[reg2];
                break;
            case 0x23: // XORRI
                fprintf(stderr, "XOR reg %d imm %d.\n", value, reg1);
                vm->cpu.registers[reg1] ^= value;
                break;
            case 0x24: // NOTR
                fprintf(stderr, "NOT reg %d.\n", reg1);
                vm->cpu.registers[reg1] = ~vm->cpu.registers[reg1];
                break;
            case 0x25: // SHRR
                fprintf(stderr, "SHR reg %d.\n", reg1);
                vm->cpu.registers[reg1] >>= 1;
                break;
            case 0x26: // SHLR
                fprintf(stderr, "SHL reg %d.\n", reg1);
                vm->cpu.registers[reg1] <<= 1;
                break;

            default:
                fprintf(stderr, "UNKNOWN OPCODE! Halting.\n");
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
        fprintf(stderr, "Program file not specified!");
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

    run_vm(&vm);
    dump_vm(&vm);
    
    printf("\n");
    return 0;
}