# Instruction Set Simulator + Web IDE

A custom 16-bit ISA with a Python-based simulator and React web IDE for interactive assembly programming.

**Designed and Developed by Vishanth Dandu**

## Project Structure

```
isa-simulator-ide/
├── frontend/          # React web application
├── backend/           # FastAPI server + simulator
├── spec/              # ISA specification documents
├── examples/          # Example assembly programs
└── tests/             # Unit tests
```

## Features

- **Custom 16-bit ISA** with R-type, I-type, J-type, and M-type instructions
- **Web-based IDE** with Monaco editor for assembly code
- **Real-time simulation** via WebSocket streaming
- **Visual register file** and memory hex dump
- **Instruction trace** and pipeline visualization
- **Step/Run/Reset controls** for debugging
- **Save/share programs** functionality

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## ISA Overview

- **Registers**: R0-R7 (8 general-purpose registers)
- **Word size**: 16-bit
- **PC**: 16-bit program counter
- **Flags**: Z (zero), N (negative), C (carry)

See `spec/isa_spec.md` for complete specification.

## Example Programs

Check `examples/` directory for sample assembly programs including:
- Array sum
- Sorting algorithms
- Matrix operations

## Testing

```bash
pytest tests/
```

## Author

**Vishanth Dandu**

Designed and developed as a comprehensive project demonstrating:
- Custom ISA design and specification
- Instruction set simulator implementation
- Full-stack web application development
- Real-time WebSocket communication
- Interactive debugging and visualization

## License

MIT

