import React from 'react';
import './StatusIndicator.css';

const StatusIndicator = ({ label, value, threshold = 20 }) => {
    let colorClass = 'status-green';
    if (value < threshold) {
        colorClass = 'status-red';
    } else if (value < 50) {
        colorClass = 'status-yellow';
    }

    return (
        <div className="status-container">
            <div className="status-header">
                <span className="status-label">{label}</span>
                <span className="status-value">{Math.round(value)}%</span>
            </div>
            <div className="progress-bar-bg">
                <div className={`progress-bar-fill ${colorClass}`} style={{ width: `${value}%` }}></div>
            </div>
        </div>
    );
};

export default StatusIndicator;
