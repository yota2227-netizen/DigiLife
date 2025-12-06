import React, { useState, useEffect } from 'react';
import NormalImg from '../assets/Normal.png';
import FineImg from '../assets/Fine.png';
import HungryImg from '../assets/Hungry.png';
import LonelyImg from '../assets/Lonely.png';
import SleepyImg from '../assets/Sleepy.png';
import RetroDevice from './RetroDevice';
import './CharacterDisplay.css';

const CharacterDisplay = ({ state, thresholds }) => {
    const [currentImage, setCurrentImage] = useState(NormalImg);
    const [animationIndex, setAnimationIndex] = useState(0);

    // Determine active violations
    const isEnergyLow = state.energy < thresholds.energy;
    const isSocialLow = state.social < thresholds.social;
    const isIntegrityLow = state.integrity < thresholds.integrity;
    const isViolation = isEnergyLow || isSocialLow || isIntegrityLow;

    // Calculate the sequence of images to animate
    // Healthy: Normal -> Fine
    // Violation: Normal -> ViolationState1 -> Normal -> ViolationState2 ...
    const getAnimationSequence = () => {
        if (!isViolation) {
            return [NormalImg, FineImg];
        }

        const sequence = [];
        if (isEnergyLow) {
            sequence.push(NormalImg, HungryImg);
        }
        if (isSocialLow) {
            sequence.push(NormalImg, LonelyImg);
        }
        if (isIntegrityLow) {
            sequence.push(NormalImg, SleepyImg);
        }
        return sequence;
    };

    const animationSequence = getAnimationSequence();

    useEffect(() => {
        // Reset index if sequence length changes (to avoid out of bounds)
        // This effectively resets animation when state changes significantly
        setAnimationIndex(0);
    }, [isViolation, isEnergyLow, isSocialLow, isIntegrityLow]);

    useEffect(() => {
        const interval = setInterval(() => {
            setAnimationIndex((prevIndex) => (prevIndex + 1) % animationSequence.length);
        }, 500);

        return () => clearInterval(interval);
    }, [animationSequence.length]); // Re-create interval if sequence length changes

    useEffect(() => {
        setCurrentImage(animationSequence[animationIndex]);
    }, [animationIndex, animationSequence]);

    return (
        <div className="character-container">
            <RetroDevice>
                <img src={currentImage} alt="Character" className="character-img" />
            </RetroDevice>
        </div>
    );
};

export default CharacterDisplay;
