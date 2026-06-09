# Assembler 

Implemented assembler translated AK-VM assembly to binary files.

Language: Python 3.10+
No external dependencies.

## Features:
- Opcodes resolution;
- Labels;
- Byte and string embedding;
- Macros/constants;
- Expression evaluation;
- Intermediate Representation (IR);
- Listing generation;
- Object file generation;

## Usage

**Usage pattern:**

```bash
asm.py [-h] [-o OUTPUT] [-v] -f {bin,obj} input_file
```


`input_file`
: Path to input source file

`-h, --help`
: Show help message

`-o, --output OUTPUT`
: Path to assembled output file (if not specified, OUTPUT = source + '.bin')

`-v, --verbose`
: Enable verbose output

`-f, --format {bin,obj}`
: Output format (binary or object)

**Usage example:**

```bash
python asm.py examples/hello.asm -o examples/hello.bin -f bin
```
