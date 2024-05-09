import requests
from bs4 import BeautifulSoup
import json

class ProductScraper:
    def __init__(self, products_path):
        with open(products_path, "r", encoding="utf-8") as f:
            self.products = [line.strip() for line in f.readlines()]
        self.base_url = "https://jiji.ng/motorcycles-and-scooters?query=car%20{}"
        self.urls = [self.base_url.format(product.replace(' ', '%20')) for product in self.products]

    def get_html_page(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def scrape(self):
        result = {}
        parent_class = "b-list-advert__gallery__item js-advert-list-item"
        for product, url in zip(self.products, self.urls):
            soup = self.get_html_page(url)
            #source_url_element = text.find_all("div", class_="b-list-advert__gallery__item js-advert-list-item")
            price_elements = soup.find_all(class_=parent_class)
            product_details = []
            for element in price_elements:
                price_element = element.find(class_="qa-advert-price")
                title_element = element.find("div", class_="b-advert-title-inner qa-advert-title b-advert-title-inner--div")
                source_url_element = element.find('a').get('href')
                if price_element and title_element and source_url_element:
                    price = price_element.text.strip()
                    title = title_element.text.strip()
                    source_url = "https://jiji.ng" + source_url_element
                    name_price_url_dict = {"name": title, "price": price,"source_url": source_url}
                    product_details.append(name_price_url_dict)
            result[product] = product_details
        return result

    def save_to_json(self, result, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

# Usage
scraper = ProductScraper("products.txt")
result = scraper.scrape()
scraper.save_to_json(result, 'result.json')
#loaded_result = scraper.load_from_json('result.json')