from pydantic import BaseModel
# from dataclass import dataclass

_SERVER_A_URL = "http://localhost:3000"
_SERVER_B_URL = "http://localhost:3001"

class SearchTerms(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
 


class ProductInfo:
    def __init__(self, title, price, page_size):
        self.title = title
        self.price = price
        self.page_size = page_size


class ScrapInfo:
    def __init__(self, phrase, prodInfo):
        self.phrase = phrase
        self.prodInfo = prodInfo
