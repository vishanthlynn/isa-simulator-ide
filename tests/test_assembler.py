"""
Unit tests for assembler
"""

import pytest
from assembler import Assembler, AssemblerError


def test_simple_add():
    """Test simple ADD instruction"""
    assembler = Assembler()
    source = "ADD R1, R2, R3"
    binary, errors = assembler.assemble(source)
    assert len(errors) == 0
    assert len(binary) == 1
    # ADD opcode=0x1, R1=1, R2=2, R3=3
    # Expected: 0x1 << 12 | 1 << 9 | 2 << 6 | 3 << 3 = 0x1248
    assert binary[0] == 0x1248


def test_addi():
    """Test ADDI instruction"""
    assembler = Assembler()
    source = "ADDI R1, R2, 5"
    binary, errors = assembler.assemble(source)
    assert len(errors) == 0
    assert len(binary) == 1
    # ADDI opcode=0x5, R1=1, R2=2, imm=5
    # Expected: 0x5 << 12 | 1 << 9 | 2 << 6 | 5 = 0x5245
    assert binary[0] == 0x5245


def test_labels():
    """Test label resolution"""
    assembler = Assembler()
    source = """
        JMP target
        NOP
target: HALT
    """
    binary, errors = assembler.assemble(source)
    assert len(errors) == 0
    assert len(binary) == 3
    # JMP should jump forward by 2 (to target at address 2)
    # JMP opcode=0x8, offset=2
    assert (binary[0] >> 12) == 0x8


def test_invalid_register():
    """Test error handling for invalid register"""
    assembler = Assembler()
    source = "ADD R8, R1, R2"  # R8 is out of range
    binary, errors = assembler.assemble(source)
    assert len(errors) > 0


def test_halt():
    """Test HALT instruction"""
    assembler = Assembler()
    source = "HALT"
    binary, errors = assembler.assemble(source)
    assert len(errors) == 0
    assert binary[0] == 0xA000  # HALT opcode << 12

