from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Access the email and password
email = os.getenv('SOURCE_INFI_EMAIL')
password = os.getenv('SOURCE_INFI_PASSWORD')

app = Flask(__name__)
CORS(app)

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# IndiaMART Scraper
import requests
from bs4 import BeautifulSoup

# @app.route('/products/indiamart', methods=['GET'])
def search_indiamart(query):
    products = []

    # Fetching data from the MP API
    url_mp = f"https://dir.indiamart.com/search.mp?ss={query}"
    response_mp = requests.get(url_mp)

    if response_mp.status_code != 200:
        print(f"Failed to retrieve MP data: {response_mp.status_code}")
        return []

    soup_mp = BeautifulSoup(response_mp.content, 'html.parser')
    product_cards = soup_mp.find_all('div', class_='card brs5')
    print(f"IndiaMart: Found {len(product_cards)} IndiaMart products.")
    searchmpProductCards = 0
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

            # Append MP product details to the list
            searchmpProductCards+= 1
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
            print(f"Error processing a product card from MP data: {e}")
            continue
    print(f"IndiaMart: Added {searchmpProductCards} to IndiaMart products. ")
    # Fetching data from the RP API
    url_rp = f"https://dir.indiamart.com/api/search.rp?ss={query}"
    response_rp = requests.get(url_rp)

    url_rp = (
        f"https://dir.indiamart.com/api/search.rp?q={query}&options.start=14&search_type=&glusrid=223513042"
        f"&source=dir.search&geo_country_info.geo_country_name=India&geo_country_info.geo_country_code=IN"
        f"&implicit_info.for_country.type=India&implicit_info.for_country.data=IN"
    )

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Accept': 'application/json',
    }

    response_rp = requests.get(url_rp, headers=headers)

    if response_rp.status_code == 200:
        try:
            rp_data = response_rp.json()

    # Check if 'results' and 'more_results' exist in the response
            if "results" in rp_data:
                for result in rp_data["results"]:
                    if "more_results" in result:
                        for item in result["more_results"]:
                            product_title = item.get('title', "No title available")
                            price = item.get('itemprice', "No price available")
                            company_name = item.get('company', "No company name available")
                            product_link = item.get('desktop_title_url', "No link available")
                            product_image = item.get('zoomed_image', "No image available")
                            location = item.get('city', "No location available")
                            contact_number = item.get('contact_number', "No contact number available")

                            # Append RP product details to the list
                            products.append({
                                'name': product_title,
                                'price': price,
                                'company': company_name,
                                'url': product_link,
                                'image': product_image,
                                'location': location,
                                'contact_number': contact_number,
                            })

            else:
                print(f"Failed to retrieve RP data: {response_rp.status_code}")

        except ValueError as e:
            print(f"Error decoding JSON data from RP API: {e}")



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
        'limit': 100,
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
                if product_id== -1 :
                    continue
                product_url = f"https://app.roposoclout.com/product/{product_id}"

                # Append the cookie to the product URL for display on the website
                #cookie_for_display = 'countryPreference={"id":1,"label":"India","code":"IN"}; recSession=...; x-session-id=ac25aa44-48c6-4d4b-8671-55047522679b'
                product_url_with_cookie = f"{product_url}"
                    # ; {cookie_for_display}"

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

def login_to_sourceinfi(username, password):
    login_url = "https://seller.sourceinfi.com/"
    payload = {
        "email": username,
        "password": password,
        "submit": 'Log in'
        # Add other fields as required by the login form
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    session = requests.Session()  # Use a session to persist cookies
    response = session.post(login_url, headers=headers, data=payload)

    if response.status_code == 200:
        logger.debug("Login successful!")
        return session  # Return the session with cookies
    else:
        logger.error("Login failed!")
        return None

def search_sourceinfi(username, password, search_query):
    session = login_to_sourceinfi(username, password)

    if session is None:
        return []  # Return an empty list if login failed

    url = f"https://seller.sourceinfi.com/sellers-v1/product/index?filter%5Bproduct_search%5D={search_query}&filter%5Bsort%5D=new_arrival&filter%5Bproduct_status%5D=&filter%5Bcats_id%5D="

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    response = session.get(url, headers=headers)

    if response.status_code != 200:
        logger.error("Search request failed!")
        return []

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

def search_dropdash(search_query, page_number=1, page_size=18):
    url = f"https://api.dropdash.co/common/getallproducts?PageNumber={page_number}&PageSize={page_size}&product_name={search_query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        products = data['data']
        formatted_products = []
        for product in products:
            formatted_product = {
                'id': product['productID'],
                'name': product['title'],
                'image': product['product_image'],
                'price': product['b_2_b_price'],
                'category': product['category_name'],
                'stock': product['stock'],
                'seller_id': product['sellerId'],
            }
            formatted_products.append(formatted_product)
        return formatted_products
    else:
        print("Failed to fetch products:", response.status_code)
        return []


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
    sourceinfi_results = search_sourceinfi(email,password,query)
    dropdash_results = search_dropdash(query)

    # Sort by price within each source
    indiamart_sorted = sorted(indiamart_results, key=lambda x: x['price'] if x['price'] else float('inf'))
    roposo_sorted = sorted(roposo_results, key=lambda x: x['price'] if x['price'] else float('inf'))
    sourceinfi_sorted = sorted(sourceinfi_results, key=lambda x: x['price'] if x['price'] else float('inf'))
    dropdash_sorted = sorted(dropdash_results, key=lambda x: x['price'] if x['price'] else float('inf'))

    # Combine results in a format to display in three columns
    results = {
        'IndiaMart': indiamart_sorted,
        'RoposoClout': roposo_sorted,
        'SourceInfi': sourceinfi_sorted,
        'DropDash': dropdash_sorted
    }

    return jsonify(results)

if __name__ == '__main__':
    # app.run(debug=True, host='localhost', port=8000)
    app.run()
