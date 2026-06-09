# 8-Bit Breadboard Computer Assembler

An assembler for a custom 8-bit breadboard computer. Takes assembly source code and produces binary ROM images that can be flashed to AT28C256 EEPROMs using a TL866II+ programmer.

## Instruction Set

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x00 | NOP | No operation |
| 0x01 | LDA addr | Load RAM[addr] into A |
| 0x02 | STA addr | Store A into RAM[addr] |
| 0x03 | LDIA val | Load immediate value into A |
| 0x04 | LDIB val | Load immediate value into B |
| 0x05 | MOVAB | Copy B into A |
| 0x06 | MOVBA | Copy A into B |
| 0x07 | LDB addr | Load RAM[addr] into B |
| 0x08 | STB addr | Store B into RAM[addr] |
| 0x09 | ADD addr | Store A + B into RAM[addr] |
| 0x0A | SUB addr | Store A - B into RAM[addr] |
| 0x0B | JMP addr | Jump to addr |
| 0x0C | JZ addr | Jump to addr if zero flag set |
| 0x0D | JNZ addr | Jump to addr if zero flag not set |
| 0x0E | OUT | Output A to display |
| 0x0F | HLT | Halt the clock |

## Assembly Syntax

- Instructions are space-separated: `LDA 0x0F`
- One instruction per line
- Operands can be decimal (`10`), hex (`0xFF`), or binary (`0b1010`)

### Example Program

```
LDIA 10
LDIB 1
SUB 0x0F
STA 0x0F
LDA 0x0F
OUT
JZ 0x0E
LDIA 0
LDA 0x0F
LDIB 1
SUB 0x0F
STA 0x0F
JMP 0x04
NOP
HLT
```

## Architecture

The assembler pipeline has three stages:

```
Source text --> Lexer --> Tokens --> Parser --> Instruction List --> Assembler --> ROM binaries
```

- **Lexer** (`lexer.py`) - Tokenizes source text into `OPCODE` and `NUMBER` tokens
- **Parser** (`parser.py`) - Validates token order and builds a linked list of instructions
- **Assembler** (`assembler.py`) - Encodes instructions and outputs two binary files

## ROM Layout

Instructions are 16 bits wide. The ROM is implemented using two AT28C256 EEPROMs in parallel:

- **Upper EEPROM** (`_upper.bin`) - Stores the opcode byte (upper 4 bits unused, lower 4 bits are the opcode)
- **Lower EEPROM** (`_lower.bin`) - Stores the operand byte (0x00 for instructions with no operand)

Both files are zero-padded to 32,768 bytes (full EEPROM size).

## Flashing to EEPROM

Uses `minipro` with a TL866II+ programmer:

```bash
minipro -p "AT28C256" -w output_upper.bin
minipro -p "AT28C256" -w output_lower.bin
```

## Running Tests

```bash
pytest -v
```
