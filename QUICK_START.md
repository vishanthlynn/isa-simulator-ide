# Quick Start Guide

## ✅ Your Program is Working!

Your assembly program has been tested and works perfectly:
- ✅ Assembles correctly
- ✅ Executes correctly  
- ✅ Produces correct results (R3 = 8)

## 🚀 Three Ways to Test

### Option 1: Command Line Test (Fastest)
```bash
cd /Users/vishanthdandu/isa-simulator-ide
python3 test_program.py
```

### Option 2: Web Interface (Most Visual)

**Terminal 1 - Backend:**
```bash
cd /Users/vishanthdandu/isa-simulator-ide/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd /Users/vishanthdandu/isa-simulator-ide/frontend
npm install
npm start
```

Then open `http://localhost:3000` and paste your code!

### Option 3: Python Script (Interactive)

```python
from backend.assembler import Assembler
from backend.simulator import Simulator

source = """ADDI R1, R0, 5
ADDI R2, R0, 3
ADD R3, R1, R2
HALT"""

# Assemble
assembler = Assembler()
binary, errors = assembler.assemble(source)
print(f"Binary: {[hex(x) for x in binary]}")

# Simulate
simulator = Simulator()
simulator.load_program(binary)
while not simulator.state.halted:
    trace = simulator.step()
    print(trace)
    print(f"R1={simulator.state.registers[1]}, "
          f"R2={simulator.state.registers[2]}, "
          f"R3={simulator.state.registers[3]}")
```

## 📝 Your Test Program

```assembly
; Simple addition example
        ADDI R1, R0, 5       ; R1 = 5
        ADDI R2, R0, 3       ; R2 = 3
        ADD  R3, R1, R2      ; R3 = R1 + R2
        HALT
```

**Expected Output:**
- R1 = 5
- R2 = 3
- R3 = 8 ✅

## 🎯 Next Steps

1. **Try the web interface** - It's the most impressive way to demonstrate the project
2. **Modify the program** - Try different operations
3. **Check examples/** - See `examples/simple_add.asm` and `examples/sum_array.asm`
4. **Read the spec** - See `spec/isa_spec.md` for all available instructions

