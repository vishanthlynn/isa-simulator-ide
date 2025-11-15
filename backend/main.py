# FastAPI backend for ISA Simulator
# Vishanth Dandu

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json

from assembler import Assembler
from simulator import Simulator

app = FastAPI(title="ISA Simulator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://isa-simulator-ide.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AssembleRequest(BaseModel):
    source: str


class AssembleResponse(BaseModel):
    binary: List[int]
    errors: List[str]
    success: bool


@app.get("/")
async def root():
    return {"message": "ISA Simulator API", "version": "1.0.0"}


@app.post("/assemble", response_model=AssembleResponse)
async def assemble(request: AssembleRequest):
    assembler = Assembler()
    binary, errors = assembler.assemble(request.source)
    
    return AssembleResponse(
        binary=binary,
        errors=errors,
        success=len(errors) == 0
    )


@app.websocket("/ws/simulate")
async def websocket_simulate(websocket: WebSocket):
    await websocket.accept()
    simulator = Simulator()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            action = message.get("action")
            
            if action == "load":
                binary = message.get("binary", [])
                start_addr = message.get("start_address", 0)
                simulator.load_program(binary, start_addr)
                await websocket.send_json({
                    "type": "state",
                    "state": simulator.get_state_dict()
                })
            
            elif action == "step":
                trace = simulator.step()
                await websocket.send_json({
                    "type": "state",
                    "state": simulator.get_state_dict(),
                    "trace": trace
                })
            
            elif action == "run":
                max_steps = message.get("max_steps", 10000)
                trace_log = simulator.run(max_steps)
                await websocket.send_json({
                    "type": "complete",
                    "state": simulator.get_state_dict(),
                    "trace_log": trace_log
                })
            
            elif action == "reset":
                simulator.reset()
                await websocket.send_json({
                    "type": "state",
                    "state": simulator.get_state_dict()
                })
            
            elif action == "set_breakpoint":
                addr = message.get("address")
                if addr is not None:
                    simulator.breakpoints.append(addr)
                    await websocket.send_json({
                        "type": "breakpoint_set",
                        "address": addr
                    })
            
            elif action == "clear_breakpoint":
                addr = message.get("address")
                if addr is not None and addr in simulator.breakpoints:
                    simulator.breakpoints.remove(addr)
                    await websocket.send_json({
                        "type": "breakpoint_cleared",
                        "address": addr
                    })
            
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

