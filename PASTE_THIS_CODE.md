# Code to Paste and Test

## 📋 Assembly Code (Copy This)

```
ADDI R1, R0, 5
ADDI R2, R0, 3
ADD R3, R1, R2
HALT
```

Or with comments:
```
; Simple addition example
        ADDI R1, R0, 5       ; R1 = 5
        ADDI R2, R0, 3       ; R2 = 3
        ADD  R3, R1, R2      ; R3 = R1 + R2
        HALT
```

## 🚀 Quick Test Steps

### Step 1: Start Backend (Terminal 1)
```bash
cd /Users/vishanthdandu/isa-simulator-ide/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Wait for: `Uvicorn running on http://127.0.0.1:8000`

### Step 2: Start Frontend (Terminal 2)
```bash
cd /Users/vishanthdandu/isa-simulator-ide/frontend
npm install
npm start
```

Wait for browser to open at `http://localhost:3000`

### Step 3: Paste and Test
1. **Paste** the code above into the Monaco editor
2. **Click "Assemble"** button
   - Should show: No errors ✅
3. **Click "Step"** button 4 times:
   - Step 1: R1 becomes 5
   - Step 2: R2 becomes 3  
   - Step 3: R3 becomes 8
   - Step 4: Program halts
4. **Or click "Run"** to execute all at once

## ✅ Expected Results

After clicking "Run" or 4 "Step" clicks:

| Register | Value | Hex |
|----------|-------|-----|
| R1 | 5 | 0x0005 |
| R2 | 3 | 0x0003 |
| R3 | 8 | 0x0008 |

**PC**: 0x0006 (after HALT)
**Halted**: Yes ✅

## 🧪 Alternative: Test API Directly

If you want to test just the backend API:

```bash
cd /Users/vishanthdandu/isa-simulator-ide
./test_api.sh
```

Or manually:
```bash
curl -X POST http://localhost:8000/assemble \
  -H "Content-Type: application/json" \
  -d '{
    "source": "ADDI R1, R0, 5\nADDI R2, R0, 3\nADD R3, R1, R2\nHALT"
  }'
```

## 🐛 Troubleshooting

**Backend not starting?**
- Check: `python3 --version` (needs 3.8+)
- Check: Port 8000 free? `lsof -i :8000`

**Frontend not starting?**
- Check: `node --version` (needs 16+)
- Check: Port 3000 free? `lsof -i :3000`

**Assemble button shows errors?**
- Make sure backend is running
- Check browser console (F12) for errors
- Verify code has no typos

**Registers not updating?**
- Click "Assemble" first
- Then click "Step" or "Run"
- Check WebSocket connection in browser console

