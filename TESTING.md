# Testing Guide

## ✅ Quick Test (Command Line)

Your program has been tested and **works correctly**! Here's what happened:

### Test Results:
```
✅ Assembly successful - 4 instructions generated
✅ R1 = 5 (correct)
✅ R2 = 3 (correct)  
✅ R3 = 8 (correct - 5 + 3)
✅ Program halted correctly
```

### Run the test yourself:
```bash
cd /Users/vishanthdandu/isa-simulator-ide
python3 test_program.py
```

## 🌐 Full Web Interface Testing

### Step 1: Start the Backend Server

```bash
cd /Users/vishanthdandu/isa-simulator-ide/backend

# Create virtual environment (first time only)
python3 -m venv venv
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### Step 2: Test the API (Optional)

In another terminal, test the assemble endpoint:

```bash
curl -X POST http://localhost:8000/assemble \
  -H "Content-Type: application/json" \
  -d '{
    "source": "ADDI R1, R0, 5\nADDI R2, R0, 3\nADD R3, R1, R2\nHALT"
  }'
```

### Step 3: Start the Frontend

Open a new terminal:

```bash
cd /Users/vishanthdandu/isa-simulator-ide/frontend

# Install dependencies (first time only)
npm install

# Start the development server
npm start
```

The frontend will open at `http://localhost:3000`

### Step 4: Use the Web Interface

1. **Open** `http://localhost:3000` in your browser
2. **Paste** your assembly code in the editor:
   ```
   ADDI R1, R0, 5       ; R1 = 5
   ADDI R2, R0, 3       ; R2 = 3
   ADD  R3, R1, R2      ; R3 = R1 + R2
   HALT
   ```
3. **Click "Assemble"** - should show no errors
4. **Click "Step"** multiple times to execute each instruction
5. **Watch** the registers update in real-time:
   - After step 1: R1 = 5
   - After step 2: R2 = 3
   - After step 3: R3 = 8
   - After step 4: HALT
6. **Or click "Run"** to execute all at once

## 📊 Expected Results

| Step | Instruction | R1 | R2 | R3 | PC |
|------|-------------|----|----|----|-----|
| 0    | (start)     | 0  | 0  | 0  | 0x0000 |
| 1    | ADDI R1, R0, 5 | 5 | 0  | 0  | 0x0002 |
| 2    | ADDI R2, R0, 3 | 5 | 3  | 0  | 0x0004 |
| 3    | ADD R3, R1, R2 | 5 | 3  | 8  | 0x0006 |
| 4    | HALT        | 5  | 3  | 8  | 0x0006 |

## 🧪 Run Unit Tests

```bash
cd /Users/vishanthdandu/isa-simulator-ide/backend

# Install pytest (first time only)
pip install pytest

# Run tests
pytest ../tests/ -v
```

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is already in use: `lsof -i :8000`
- Make sure you're in the backend directory
- Verify Python version: `python3 --version` (needs 3.8+)

### Frontend won't start
- Check if port 3000 is already in use
- Make sure Node.js is installed: `node --version`
- Try deleting `node_modules` and running `npm install` again

### WebSocket connection errors
- Make sure backend is running first
- Check browser console for errors
- Verify CORS settings in `backend/main.py`

### Assembly errors
- Check syntax matches the ISA spec
- Register numbers must be R0-R7
- Immediate values must be in range (-32 to 31 for ADDI)

## ✅ Verification Checklist

- [x] Assembler correctly parses your code
- [x] Simulator executes instructions correctly
- [x] Registers update as expected
- [x] Program halts correctly
- [ ] Backend API responds (test with curl or web interface)
- [ ] Frontend connects to backend
- [ ] Web interface displays registers correctly
- [ ] Step/Run buttons work

