#from bot import Chat
from scraper import ProductScraper
from utils import load_from_json
#res = Chat().chat("I need a car part")

#res = Chat().chat("I need oil filter for my car")


res = load_from_json('result.json')
details = res["Oil filter"]
print(details)