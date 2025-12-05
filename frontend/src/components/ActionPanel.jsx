import React from 'react';
import './ActionPanel.css';

const ActionPanel = ({ onAction, state, threshold = 20 }) => {
    return (
        <div className="action-panel">
            <button
                className={`action-btn ${state.energy < threshold ? 'active request-eat' : ''}`}
                onClick={() => onAction('eat')}
            >
                食事 (Eat)
                {state.energy < threshold && <span className="alert-badge">!</span>}
            </button>
            <button
                className={`action-btn ${state.social < threshold ? 'active request-talk' : ''}`}
                onClick={() => onAction('talk')}
            >
                会話 (Talk)
                {state.social < threshold && <span className="alert-badge">!</span>}
            </button>
            <button
                className={`action-btn ${state.integrity < threshold ? 'active request-sleep' : ''}`}
                onClick={() => onAction('sleep')}
            >
                睡眠 (Sleep)
                {state.integrity < threshold && <span className="alert-badge">!</span>}
            </button>
        </div>
    );
};

export default ActionPanel;
