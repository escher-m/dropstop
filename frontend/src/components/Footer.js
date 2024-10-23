import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css'; // Optional: Add styles specific to the footer

const Footer = () => {
    return (
        <footer className="footer">
            <Link to="/about-us" className="footer-link">About Us</Link>
            <Link to="/contact-us" className="footer-link">Contact Us</Link>
            <Link to="/privacy-policy" className="footer-link">Privacy Policy</Link>
            <Link to="/blog" className="footer-link">Blog</Link>
        </footer>
    );
};

export default Footer;
