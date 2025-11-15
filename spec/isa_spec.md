# Custom 16-bit ISA Specification

## Architecture Overview

- **Word size**: 16 bits
- **Memory**: Byte-addressable, word-aligned
- **Registers**: 8 general-purpose registers (R0-R7), 3-bit encoding
- **Program Counter**: 16-bit
- **Status Flags**: Z (zero), N (negative), C (carry)

## Instruction Formats

### R-type (Register) - 16 bits
```
[opcode:4][rd:3][rs1:3][rs2:3][unused:3]
```
Used for: ADD, SUB, AND, OR

### I-type (Immediate) - 16 bits
```
[opcode:4][rd:3][rs:3][imm6:6]
```
Used for: ADDI (imm6 is sign-extended to 16 bits)

### J-type (Jump/Branch) - 16 bits
```
[opcode:4][cond:2][offset10:10]
```
Used for: JMP, BRZ (offset10 is sign-extended to 16 bits)

### M-type (Memory) - 16 bits
```
[opcode:4][rd:3][base:3][offset6:6]
```
Used for: LOAD, STORE (offset6 is sign-extended to 16 bits)

## Opcode Table

| Opcode | Mnemonic | Type | Description |
|--------|----------|------|-------------|
| 0000   | NOP      | -    | No operation |
| 0001   | ADD      | R    | rd = rs1 + rs2 |
| 0010   | SUB      | R    | rd = rs1 - rs2 |
| 0011   | AND      | R    | rd = rs1 & rs2 |
| 0100   | OR       | R    | rd = rs1 \| rs2 |
| 0101   | ADDI     | I    | rd = rs + imm6 |
| 0110   | LOAD     | M    | rd = MEM[base + offset6] |
| 0111   | STORE    | M    | MEM[base + offset6] = rd |
| 1000   | JMP      | J    | PC = PC + offset10 |
| 1001   | BRZ      | J    | if (Z flag) PC = PC + offset10 |
| 1010   | HALT     | -    | Stop execution |

## Instruction Encoding Examples

### ADD R1, R2, R3
```
0001 001 010 011 000
op   rd  rs1 rs2 unused
```

### ADDI R1, R2, 5
```
0101 001 010 000101
op   rd  rs  imm6
```

### LOAD R1, R2, 4
```
0110 001 010 000100
op   rd  base offset6
```

### JMP 100
```
1000 00 0001100100
op   cond offset10
```

## Status Flags

- **Z (Zero)**: Set when result is zero
- **N (Negative)**: Set when result is negative (MSB = 1)
- **C (Carry)**: Set when arithmetic operation overflows

## Memory Model

- Memory is byte-addressable
- Words are 16 bits (2 bytes)
- Load/store operations are word-aligned
- Address space: 0x0000 - 0xFFFF (64KB)

## Register Conventions

- **R0**: Often used as zero register (always reads as 0)
- **R1-R6**: General purpose
- **R7**: Stack pointer (convention)

