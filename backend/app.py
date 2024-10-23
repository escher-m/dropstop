from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)
CORS(app)

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# IndiaMART Scraper
def search_indiamart(query):
    url = f"https://dir.indiamart.com/search.mp?ss={query}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    product_cards = soup.find_all('div', class_='card brs5')

    products = []

    for card in product_cards:
        try:
            # Extracting the product title
            title_tag = card.find('div', class_='producttitle').find('a')
            product_title = title_tag.text.strip() if title_tag else "No title available"

            # Extracting the price
            price_tag = card.find('p', class_='price')
            price = price_tag.text.strip() if price_tag else "No price available"

            # Extracting company name
            company_tag = card.find('div', class_='companyname').find('a')
            company_name = company_tag.text.strip() if company_tag else "No company name available"

            # Extracting product link
            product_link = title_tag['href'] if title_tag else "No link available"

            # Extracting the product image
            image_tag = card.find('img', class_='productimg')
            product_image = image_tag['src'] if image_tag else "No image available"

            # Extracting location details
            location_tag = card.find('div', class_='newLocationUi')
            location = location_tag.text.strip() if location_tag else "No location available"

            # Extracting contact details
            contact_tag = card.find('span', class_='pns_h duet fwb')
            contact_number = contact_tag.text.strip() if contact_tag else "No contact number available"

            # Append product details to the list
            products.append({
                'name': product_title,
                'price': price,
                'company': company_name,
                'url': product_link,
                'image': product_image,
                'location': location,
                'contact_number': contact_number,
            })

        except Exception as e:
            print(f"Error processing a product card: {e}")
            continue

    return products

# Roposo Clout Scraper
def search_roposo_clout(query):
    logger.debug(f"Searching Roposo Clout for query: {query}")

    # Search API URL
    search_url = "https://api.cdn.myownshop.in/shopify/catalog/search/v2"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "country-code": "IN",
        "Content-Type": "application/json",
        "X-Session-Id": "ac25aa44-48c6-4d4b-8671-55047522679b"
    }

    params = {
        'offset': 0,
        'limit': 10,
        'sortType': '',
        'tilesInRow': 5,
        'catalogueName': query,
        'category': '',
        'subCategory': '',
        'leafCategory': '',
        'isAutocorrect': 'false',
        'countryCode': 'IN',
        'showBanner': 'true',
        'videoOffset': 3
    }

    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])

            product_list = []
            for product in products:
                product_id = product.get('productId')
                product_url = f"https://app.roposoclout.com/product/{product_id}"

                # Append the cookie to the product URL for display on the website
                cookie_for_display = 'countryPreference={"id":1,"label":"India","code":"IN"}; recSession=...; x-session-id=ac25aa44-48c6-4d4b-8671-55047522679b'
                product_url_with_cookie = f"{product_url}; {cookie_for_display}"

                # Use 'productName' and 'productPrice' fields, and include the first image from 'imageUrls'
                product_list.append({
                    "name": product.get('productName'),
                    "price": product.get('productPrice'),
                    "image": product['imageUrls'][0] if product.get('imageUrls') else None,  # Ensure imageUrls exists
                    "url": product_url_with_cookie
                })

            # Sort by price within Roposo Clout results
            sorted_products = sorted(product_list, key=lambda x: x['price'] if x['price'] else float('inf'))
            logger.debug(f"Found {len(sorted_products)} products in Roposo Clout.")
            return sorted_products

        elif response.status_code == 401:
            logger.warning("Authentication failed: Cookies or headers may be expired or invalid.")
            return [{'error': "Authentication failed: Cookies or headers may be expired or invalid."}]

        else:
            logger.error(f"Failed to fetch products. Status code: {response.status_code}")
            return [{'error': f"Failed to fetch products. Status code: {response.status_code}"}]

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Roposo Clout products: {str(e)}")
        return [{'error': f"An error occurred while fetching products: {str(e)}"}]
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return [{'error': f"An unexpected error occurred: {str(e)}"}]

# SourceInfi Scraper

def search_sourceinfi(search_query):
    url = f"https://seller.sourceinfi.com/sellers-v1/product/index?filter%5Bproduct_search%5D={search_query}&filter%5Bsort%5D=new_arrival&filter%5Bproduct_status%5D=&filter%5Bcats_id%5D="

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        # Add other headers as needed
    }

    cookies = {
        '_fw_crm_v': '53306e37-9e16-4bc3-9103-d5b805302ecd',
        '_ga': 'GA1.1.1548602773.1724329561',
        'ci_session': 'emnf62g50fgm2sq50em0o9qmhuf2ejnt',
        # Add any additional cookies here
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []

    # Find all product cards
    product_cards = soup.find_all('div', class_='card product-box')
    logger.debug(f"Found {len(product_cards)} products in SourceInfi.")

    for card in product_cards:
        title_element = card.find('h5', class_='title fw-500 mb-0 py-2')
        price_element = card.find('span', class_='d-block text-success fw-500')
        img_element = card.find('img', class_='lozad')
        link_element = card.find('a', href=True)

        # Initialize shipping variable
        shipping = None

        # Check for the shipping tag; it might be in different structures
        shipping_tag = card.find('p', text=lambda x: x and 'Shipping:' in x)
        if shipping_tag:
            shipping = shipping_tag.get_text(strip=True).replace('Shipping:', '').strip()

        if title_element and price_element and img_element and link_element:
            product = {
                'name': title_element.get_text(strip=True),
                'price': price_element.get_text(strip=True).replace('₹ ', '').replace(',', ''),  # Convert to plain number
                'image': img_element['data-src'] if 'data-src' in img_element.attrs else img_element['src'],
                'url': f"https://seller.sourceinfi.com{link_element['href']}",  # Prepend base URL
                'shipping': shipping  # Add shipping info if available
            }
            products.append(product)

    return products  # Return the list of products directly


# Route to handle search and display products in three columns, sorted by price within each source
@app.route('/')
def home():
    return "Flask is running with Gunicorn!"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # Search across all sources
    indiamart_results = search_indiamart(query)
    roposo_results = search_roposo_clout(query)
    sourceinfi_results = search_sourceinfi(query)

    # Sort by price within each source
    indiamart_sorted = sorted(indiamart_results, key=lambda x: x['price'] if x['price'] else float('inf'))
    roposo_sorted = sorted(roposo_results, key=lambda x: x['price'] if x['price'] else float('inf'))
    sourceinfi_sorted = sorted(sourceinfi_results, key=lambda x: x['price'] if x['price'] else float('inf'))

    # Combine results in a format to display in three columns
    results = {
        'IndiaMart': indiamart_sorted,
        'RoposoClout': roposo_sorted,
        'SourceInfi': sourceinfi_sorted
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run()
