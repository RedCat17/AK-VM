# Machine specifications

## Memory layout:
```
[0x0000 - 0x3FFF] - Program Space (16 KB)
[0x4000 - 0xF7FF] - Heap (~44 KB) 
[0xF800 - 0xF8FF] - Mapped I/O (256 bytes)
[0xF900 - 0xFFFF] - Stack (2 KB, grows downward)
```

## I/O:

### Serial I/O (stdin/stdout). 

Blocking I/O (execution pauses until symbol is read or written). 
```
[0xF800] - serial input (RX), read a char;
[0xF801] - serial output (TX), write a char;
[0xF802] - refresh screen trigger;
```