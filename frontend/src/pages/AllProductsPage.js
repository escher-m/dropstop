import React from 'react';
import { useLocation } from 'react-router-dom';
import './AllProductsPage.css';

const AllProductsPage = () => {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);

    const source = queryParams.get('source');
    const products = JSON.parse(queryParams.get('products') || '[]'); // Parse products from query params

    console.log("Source:", source);
    console.log("Products:", products); // Log the products to debug

    return (
        <div className="all-products-page">
            <div className="all-results-container">
                <div className="all-source-row">
                    <div className="all-source-header">
                        <h2>{source}</h2>
                        <img className="all-source-logo" src={`/logos/${source}.png`} alt={`${source} logo`} />
                    </div>
                    <div className="all-product-row">
                        <div className="all-products">
                            {products.length > 0 ? (
                                products.map(product => (
                                    <div className="all-product-box" key={product.id}>
                                        <a href={product.url} target="_blank" rel="noopener noreferrer">
                                            <img className="all-product-image" src={product.image} alt={product.name} />
                                            <p>{product.name}</p>
                                            <p>{product.price}</p>
                                        </a>
                                    </div>
                                ))
                            ) : (
                                <p>No products available for this source.</p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AllProductsPage;
