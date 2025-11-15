#!/usr/bin/env python3
"""
Quick test script for the assembly program
Tests assembler and simulator with the simple addition example
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from assembler import Assembler
from simulator import Simulator

def test_simple_add():
    """Test the simple addition program"""
    
    # Your assembly code
    source = """; Simple addition example
        ADDI R1, R0, 5       ; R1 = 5
        ADDI R2, R0, 3       ; R2 = 3
        ADD  R3, R1, R2      ; R3 = R1 + R2
        HALT"""
    
    print("=" * 60)
    print("Testing Assembly Program")
    print("=" * 60)
    print("\nSource Code:")
    print(source)
    print("\n" + "-" * 60)
    
    # Step 1: Assemble
    print("\n[1] Assembling...")
    assembler = Assembler()
    binary, errors = assembler.assemble(source)
    
    if errors:
        print("❌ Assembly Errors:")
        for error in errors:
            print(f"   {error}")
        return False
    else:
        print("✅ Assembly successful!")
        print(f"   Generated {len(binary)} instructions:")
        for i, instr in enumerate(binary):
            print(f"   [{i}] 0x{instr:04X} ({instr:016b})")
    
    print("\n" + "-" * 60)
    
    # Step 2: Simulate
    print("\n[2] Simulating...")
    simulator = Simulator()
    simulator.load_program(binary, start_address=0)
    
    print("\nInitial State:")
    print(f"   PC: 0x{simulator.state.pc:04X}")
    print(f"   Registers: {simulator.state.registers}")
    
    print("\nExecuting instructions step by step:")
    print("-" * 60)
    
    step_count = 0
    while not simulator.state.halted and step_count < 10:
        trace = simulator.step()
        step_count += 1
        print(f"\nStep {step_count}: {trace}")
        print(f"   PC: 0x{simulator.state.pc:04X}")
        print(f"   R1: {simulator.state.registers[1]}, "
              f"R2: {simulator.state.registers[2]}, "
              f"R3: {simulator.state.registers[3]}")
        print(f"   Flags: Z={simulator.state.flags['Z']}, "
              f"N={simulator.state.flags['N']}, "
              f"C={simulator.state.flags['C']}")
    
    print("\n" + "-" * 60)
    print("\n[3] Final Results:")
    print("-" * 60)
    print(f"✅ Program completed in {simulator.state.instruction_count} instructions")
    print(f"✅ Total cycles: {simulator.state.cycle_count}")
    print(f"\nFinal Register Values:")
    for i in range(8):
        if simulator.state.registers[i] != 0 or i <= 3:
            print(f"   R{i}: {simulator.state.registers[i]} (0x{simulator.state.registers[i]:04X})")
    
    print(f"\nExpected Result:")
    print(f"   R1 = 5")
    print(f"   R2 = 3")
    print(f"   R3 = 8 (5 + 3)")
    
    # Verify results
    success = True
    if simulator.state.registers[1] == 5:
        print(f"   ✅ R1 is correct: {simulator.state.registers[1]}")
    else:
        print(f"   ❌ R1 is incorrect: expected 5, got {simulator.state.registers[1]}")
        success = False
    
    if simulator.state.registers[2] == 3:
        print(f"   ✅ R2 is correct: {simulator.state.registers[2]}")
    else:
        print(f"   ❌ R2 is incorrect: expected 3, got {simulator.state.registers[2]}")
        success = False
    
    if simulator.state.registers[3] == 8:
        print(f"   ✅ R3 is correct: {simulator.state.registers[3]}")
    else:
        print(f"   ❌ R3 is incorrect: expected 8, got {simulator.state.registers[3]}")
        success = False
    
    if simulator.state.halted:
        print(f"   ✅ Program halted correctly")
    else:
        print(f"   ❌ Program did not halt")
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    success = test_simple_add()
    sys.exit(0 if success else 1)

