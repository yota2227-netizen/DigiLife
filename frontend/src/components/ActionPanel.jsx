import React from 'react';
import './ActionPanel.css';

const ActionPanel = ({ onAction, state, thresholds }) => {
    return (
        <div className="action-panel">
            <button
                className={`action-btn ${state.energy < thresholds.energy ? 'active request-eat' : ''}`}
                onClick={() => onAction('eat')}
            >
                食事 (Eat)
                {state.energy < thresholds.energy && <span className="alert-badge">!</span>}
            </button>
            <button
                className={`action-btn ${state.social < thresholds.social ? 'active request-talk' : ''}`}
                onClick={() => onAction('talk')}
            >
                会話 (Talk)
                {state.social < thresholds.social && <span className="alert-badge">!</span>}
            </button>
            <button
                className={`action-btn ${state.integrity < thresholds.integrity ? 'active request-sleep' : ''}`}
                onClick={() => onAction('sleep')}
            >
                睡眠 (Sleep)
                {state.integrity < thresholds.integrity && <span className="alert-badge">!</span>}
            </button>
        </div>
    );
};

export default ActionPanel;
