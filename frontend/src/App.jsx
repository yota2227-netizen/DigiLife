import React, { useState, useEffect, useRef } from 'react';
import StatusIndicator from './components/StatusIndicator';
import ActionPanel from './components/ActionPanel';
import './App.css';

function App() {
  const [lifeForm, setLifeForm] = useState({
    energy: 100,
    social: 100,
    integrity: 100
  });
  const [connected, setConnected] = useState(false);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws');

    ws.current.onopen = () => {
      console.log('Connected to WebSocket');
      setConnected(true);
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLifeForm(data);
      } catch (e) {
        console.error('Error parsing WebSocket message', e);
      }
    };

    ws.current.onclose = () => {
      console.log('Disconnected from WebSocket');
      setConnected(false);
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  const handleAction = async (actionType) => {
    try {
      await fetch(`http://localhost:8000/action/${actionType}`, {
        method: 'POST'
      });
    } catch (e) {
      console.error('Error performing action', e);
    }
  };

  return (
    <div className="app-container">
      <div className="dashboard-card">
        <h1 className="app-title">DigiLife Simulation</h1>
        <div className="connection-status">
          Status: <span className={connected ? 'text-green' : 'text-red'}>
            {connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>

        <div className="indicators-section">
          <StatusIndicator label="エネルギー (Energy)" value={lifeForm.energy} />
          <StatusIndicator label="社交性 (Social)" value={lifeForm.social} />
          <StatusIndicator label="整合性 (Integrity)" value={lifeForm.integrity} />
        </div>

        <ActionPanel onAction={handleAction} state={lifeForm} />
      </div>
    </div>
  );
}

export default App;
