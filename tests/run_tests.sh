#!/bin/sh
TEST_DIR=$(dirname "$0")
ASM="python3 ../asm.py"
VM="../build/akvm"
PASS=0
FAIL=0

for t in "$TEST_DIR"/*/ ; do
    name=$(basename "$t")
    echo "Test: $name"
    # Assemble
    $ASM "$t/$name.asm" -o "$t/$name.bin" -f bin || { echo "  ASSEMBLY FAIL"; FAIL=$((FAIL+1)); continue; }
    # Run VM, capture output
    $VM "$t/$name.bin" -t > "$t/output.actual" 2>&1
    # Remove binary 
    rm "$t/$name.bin"
    # Compare
    if diff -u "$t/output.expected" "$t/output.actual" > "$t/diff.txt"; then
        echo "  PASS"
        PASS=$((PASS+1))
        rm "$t/output.actual" "$t/diff.txt"
    else
        echo "  FAIL (diff in $t/diff.txt)"
        FAIL=$((FAIL+1))
    fi
done
echo "Passed: $PASS, Failed: $FAIL"