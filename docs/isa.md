
### ISA:

#### Control flow:
```
CMP R R/I - compares and sets flags
JMP label - sets PC to said adress
JZ label - jumps if Z flag is set
JNZ label - jump if not Z
JMC label - jump if not Z
JMS label - jump if not Z
CALL label - saves PC to stack and jumps
RET - retrieves PC from stack
NOP - does nothing
HLT - stops execution
```

#### Memory:
```
MOV R R/I - copies value from src to dst
STOR D/M R/I - stores value from src in memory
LOAD R D/M - loads value from memory to dst
PUSH R - pushes value to stack
POP R - pops value from stack
```

#### Arithmetics:
```
ADD R R/I - adds src to dst
SUB R R/I - subs src from dst
INC R - increments by 1
DEC R - decrements by 1
MUL R R/I
```

#### Bit ops:
```
AND R R/I
OR R R/I
XOR R R/I
NOT R
SHR R
```