# Assembler for 16-bit ISA
# Vishanth Dandu

import re
from typing import List, Tuple, Dict, Optional


class AssemblerError(Exception):
    def __init__(self, message: str, line: int = 0):
        self.message = message
        self.line = line
        super().__init__(f"Line {line}: {message}")


class Assembler:
    OPCODES = {
        'NOP': 0x0,
        'ADD': 0x1,
        'SUB': 0x2,
        'AND': 0x3,
        'OR': 0x4,
        'ADDI': 0x5,
        'LOAD': 0x6,
        'STORE': 0x7,
        'JMP': 0x8,
        'BRZ': 0x9,
        'HALT': 0xA,
    }
    
    def __init__(self):
        self.labels: Dict[str, int] = {}
        self.symbols: Dict[str, int] = {}
    
    def parse_register(self, reg_str: str) -> int:
        match = re.match(r'R(\d+)', reg_str.upper())
        if not match:
            raise ValueError(f"Invalid register: {reg_str}")
        reg_num = int(match.group(1))
        if reg_num < 0 or reg_num > 7:
            raise ValueError(f"Register out of range: {reg_str}")
        return reg_num
    
    def parse_immediate(self, imm_str: str) -> int:
        imm_str = imm_str.strip()
        if imm_str.startswith('0x') or imm_str.startswith('0X'):
            return int(imm_str, 16)
        elif imm_str.startswith('#'):
            return int(imm_str[1:], 16) if imm_str[1:].startswith('0x') else int(imm_str[1:])
        return int(imm_str)
    
    def encode_r_type(self, opcode: int, rd: int, rs1: int, rs2: int) -> int:
        return (opcode << 12) | (rd << 9) | (rs1 << 6) | (rs2 << 3)
    
    def encode_i_type(self, opcode: int, rd: int, rs: int, imm: int) -> int:
        imm &= 0x3F
        return (opcode << 12) | (rd << 9) | (rs << 6) | imm
    
    def encode_j_type(self, opcode: int, cond: int, offset: int) -> int:
        offset &= 0x3FF
        return (opcode << 12) | (cond << 10) | offset
    
    def encode_m_type(self, opcode: int, rd: int, base: int, offset: int) -> int:
        offset &= 0x3F
        return (opcode << 12) | (rd << 9) | (base << 6) | offset
    
    def preprocess(self, source: str) -> List[Tuple[int, str, Optional[str]]]:
        lines = []
        current_address = 0
        
        for line_num, line in enumerate(source.split('\n'), 1):
            line = line.split(';')[0].strip()
            if not line:
                continue
            
            label = None
            if ':' in line:
                parts = line.split(':', 1)
                label = parts[0].strip()
                line = parts[1].strip()
                self.labels[label] = current_address
            
            if line:
                lines.append((current_address, line, label))
                current_address += 2
        
        return lines
    
    def assemble_instruction(self, line: str, current_pc: int) -> int:
        parts = [p.strip() for p in re.split(r'[,\s]+', line) if p.strip()]
        if not parts:
            raise AssemblerError("Empty instruction", 0)
        
        mnemonic = parts[0].upper()
        
        if mnemonic not in self.OPCODES:
            raise AssemblerError(f"Unknown instruction: {mnemonic}", 0)
        
        opcode = self.OPCODES[mnemonic]
        
        if mnemonic in ['NOP', 'HALT']:
            return opcode << 12
        
        if mnemonic in ['ADD', 'SUB', 'AND', 'OR']:
            if len(parts) != 4:
                raise AssemblerError(f"{mnemonic} requires 3 operands", 0)
            rd = self.parse_register(parts[1])
            rs1 = self.parse_register(parts[2])
            rs2 = self.parse_register(parts[3])
            return self.encode_r_type(opcode, rd, rs1, rs2)
        
        # I-type: ADDI
        if mnemonic == 'ADDI':
            if len(parts) != 4:
                raise AssemblerError("ADDI requires 3 operands", 0)
            rd = self.parse_register(parts[1])
            rs = self.parse_register(parts[2])
            imm = self.parse_immediate(parts[3])
            if imm < -32 or imm > 31:
                raise AssemblerError(f"Immediate out of range: {imm} (must be -32 to 31)", 0)
            # Convert to unsigned 6-bit with sign extension
            imm_unsigned = imm & 0x3F
            return self.encode_i_type(opcode, rd, rs, imm_unsigned)
        
        # M-type: LOAD, STORE
        if mnemonic in ['LOAD', 'STORE']:
            if len(parts) != 4:
                raise AssemblerError(f"{mnemonic} requires 3 operands", 0)
            rd = self.parse_register(parts[1])
            base = self.parse_register(parts[2])
            offset = self.parse_immediate(parts[3])
            if offset < -32 or offset > 31:
                raise AssemblerError(f"Offset out of range: {offset} (must be -32 to 31)", 0)
            # Convert to unsigned 6-bit with sign extension
            offset_unsigned = offset & 0x3F
            return self.encode_m_type(opcode, rd, base, offset_unsigned)
        
        # J-type: JMP, BRZ
        if mnemonic in ['JMP', 'BRZ']:
            if len(parts) != 2:
                raise AssemblerError(f"{mnemonic} requires 1 operand", 0)
            
            target = parts[1]
            offset = 0
            
            if target in self.labels:
                target_addr = self.labels[target]
                offset = target_addr - current_pc
            else:
                try:
                    offset = self.parse_immediate(target)
                except ValueError:
                    raise AssemblerError(f"Unknown label or invalid offset: {target}", 0)
            
            if offset < -512 or offset > 511:
                raise AssemblerError(f"Jump offset out of range: {offset} (must be -512 to 511)", 0)
            
            offset_unsigned = offset & 0x3FF
            cond = 0 if mnemonic == 'JMP' else 0
            return self.encode_j_type(opcode, cond, offset_unsigned)
        
        raise AssemblerError(f"Unhandled instruction: {mnemonic}", 0)
    
    def assemble(self, source: str) -> Tuple[List[int], List[str]]:
        self.labels = {}
        errors = []
        binary = []
        
        try:
            # First pass: collect labels
            preprocessed = self.preprocess(source)
            
            # Second pass: assemble instructions
            for address, line, label in preprocessed:
                try:
                    instruction = self.assemble_instruction(line, address)
                    binary.append(instruction)
                except (AssemblerError, ValueError) as e:
                    errors.append(str(e))
            
        except Exception as e:
            errors.append(f"Assembly error: {str(e)}")
        
        return binary, errors

