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

Assembler translates code line-by-line. Each line can be empty or can contain following parts: label, instruction/directive and comment.

### Labels
Label is `identifier + ":"`. 

Examples: `start:`, `loop:`, `_init_42:`.

### Instructions
Instruction consists of mnemonic + operands. Depending on instruction, it can have one or two operands.

Operand types:
Syntax          | Name
----------------|-----------------
`R0-R15`        | Register
`expression`    | Immediate
`[R0-R15]`      | Memory indirect
`[expression]`  | Memory direct

Examples: `MOV R0, 42`, `PUSH R3`, `STOR R3, [R0]`

### Directives

#### .DB
Emits bytes into binary. Syntax: `.DB expression, {" , " expression}`. 

Examples: `.DB 0`, `.DB 2+3, ADDRESS + 10, 33, 0`

#### .STR
Emits zero-terminated string into binary. Syntax: `.STR "string"`

Examples: `.STR "Hello world!"`

#### .DEF
Defines a constant (assembler-time). Doesn't affect binary. Syntax: `.DEF identifier value`

Examples: `.DEF OUTPUT_ADDRESS 0xF801`, `.DEF A 48`

### Comments
Comments are ignored. They start with ";" and extend to the end of line. Syntax: `; comment`

Examples: `; this line does something`

### Identifiers
Identifiers start with latin letter [aA-zZ] or lowercase "\_" and can contain latin letters [aA-zZ], numbers [0-9] and lowercase "\_". They are case-sensitive.

Examples: `A`, `start`, `_init_42`, `fn32`

### Expressions
Expressions consist of expression operands and operators. They can be complex and contain sub-expressions.

Supported operators:
Symbol | Name              | Priority
-------|-------------------|-------------------------------------
`!`    | Logical NOT       | 0
`*`    | Multiply          | 1
`/`    | Divide            | 1
`+`    | Add               | 2
`-`    | Subtract          | 2
`<<`   | Shift left        | 3
`>>`   | Shift right       | 3
`^`    | Bitwise XOR       | 4
`>`    | Greater than      | 5
`<`    | Less than         | 5
`>=`   | Greater or equal  | 5
`<=`   | Less or equal     | 5
`==`   | Equal             | 6
`!=`   | Not equal         | 6
`&`    | Bitwise AND       | 7
`\|`    | Bitwise OR        | 7

Examples: `2 + 2`, `A + 2`, `2 * (1 + 42)`, `(A | B) & DEBUG`


## EBNF grammar
```
line        = [label] [instruction | directive] [comment]

label       = ident , ":" ; (*e.g. start:*)
instruction = mnemonic , operand , {', ' , operand}
directive   = ".DB" | ".STR" | ".DEF" , arguments
```