import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SearchPage.css';

const SearchPage = () => {
    const [results, setResults] = useState({});
    const [visibleProducts, setVisibleProducts] = useState({});
    const [currentStartIndex, setCurrentStartIndex] = useState({});
    const [productsPerRow, setProductsPerRow] = useState(3);
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false); // Loading state

    // Calculate number of products to display per row based on the screen width
    const calculateProductsPerRow = () => {
        const containerWidth = window.innerWidth;
        const productWidth = 220;  // Width of the product
        const spaceBetween = 10;   // Gap between products
        const containerPadding = 40; // Left and right padding (20px each)

        const totalWidth = productWidth + spaceBetween;
        const availableWidth = containerWidth - containerPadding; // Consider container padding
        const numberOfProducts = Math.floor(availableWidth / totalWidth);

        setProductsPerRow(Math.max(numberOfProducts, 1)); // Ensure at least one product
    };

    useEffect(() => {
        calculateProductsPerRow();
        window.addEventListener('resize', calculateProductsPerRow);
        document.documentElement.style.setProperty('--products-per-row', productsPerRow);
        return () => window.removeEventListener('resize', calculateProductsPerRow);
    }, [productsPerRow]);

    const handleSearch = async () => {
        setLoading(true);  // Start loading
        try {
            const response = await axios.get(`https://dropstop.onrender.com/search?q=${query}`);
            setResults(response.data);
            const initialVisible = {};
            const initialIndex = {};
            Object.keys(response.data).forEach(source => {
                initialVisible[source] = productsPerRow;
                initialIndex[source] = 0;
            });
            setVisibleProducts(initialVisible);
            setCurrentStartIndex(initialIndex);
        } catch (error) {
            console.error("Error fetching the search results:", error);
        } finally {
            setLoading(false);  // Stop loading
        }
    };

    const nextProducts = (source) => {
        const remainingProducts = results[source].length - currentStartIndex[source];
        if (remainingProducts > productsPerRow) {
            setCurrentStartIndex(prevIndex => ({
                ...prevIndex,
                [source]: prevIndex[source] + productsPerRow,
            }));
        }
    };

    const prevProducts = (source) => {
        if (currentStartIndex[source] > 0) {
            setCurrentStartIndex(prevIndex => ({
                ...prevIndex,
                [source]: Math.max(prevIndex[source] - productsPerRow, 0),
            }));
        }
    };

    const showAllProducts = (source) => {
        const allProducts = JSON.stringify(results[source]); // Convert the product array to a string
        const encodedProducts = encodeURIComponent(allProducts); // Encode it for the URL
        window.open(`/all-products?products=${encodedProducts}&source=${source}`, '_blank');
    };


    return (
        <div className="searchpage">
            <h1 className="byline">One stop for sourcing winning products</h1>

            <div className="search-container">
                <input
                    className="search-input"
                    type="text"
                    placeholder="Search..."
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                />
                <button className="search-button" onClick={handleSearch}>Search</button>
            </div>

            {/* Loading animation */}
            {loading && (
                <div className="loading-overlay">
                    <div className="loading-spinner"></div>
                </div>
            )}

            <div className="results-container">
                {Object.keys(results).map(source => (
                    <div className="source-row" key={source}>
                        <div className="source-header">
                            <h2>{source}</h2>
                            <img className="source-logo" src={`/logos/${source}.png`} alt={`${source} logo`} />
                            <div className="source-controls">
                                <button className="show-all-button" onClick={() => showAllProducts(source)}>
                                    Show All
                                </button>
                                <div className="arrow-buttons">
                                    <button className="arrow-button left" onClick={() => prevProducts(source)} disabled={currentStartIndex[source] === 0}>
                                        &lt;
                                    </button>
                                    <button className="arrow-button right" onClick={() => nextProducts(source)} disabled={currentStartIndex[source] + productsPerRow >= results[source].length}>
                                        &gt;
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div className="product-row">
                            <div className="products">
                                {results[source].slice(currentStartIndex[source], currentStartIndex[source] + productsPerRow).map(product => (
                                    <div className="product-box" key={product.id}>
                                        <a href={product.url} target="_blank" rel="noopener noreferrer">
                                            <img className="product-image" src={product.image} alt={product.name} />
                                            <p>{product.name}</p>
                                            <p>{product.price}</p>
                                        </a>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SearchPage;
