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

| Argument                 | Description                      |
|--------------------------|----------------------------------|
| `input_file`             | Path to input source file        |
| `-h, --help`             | Show help message                |
| `-o, --output OUTPUT`    | Path to assembled output file<br>(if not specified, OUTPUT = source + '.bin')|
| `-v, --verbose`          | Enable verbose output<br>(IR and listing)|
| `-f, --format {bin,obj}` | Output format (binary or object) |

**Usage example:**

```bash
python asm.py examples/hello.asm -o examples/hello.bin -f bin
```

## Syntax

Assembler translates code line-by-line. Each line be empty or contain label, instruction/directive and comment.

Formally, syntax is following:
```
line        = [label] [instruction | directive] [comment]

label       = ident , ":" ; (*e.g. start:*)
instruction = mnemonic , operand , {', ' , operand}
directive   = ".DB" | ".STR" | ".DEF" , arguments
```