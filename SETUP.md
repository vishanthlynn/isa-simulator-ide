# Setup Instructions

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the backend server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Running Tests

From the project root:

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_assembler.py
pytest tests/test_simulator.py
```

## Project Structure

```
isa-simulator-ide/
├── backend/           # FastAPI server + simulator
│   ├── main.py        # API endpoints and WebSocket
│   ├── simulator.py   # CPU simulator core
│   ├── assembler.py   # Assembly to binary converter
│   └── requirements.txt
├── frontend/          # React web application
│   ├── src/
│   │   ├── App.js     # Main React component
│   │   └── ...
│   └── package.json
├── spec/              # ISA specification
├── examples/          # Example assembly programs
└── tests/             # Unit tests
```

## Usage

1. Start the backend server (port 8000)
2. Start the frontend server (port 3000)
3. Open `http://localhost:3000` in your browser
4. Write assembly code in the editor
5. Click "Assemble" to compile
6. Use "Step" to execute one instruction at a time
7. Use "Run" to execute until halt
8. View registers, memory, and instruction trace in the right panel

## Example Assembly Code

```assembly
; Simple addition
        ADDI R1, R0, 5       ; R1 = 5
        ADDI R2, R0, 3       ; R2 = 3
        ADD  R3, R1, R2      ; R3 = R1 + R2
        HALT
```

## Troubleshooting

- **Backend won't start**: Make sure port 8000 is not in use
- **Frontend won't connect**: Ensure backend is running on port 8000
- **WebSocket errors**: Check browser console for connection issues
- **Assembly errors**: Check the error panel below the editor

