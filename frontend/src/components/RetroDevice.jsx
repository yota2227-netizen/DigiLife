import React from 'react';

const RetroDevice = ({ children }) => {
    return (
        <div style={{ position: 'relative', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            {/* The Device SVG Layer */}
            <svg
                width="600"
                height="450"
                viewBox="0 0 600 450"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                style={{ maxWidth: '100%', height: 'auto', dropShadow: '0 20px 30px rgba(0,0,0,0.5)' }}
            >
                <defs>
                    {/* Stone Texture Filter */}
                    <filter id="stoneNoise" x="0%" y="0%" width="100%" height="100%">
                        <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="3" result="noise" />
                        <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.15 0" in="noise" result="coloredNoise" />
                        <feComposite operator="in" in="coloredNoise" in2="SourceGraphic" result="composite" />
                        <feBlend mode="multiply" in="composite" in2="SourceGraphic" />
                    </filter>

                    {/* Inner Shadow for Screen */}
                    <filter id="innerShadow">
                        <feOffset dx="0" dy="3" />
                        <feGaussianBlur stdDeviation="3" result="offset-blur" />
                        <feComposite operator="out" in="SourceGraphic" in2="offset-blur" result="inverse" />
                        <feFlood floodColor="black" floodOpacity="1" result="color" />
                        <feComposite operator="in" in="color" in2="inverse" result="shadow" />
                        <feComposite operator="over" in="shadow" in2="SourceGraphic" />
                    </filter>
                </defs>

                {/* Main Body Shell */}
                {/* Base Yellow Color #FFD600 (Yellow A700) */}
                <rect x="10" y="10" width="580" height="430" rx="40" fill="#FFD600" stroke="#F9A825" strokeWidth="4" />

                {/* Apply Texture */}
                <rect x="10" y="10" width="580" height="430" rx="40" fill="#FFD600" filter="url(#stoneNoise)" opacity="0.8" />

                {/* Crack Lines (Brick Pattern) */}
                <g stroke="#F9A825" strokeWidth="3" strokeLinecap="round" filter="url(#stoneShadow)">
                    {/* Horizontal Cracks */}
                    <path d="M10 120 H590" strokeOpacity="0.6" />
                    <path d="M10 240 H400" strokeOpacity="0.6" /> {/* Stop before buttons area */}
                    <path d="M450 240 H590" strokeOpacity="0.6" />
                    <path d="M10 360 H590" strokeOpacity="0.6" />

                    {/* Vertical Cracks (Staggered like bricks) */}
                    <path d="M150 10 V120" strokeOpacity="0.6" />
                    <path d="M450 10 V120" strokeOpacity="0.6" />
                    <path d="M300 120 V240" strokeOpacity="0.6" />
                    <path d="M150 240 V360" strokeOpacity="0.6" />
                    <path d="M450 240 V360" strokeOpacity="0.6" />
                    <path d="M300 360 V440" strokeOpacity="0.6" />
                </g>

                {/* Chips/Damage to corners (Decorative) */}
                <path d="M20 20 L40 25 L25 40 Z" fill="#F9A825" opacity="0.5" />
                <path d="M570 420 L550 415 L565 400 Z" fill="#F9A825" opacity="0.5" />

                {/* Screen Bezel Area (Left Side) */}
                <rect x="60" y="85" width="360" height="280" rx="15" fill="#e5e7eb" stroke="#9ca3af" strokeWidth="5" />

                {/* Screen Bezel Screws/Details */}
                <circle cx="75" cy="100" r="5" fill="#9ca3af" />
                <circle cx="75" cy="350" r="5" fill="#9ca3af" />
                <circle cx="405" cy="100" r="5" fill="#9ca3af" />
                <circle cx="405" cy="350" r="5" fill="#9ca3af" />

                {/* Button Area (Right Side) */}
                <g transform="translate(480, 100)">
                    {/* Button 1 */}
                    <circle cx="20" cy="50" r="30" fill="#9ca3af" stroke="black" strokeWidth="2" />
                    <circle cx="20" cy="45" r="25" fill="#d1d5db" /> {/* Highlight */}

                    {/* Button 2 */}
                    <circle cx="45" cy="130" r="30" fill="#9ca3af" stroke="black" strokeWidth="2" />
                    <circle cx="45" cy="125" r="25" fill="#d1d5db" />

                    {/* Button 3 */}
                    <circle cx="20" cy="210" r="30" fill="#9ca3af" stroke="black" strokeWidth="2" />
                    <circle cx="20" cy="205" r="25" fill="#d1d5db" />

                    {/* Small Reset Button */}
                    <circle cx="-10" cy="170" r="8" fill="#6b7280" />
                </g>
            </svg>

            {/* Screen Content Overlay */}
            <div style={{
                position: 'absolute',
                top: '50%',
                left: '40%', /* Correctly aligned to bezel center (240px / 600px) */
                transform: 'translate(-50%, -50%)',
                width: '320px', /* Match SVG bezel inner width roughy */
                height: '240px',
                backgroundColor: '#9cbda7',
                boxShadow: 'inset 0 0 20px rgba(0,0,0,0.3)',
                overflow: 'hidden',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                zIndex: 10
            }}>
                {children}
            </div>
        </div>
    );
};

export default RetroDevice;
