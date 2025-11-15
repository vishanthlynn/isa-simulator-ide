"""
Unit tests for simulator
"""

import pytest
from simulator import Simulator


def test_simple_add():
    """Test simple ADD instruction execution"""
    simulator = Simulator()
    # ADD R1, R2, R3 where R2=5, R3=3
    simulator.state.registers[2] = 5
    simulator.state.registers[3] = 3
    # Encode: ADD(0x1) R1(1) R2(2) R3(3)
    instruction = 0x1248
    simulator.state.pc = 0
    simulator.state.memory[0] = 0x48
    simulator.state.memory[1] = 0x12
    
    trace = simulator.step()
    assert simulator.state.registers[1] == 8
    assert simulator.state.pc == 2


def test_addi():
    """Test ADDI instruction execution"""
    simulator = Simulator()
    simulator.state.registers[2] = 10
    # ADDI R1, R2, 5
    simulator.state.memory[0] = 0x45
    simulator.state.memory[1] = 0x52
    
    trace = simulator.step()
    assert simulator.state.registers[1] == 15
    assert simulator.state.pc == 2


def test_flags():
    """Test flag updates"""
    simulator = Simulator()
    simulator.state.registers[1] = 5
    simulator.state.registers[2] = 5
    # SUB R3, R1, R2 (should result in 0, setting Z flag)
    simulator.state.memory[0] = 0x66
    simulator.state.memory[1] = 0x22
    
    trace = simulator.step()
    assert simulator.state.registers[3] == 0
    assert simulator.state.flags['Z'] == True


def test_halt():
    """Test HALT instruction"""
    simulator = Simulator()
    simulator.state.memory[0] = 0x00
    simulator.state.memory[1] = 0xA0  # HALT
    
    trace = simulator.step()
    assert simulator.state.halted == True


def test_load_store():
    """Test LOAD and STORE instructions"""
    simulator = Simulator()
    simulator.state.registers[1] = 0x0100  # Base address
    simulator.state.registers[2] = 42      # Value to store
    
    # STORE R2, R1, 0
    simulator.state.memory[0] = 0x00
    simulator.state.memory[1] = 0x72
    
    trace = simulator.step()
    # Check value was stored
    assert simulator.state.memory[0x0100] == 42
    assert simulator.state.memory[0x0101] == 0
    
    # Now load it back
    simulator.state.pc = 2
    # LOAD R3, R1, 0
    simulator.state.memory[2] = 0x00
    simulator.state.memory[3] = 0x63
    
    trace = simulator.step()
    assert simulator.state.registers[3] == 42

