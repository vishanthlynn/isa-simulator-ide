import React, { useState, useEffect, useRef } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws/simulate';

function App() {
  const [code, setCode] = useState(`; Simple addition example
        ADDI R1, R0, 5       ; R1 = 5
        ADDI R2, R0, 3       ; R2 = 3
        ADD  R3, R1, R2      ; R3 = R1 + R2
        HALT`);
  
  const [binary, setBinary] = useState([]);
  const [errors, setErrors] = useState([]);
  const [state, setState] = useState(null);
  const [trace, setTrace] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  
  const wsRef = useRef(null);

  useEffect(() => {
    // Cleanup WebSocket on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const connectWebSocket = () => {
    if (wsRef.current) {
      wsRef.current.close();
    }

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      if (message.type === 'state') {
        setState(message.state);
        if (message.trace) {
          setTrace(prev => [...prev, message.trace]);
        }
      } else if (message.type === 'complete') {
        setState(message.state);
        setTrace(message.trace_log);
        setIsRunning(false);
      } else if (message.type === 'error') {
        console.error('WebSocket error:', message.message);
        setIsRunning(false);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsRunning(false);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };
  };

  const handleAssemble = async () => {
    try {
      const response = await axios.post(`${API_URL}/assemble`, {
        source: code
      });
      
      setBinary(response.data.binary);
      setErrors(response.data.errors);
      setTrace([]); // Clear trace
      
      if (response.data.success) {
        // Reset first, then connect and load
        if (wsRef.current) {
          wsRef.current.close();
        }
        connectWebSocket();
        
        // Wait for WebSocket to be ready before loading
        setTimeout(() => {
          if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            // Reset first
            wsRef.current.send(JSON.stringify({ action: 'reset' }));
            // Then load program
            setTimeout(() => {
              if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
                wsRef.current.send(JSON.stringify({
                  action: 'load',
                  binary: response.data.binary,
                  start_address: 0
                }));
              }
            }, 100);
          }
        }, 200);
      }
    } catch (error) {
      console.error('Assemble error:', error);
      setErrors([`Assemble error: ${error.message}`]);
    }
  };

  const handleStep = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ action: 'step' }));
    }
  };

  const handleRun = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      setIsRunning(true);
      setTrace([]);
      wsRef.current.send(JSON.stringify({
        action: 'run',
        max_steps: 10000
      }));
    }
  };

  const handleReset = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ action: 'reset' }));
      setTrace([]);
      setIsRunning(false);
      setState(null);
    }
  };

  return (
    <div className="app">
      <div className="header">
        <h1>ISA Simulator IDE</h1>
        <div className="controls">
          <button onClick={handleAssemble} disabled={isRunning}>
            Assemble
          </button>
          <button onClick={handleStep} disabled={isRunning || !state}>
            Step
          </button>
          <button onClick={handleRun} disabled={isRunning || !state}>
            Run
          </button>
          <button onClick={handleReset} disabled={isRunning}>
            Reset
          </button>
        </div>
      </div>

      <div className="main-content">
        <div className="editor-pane">
          <div className="pane-header">Assembly Editor</div>
          <Editor
            height="100%"
            defaultLanguage="plaintext"
            value={code}
            onChange={(value) => setCode(value || '')}
            theme="vs-dark"
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              wordWrap: 'on',
            }}
          />
          {errors.length > 0 && (
            <div className="errors">
              <strong>Errors:</strong>
              {errors.map((err, i) => (
                <div key={i} className="error">{err}</div>
              ))}
            </div>
          )}
        </div>

        <div className="right-pane">
          <div className="registers-pane">
            <div className="pane-header">Registers</div>
            {state && (
              <div className="registers">
                {state.registers.map((value, i) => (
                  <div key={i} className="register">
                    <span className="reg-name">R{i}</span>
                    <span className="reg-value">{value}</span>
                    <span className="reg-hex">0x{value.toString(16).toUpperCase().padStart(4, '0')}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flags-pane">
            <div className="pane-header">Flags</div>
            {state && (
              <div className="flags">
                <div className={`flag ${state.flags.Z ? 'set' : ''}`}>Z: {state.flags.Z ? '1' : '0'}</div>
                <div className={`flag ${state.flags.N ? 'set' : ''}`}>N: {state.flags.N ? '1' : '0'}</div>
                <div className={`flag ${state.flags.C ? 'set' : ''}`}>C: {state.flags.C ? '1' : '0'}</div>
              </div>
            )}
          </div>

          <div className="state-pane">
            <div className="pane-header">State</div>
            {state && (
              <div className="state-info">
                <div>PC: 0x{state.pc.toString(16).toUpperCase().padStart(4, '0')}</div>
                <div>Cycles: {state.cycle_count}</div>
                <div>Instructions: {state.instruction_count}</div>
                <div>Halted: {state.halted ? 'Yes' : 'No'}</div>
              </div>
            )}
          </div>

          <div className="memory-pane">
            <div className="pane-header">Memory (first 256 bytes)</div>
            {state && (
              <div className="memory">
                {Array.from({ length: Math.min(256, state.memory.length) }, (_, i) => {
                  if (i % 16 === 0) {
                    return (
                      <div key={i} className="memory-row">
                        <span className="mem-addr">0x{i.toString(16).toUpperCase().padStart(4, '0')}:</span>
                        {Array.from({ length: 16 }, (_, j) => (
                          <span key={j} className="mem-byte">
                            {state.memory[i + j]?.toString(16).toUpperCase().padStart(2, '0') || '00'}
                          </span>
                        ))}
                      </div>
                    );
                  }
                  return null;
                })}
              </div>
            )}
          </div>

          <div className="trace-pane">
            <div className="pane-header">Instruction Trace</div>
            <div className="trace">
              {trace.map((line, i) => (
                <div key={i} className="trace-line">{line}</div>
              ))}
            </div>
          </div>
        </div>
      </div>
      
      <div className="footer">
        <div className="footer-content">
          <span>Designed and Developed by <strong>Vishanth Dandu</strong></span>
        </div>
      </div>
    </div>
  );
}

export default App;

