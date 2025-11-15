# ISA Simulator - 16-bit instruction set simulator
# Vishanth Dandu

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class CPUState:
    # CPU state storage
    registers: List[int] = field(default_factory=lambda: [0] * 8)
    memory: List[int] = field(default_factory=lambda: [0] * 65536)  # 64KB
    pc: int = 0
    flags: Dict[str, bool] = field(default_factory=lambda: {'Z': False, 'N': False, 'C': False})
    halted: bool = False
    cycle_count: int = 0
    instruction_count: int = 0


class InstructionDecoder:
    # Instruction decoding utilities
    
    @staticmethod
    def decode_r_type(instruction: int) -> Tuple[int, int, int, int]:
        # R-type: opcode(4) rd(3) rs1(3) rs2(3) unused(3)
        opcode = (instruction >> 12) & 0xF
        rd = (instruction >> 9) & 0x7
        rs1 = (instruction >> 6) & 0x7
        rs2 = (instruction >> 3) & 0x7
        return opcode, rd, rs1, rs2
    
    @staticmethod
    def decode_i_type(instruction: int) -> Tuple[int, int, int, int]:
        # I-type: opcode(4) rd(3) rs(3) imm6(6)
        opcode = (instruction >> 12) & 0xF
        rd = (instruction >> 9) & 0x7
        rs = (instruction >> 6) & 0x7
        imm6 = instruction & 0x3F
        # sign extend
        if imm6 & 0x20:
            imm6 |= 0xFFC0
        return opcode, rd, rs, imm6
    
    @staticmethod
    def decode_j_type(instruction: int) -> Tuple[int, int, int]:
        # J-type: opcode(4) cond(2) offset10(10)
        opcode = (instruction >> 12) & 0xF
        cond = (instruction >> 10) & 0x3
        offset10 = instruction & 0x3FF
        # sign extend offset
        if offset10 & 0x200:
            offset10 |= 0xFC00
        return opcode, cond, offset10
    
    @staticmethod
    def decode_m_type(instruction: int) -> Tuple[int, int, int, int]:
        # M-type: opcode(4) rd(3) base(3) offset6(6)
        opcode = (instruction >> 12) & 0xF
        rd = (instruction >> 9) & 0x7
        base = (instruction >> 6) & 0x7
        offset6 = instruction & 0x3F
        if offset6 & 0x20:
            offset6 |= 0xFFC0
        return opcode, rd, base, offset6


class Simulator:
    """Main simulator class implementing fetch-decode-execute cycle"""
    
    def __init__(self):
        self.state = CPUState()
        self.decoder = InstructionDecoder()
        self.breakpoints: List[int] = []
        self.watchpoints: List[int] = []
    
    def reset(self):
        # clear everything
        self.state.memory = [0] * 65536
        self.state.pc = 0
        self.state.halted = False
        self.state.cycle_count = 0
        self.state.instruction_count = 0
        self.state.registers = [0] * 8
        self.state.flags = {'Z': False, 'N': False, 'C': False}
        self.breakpoints = []
        self.watchpoints = []
    
    def load_program(self, binary: List[int], start_address: int = 0):
        # reset and load program
        self.state.pc = start_address
        self.state.halted = False
        self.state.cycle_count = 0
        self.state.instruction_count = 0
        self.state.registers = [0] * 8
        self.state.flags = {'Z': False, 'N': False, 'C': False}
        
        for i, word in enumerate(binary):
            addr = start_address + (i * 2)
            if addr < len(self.state.memory) - 1:
                self.state.memory[addr] = word & 0xFF
                self.state.memory[addr + 1] = (word >> 8) & 0xFF
    
    def fetch_instruction(self) -> int:
        # fetch instruction at PC
        if self.state.pc >= len(self.state.memory) - 1 or self.state.pc < 0:
            self.state.halted = True
            return 0
        low = self.state.memory[self.state.pc]
        high = self.state.memory[self.state.pc + 1]
        return low | (high << 8)
    
    def update_flags(self, result: int):
        self.state.flags['Z'] = (result == 0)
        self.state.flags['N'] = (result & 0x8000) != 0
    
    def execute_instruction(self, instruction: int) -> Optional[str]:
        """Execute a single instruction, returns trace string"""
        opcode = (instruction >> 12) & 0xF
        
        trace = f"PC={self.state.pc:04X} I={instruction:04X} "
        
        if opcode == 0x0:  # NOP
            trace += "NOP"
        
        elif opcode == 0x1:  # ADD
            _, rd, rs1, rs2 = self.decoder.decode_r_type(instruction)
            result = self.state.registers[rs1] + self.state.registers[rs2]
            result &= 0xFFFF  # 16-bit wrap
            self.state.registers[rd] = result
            self.update_flags(result)
            self.state.flags['C'] = (result < self.state.registers[rs1])  # Carry
            trace += f"ADD R{rd}, R{rs1}, R{rs2}"
        
        elif opcode == 0x2:  # SUB
            _, rd, rs1, rs2 = self.decoder.decode_r_type(instruction)
            result = self.state.registers[rs1] - self.state.registers[rs2]
            result &= 0xFFFF  # 16-bit wrap
            self.state.registers[rd] = result
            self.update_flags(result)
            trace += f"SUB R{rd}, R{rs1}, R{rs2}"
        
        elif opcode == 0x3:  # AND
            _, rd, rs1, rs2 = self.decoder.decode_r_type(instruction)
            result = self.state.registers[rs1] & self.state.registers[rs2]
            self.state.registers[rd] = result
            self.update_flags(result)
            trace += f"AND R{rd}, R{rs1}, R{rs2}"
        
        elif opcode == 0x4:  # OR
            _, rd, rs1, rs2 = self.decoder.decode_r_type(instruction)
            result = self.state.registers[rs1] | self.state.registers[rs2]
            self.state.registers[rd] = result
            self.update_flags(result)
            trace += f"OR R{rd}, R{rs1}, R{rs2}"
        
        elif opcode == 0x5:  # ADDI
            _, rd, rs, imm = self.decoder.decode_i_type(instruction)
            result = self.state.registers[rs] + imm
            result &= 0xFFFF  # 16-bit wrap
            self.state.registers[rd] = result
            self.update_flags(result)
            trace += f"ADDI R{rd}, R{rs}, {imm}"
        
        elif opcode == 0x6:  # LOAD
            _, rd, base, offset = self.decoder.decode_m_type(instruction)
            addr = (self.state.registers[base] + offset) & 0xFFFF
            if addr < len(self.state.memory) - 1:
                low = self.state.memory[addr]
                high = self.state.memory[addr + 1]
                self.state.registers[rd] = low | (high << 8)
            trace += f"LOAD R{rd}, R{base}, {offset}"
        
        elif opcode == 0x7:  # STORE
            _, rd, base, offset = self.decoder.decode_m_type(instruction)
            addr = (self.state.registers[base] + offset) & 0xFFFF
            value = self.state.registers[rd]
            if addr < len(self.state.memory) - 1:
                self.state.memory[addr] = value & 0xFF
                self.state.memory[addr + 1] = (value >> 8) & 0xFF
            trace += f"STORE R{rd}, R{base}, {offset}"
        
        elif opcode == 0x8:  # JMP
            _, cond, offset = self.decoder.decode_j_type(instruction)
            self.state.pc += offset
            trace += f"JMP {offset:+d}"
            return trace  # Early return, PC already updated
        
        elif opcode == 0x9:  # BRZ
            _, cond, offset = self.decoder.decode_j_type(instruction)
            if self.state.flags['Z']:
                self.state.pc += offset
                trace += f"BRZ (taken) {offset:+d}"
            else:
                trace += f"BRZ (not taken) {offset:+d}"
            if self.state.flags['Z']:
                return trace  # Early return if branch taken
        
        elif opcode == 0xA:  # HALT
            self.state.halted = True
            trace += "HALT"
            return trace
        
        else:
            trace += f"UNKNOWN({opcode})"
        
        self.state.pc += 2  # Advance PC by 2 bytes (word size)
        return trace
    
    def step(self) -> Optional[str]:
        if self.state.halted:
            return None
        
        if self.state.pc in self.breakpoints:
            return f"BREAKPOINT at PC={self.state.pc:04X}"
        
        instruction = self.fetch_instruction()
        trace = self.execute_instruction(instruction)
        self.state.cycle_count += 1
        self.state.instruction_count += 1
        return trace
    
    def run(self, max_steps: int = 10000) -> List[str]:
        trace_log = []
        steps = 0
        
        while not self.state.halted and steps < max_steps:
            if self.state.pc in self.breakpoints:
                trace_log.append(f"BREAKPOINT at PC={self.state.pc:04X}")
                break
            
            trace = self.step()
            if trace:
                trace_log.append(trace)
            steps += 1
        
        return trace_log
    
    def get_state_dict(self) -> dict:
        return {
            'registers': self.state.registers,
            'pc': self.state.pc,
            'flags': self.state.flags,
            'halted': self.state.halted,
            'cycle_count': self.state.cycle_count,
            'instruction_count': self.state.instruction_count,
            'memory': self.state.memory[:1024]
        }

