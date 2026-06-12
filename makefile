# Targets: all, clean, test, run

CC = clang
CFLAGS = -Wall -Wextra 
DEV_CFLAGS = -Wall -Wextra -Wpedantic -Werror -std=c99

VM_SRC = akvm.c
VM_BIN = build/akvm

ASSEMBLER = asm.py
PYTHON = python3

all: $(VM_BIN)

$(VM_BIN): $(VM_SRC)
	$(CC) $(CFLAGS) -o $@ $^

dev:
	$(CC) $(DEV_CFLAGS) -o $(VM_BIN) $(VM_SRC)

clean: 
	rm -f $(VM_BIN)
	find . -type f \( -name "*.bin" -o -name "*.actual" -o -name "*.diff.txt" -o -name "*.o" -o -name "*.obj" \) -delete

run: $(VM_BIN)
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make run FILE=test.asm"; \
		exit 1; \
	fi
	$(PYTHON) $(ASSEMBLER) $(FILE) -o build/program.bin -f bin
	./$(VM_BIN) build/program.bin
# 	rm build/program.bin

test: $(VM_BIN)
	@cd tests && ./run_tests.sh

.PHONY: all clean run test
