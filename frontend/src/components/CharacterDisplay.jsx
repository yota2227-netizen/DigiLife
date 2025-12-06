import React, { useState, useEffect } from 'react';
import NormalImg from '../assets/Normal.png';
import FineImg from '../assets/Fine.png';
import './CharacterDisplay.css';

const CharacterDisplay = ({ state, thresholds }) => {
    const [currentImage, setCurrentImage] = useState(NormalImg);
    const [isFineFrame, setIsFineFrame] = useState(false);

    // Check if any parameter is below threshold (Violation)
    const isViolation =
        state.energy < thresholds.energy ||
        state.social < thresholds.social ||
        state.integrity < thresholds.integrity;

    useEffect(() => {
        let interval;

        if (!isViolation) {
            // Normal operation: Toggle between Normal and Fine every 0.5s
            interval = setInterval(() => {
                setIsFineFrame(prev => !prev);
            }, 500);
        } else {
            // Violation state: Stop animation, show Normal (or wait for future instruction)
            setIsFineFrame(false);
        }

        return () => {
            if (interval) clearInterval(interval);
        };
    }, [isViolation]);

    useEffect(() => {
        setCurrentImage(isFineFrame ? FineImg : NormalImg);
    }, [isFineFrame]);

    return (
        <div className="character-container">
            <img src={currentImage} alt="Character" className="character-img" />
        </div>
    );
};

export default CharacterDisplay;
