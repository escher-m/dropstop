import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';  // Style your homepage elements here

function HomePage() {
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
        <div className="homepage">
            {/* Title and byline */}
            <header className="header">
                <h1 className="title">
                    Drop<span className={`replace ${isRotating ? 'rotate' : ''}`}>{word}</span>
                    <span className="water-drop">💧</span>
                </h1>
                <h2 className="byline">One stop for sourcing winning products</h2>
            </header>
            {/* Navbar separated with its own wrapper and light grey background */}
            <div className="navbar-wrapper">
                <nav className="navbar">
                    <Link to="/source-from-suppliers" className="nav-link">Source from Suppliers</Link>
                    <div className="dropdown">
                        <span className="nav-link">Free Tools</span>
                        <div className="dropdown-content">
                            <Link to="/roposo-sorter" className="dropdown-item">Roposo Product Sorter</Link>
                        </div>
                    </div>
                </nav>
            </div>
            {/* USP content */}
            <div className="homebody">
                <div className="usp-container">
                    <div className="usp">
                        <img src="./homepage/usp1.jpg" alt="USP 1" className="usp-logo"/>
                        <p>Find Winning Products Quickly</p>
                    </div>
                    <div className="usp">
                        <img src="./homepage/usp2.jpg" alt="USP 2" className="usp-logo"/>
                        <p>Best Supplier Integration</p>
                    </div>
                    <div className="usp">
                        <img src="./homepage/usp3.jpg" alt="USP 3" className="usp-logo"/>
                        <p>Real-Time Price Comparisons</p>
                    </div>
                    <div className="usp">
                        <img src="./homepage/usp6.jpg" alt="USP 4" className="usp-logo"/>
                        <p>User-Friendly Product Sorting Tools</p>
                    </div>
                    <div className="usp">
                        <img src="./homepage/usp4.jpg" alt="USP 5" className="usp-logo"/>
                        <p>Expert Insights and Resources</p>
                    </div>
                    <div className="usp">
                        <img src="./homepage/usp9.jpg" alt="USP 6" className="usp-logo"/>
                        <p>Dedicated Customer Support</p>
                    </div>
                </div>
            </div>

            {/* Footer */}
        </div>
    );
}

export default HomePage;
