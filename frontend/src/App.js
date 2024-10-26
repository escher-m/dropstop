import React, {useEffect} from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SearchPage from './pages/SearchPage';
import RoposoSorterPage from './pages/RoposoSorterPage';
import AboutUsPage from './pages/AboutUs';
import ContactUsPage from './pages/ContactUs';
import PrivacyPolicyPage from "./pages/PrivacyPolicy";
import BlogPage from './pages/Blog';
import './App.css';
import Footer from "./components/Footer";
import Header from "./components/Header";
import AllProductsPage from "./pages/AllProductsPage";

// New component that uses useLocation to manage header visibility
function Layout() {
    const location = useLocation();
    let containerClass = "content-container"; // Default class
    let bodyClass = "";
    if (location.pathname === '/source-from-suppliers') {
        bodyClass = "searchpage-body"; // Add a class for SearchPage
    }
    // Determine the page title based on the current route
    let pageTitle;
    switch (location.pathname) {
        case '/source-from-suppliers':
            pageTitle = "Source from Suppliers";
            break;
        case '/roposo-sorter':
            pageTitle = "Roposo Product Sorter";
            break;
        case '/about-us':
            pageTitle = "About Us";
            break;
        case '/contact-us':
            pageTitle = "Contact Us";
            break;
        case '/privacy-policy':
            pageTitle = "Privacy Policy";
            break;
        case '/blog':
            pageTitle = "Blog";
            break;
        case '/all-products':
            pageTitle = "All Products from";
            break;
        default:
            pageTitle = ""; // No title for home page
            containerClass += " full-width"; // Add a class for the home page
    }
    const RoposoSorterRedirect = () => {
        useEffect(() => {
            window.open("https://chromewebstore.google.com/detail/roposo-clout-product-sort/hgpbhpnknolocmdihnoenjemonfoibkk");
        }, []); // Empty dependency array ensures it runs only on mount

        return null; // Render nothing as it's just a redirect
    };

    // useEffect(() => {
    //     document.body.className = bodyClass;
    // }, [bodyClass]);

    return (
        <div className="full-page-wrapper">
            {/* Conditionally render the Header */}
            {location.pathname !== '/' && <Header pageTitle={pageTitle} />} {/* Don't show on the home page */}

            <main className="App">
                <div className={containerClass}>
                    {/* Logo as a home link */}
                    <Link to="/" className="home-logo"><span className="water-drop">💧</span></Link>

                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/source-from-suppliers" element={<SearchPage />} />
                        <Route path="/roposo-sorter" element={<RoposoSorterPage />} />
                        <Route path="/about-us" element={<AboutUsPage />} />
                        <Route path="/contact-us" element={<ContactUsPage />} />
                        <Route path="/privacy-policy" element={<PrivacyPolicyPage />} />
                        <Route path="/blog" element={<BlogPage />} />
                        <Route path="/all-products" element={<AllProductsPage />} />
                    </Routes>
                </div>
            </main>

            <Footer />
        </div>
    );
}

function App() {
    return (
        <Router basename="/dropstop">
            <Layout />
        </Router>
    );
}

export default App;
