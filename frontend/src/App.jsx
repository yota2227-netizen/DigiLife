import React, { useState, useEffect, useRef } from 'react';
import StatusIndicator from './components/StatusIndicator';
import ActionPanel from './components/ActionPanel';
import CharacterDisplay from './components/CharacterDisplay';
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

        <div className="dashboard-content">
          <div className="left-panel">
            <div className="indicators-section">
              <StatusIndicator
                label="エネルギー (Energy)"
                value={lifeForm.energy}
                threshold={20}
                customDisplay={`${Math.round(lifeForm.energy)}% (${lifeForm.token_balance} / 5000 Token)`}
              />
              <StatusIndicator label="社交性 (Social)" value={lifeForm.social} threshold={50} />
              <StatusIndicator label="整合性 (Integrity)" value={lifeForm.integrity} threshold={20} />
            </div>

            <ActionPanel
              onAction={handleAction}
              state={lifeForm}
              thresholds={{
                energy: lifeForm.energy < 20,
                social: lifeForm.social < 50,
                integrity: lifeForm.integrity < 20
              }}
            />

            <div className="search-stats" style={{ marginTop: '20px', padding: '15px', background: 'rgba(255,255,255,0.8)', borderRadius: '10px', color: '#1f2937' }}>
              <h3 style={{ fontSize: '1rem', marginBottom: '10px', color: '#111827', fontWeight: 'bold' }}>Web Search Stats</h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '8px 15px', fontSize: '0.9rem', alignItems: 'center' }}>
                <div style={{ color: '#4b5563' }}>Last Keyword:</div>
                <div style={{ fontWeight: 'bold', color: '#111827' }}>{lifeForm.last_search_keyword || '-'}</div>

                <div style={{ color: '#4b5563' }}>Last Tokens:</div>
                <div style={{ fontWeight: 'bold', color: '#111827' }}>{lifeForm.last_search_tokens || 0}</div>

                <div style={{ color: '#4b5563' }}>Total Tokens:</div>
                <div style={{ fontWeight: 'bold', color: '#10b981' }}>{lifeForm.total_search_tokens || 0}</div>
              </div>
            </div>
          </div>

          <div className="right-panel">
            <CharacterDisplay state={lifeForm} thresholds={{ energy: 20, social: 50, integrity: 20 }} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
