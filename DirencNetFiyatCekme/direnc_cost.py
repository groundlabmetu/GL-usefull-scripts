import requests
from bs4 import BeautifulSoup

def get_product_price(url):
    # Fetch the web page
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        return "Failed to retrieve the page"

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the price element and extract its text
    price_element = soup.find('span', class_='product-price-tl')
    if price_element:
        return price_element.text.strip()
    else:
        return "Price not found"

# Example usage
file_path = 'component_urls.txt'

with open(file_path, 'r') as file:
    for line in file:       
        url = line.strip()
        price = get_product_price(url)
        print(price)



# url = 'https://www.direnc.net/s-140-antistatik-esd-lehimleme-mati'
# print(get_product_price(url))


