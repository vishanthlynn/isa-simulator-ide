#!/bin/bash
# Test the backend API directly

echo "Testing ISA Simulator API..."
echo ""

# Test assemble endpoint
echo "1. Testing /assemble endpoint..."
curl -X POST http://localhost:8000/assemble \
  -H "Content-Type: application/json" \
  -d '{
    "source": "ADDI R1, R0, 5\nADDI R2, R0, 3\nADD R3, R1, R2\nHALT"
  }' | python3 -m json.tool

echo ""
echo "2. Testing root endpoint..."
curl http://localhost:8000/

echo ""
echo ""
echo "✅ If you see JSON output above, the API is working!"
echo "   Now start the frontend with: cd frontend && npm start"

