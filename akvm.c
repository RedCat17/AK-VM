#include <stdint.h>
#include <string.h>
#include <stdio.h>

#define REG_COUNT 16

#define STACK_ADRESS 0xDEFF
#define RAM_ADRESS 0x4000

typedef struct {
    uint16_t registers[REG_COUNT];
    uint16_t pc, sp;
    uint8_t flags;
} CPU;

typedef struct {
    CPU cpu;
    uint8_t memory[0x10000];
} VM;

// initialize CPU, set all registers to zero
void init_cpu(CPU *cpu) {
    memset(cpu->registers, 0, sizeof(cpu->registers));
    cpu->pc = 0; 
    cpu->sp = STACK_ADRESS;
    cpu->flags = 0;
}

// initialize whole VM, reset CPU and memory
void init_vm(VM *vm) {
    init_cpu(&vm->cpu);
    memset(vm->memory, 0, sizeof(vm->memory));
}

// dump VM state to console
void dump_vm(VM *vm) {
    printf("PC: %X; SP: %X; Flags: %d;\n", vm->cpu.pc, vm->cpu.sp, vm->cpu.flags);
    printf("Registers: ");
    for (char i = 0; i < REG_COUNT; i++) {
        printf("%d ", vm->cpu.registers[i]);
    }
    printf("\n");
}

// fetch-decode-execute loop
void run_vm(VM *vm) {
    while (1) {
        uint8_t opcode = vm->memory[vm->cpu.pc++];
        uint8_t reg1 = 0, reg2 = 0; uint16_t value = 0;
        if (opcode >= 0x04) { // 2-byte instruction
            uint8_t byte = vm->memory[vm->cpu.pc++];
            reg1 = (byte & 0b11110000) >> 4;
            reg2 = (byte & 0b00001111);
        } 
        if (opcode >= 0x10) { // 4-byte instruction
            value = vm->memory[vm->cpu.pc++] | (vm->memory[vm->cpu.pc++] << 8);
        }
        printf("opcode: %X; reg1: %d; reg2: %d; value: %d\n", opcode, reg1, reg2, value);
        switch (opcode) {
            case 0x00: // NOP
                printf("NOP...\n");
                break;
            case 0x01: // HLT
                printf("Halting.\n");
                return;

            case 0x10: // MOVRI
                printf("Moving immediate %d to register %d.\n", value, reg1);
                vm->cpu.registers[reg1] = value;
                break;


            case 0x02: // RET
                printf("NOT IMPLEMENTED!\n");
                return;
            default:
                printf("UNKNOWN OPCODE!\n");
                return;

        }
        if (vm->cpu.pc >= RAM_ADRESS) {
            printf("PC is outside program space! Halting.\n");
            return;
        }
        dump_vm(vm);
    }
}

int main() {
    VM vm;
    init_vm(&vm);
    dump_vm(&vm);

    // basic program
    uint8_t program[] = {
        0x00, 
        0x10, 
        0b11110000, 
        0xFF, 0x00, 
        0b00000001};
    memcpy(vm.memory, program, sizeof(program));

    run_vm(&vm);
    
    return 0;
}