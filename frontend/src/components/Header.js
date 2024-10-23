import React, { useEffect, useState } from 'react';
import './Header.css';

const Header = ({ pageTitle }) => {
    const [word, setWord] = useState('Stop');
    const [isRotating, setIsRotating] = useState(false);

    useEffect(() => {
        const interval = setInterval(() => {
            setIsRotating(true);
            setTimeout(() => {
                setWord(prev => prev === 'Stop.' ? 'Ship?' : 'Stop.');
                setIsRotating(false);
            }, 1000); // Duration of the rotation
        }, 2000); // Changes every 2 seconds

        return () => clearInterval(interval); // Cleanup on unmount
    }, []);

    return (
        <header className="header-small">
            <div className="page-title-container">
                <h1 className="page-title">{pageTitle}</h1>
            </div>
            <div className="header-title">
                <h1 className="title-small">
                    Drop<span className={`replace ${isRotating ? 'rotate' : ''}`}>{word}</span>
                    <span className="water-drop">💧</span>
                </h1>
            </div>
        </header>
    );
};

export default Header;
