"""
@date 1/11/19
@author dolphin
@description
- Allow the user to input the list of phrases via a Swagger.
- Request product info to B and get info from it.
- Allow the user to check to view the results.
"""

from fastapi import FastAPI, Query
from models import SearchTerms, ProductInfo, _SERVER_A_URL, _SERVER_B_URL
from typing import List
import requests
import aiohttp
import asyncio
from mydb import MyDB

mydb = MyDB()

app = FastAPI()

prodInfo = ProductInfo("test title", 41.6, 192.6)


@app.get("/")
def read_root():
    return {"Success": "This is server A on my test project using FastAPI."}

"""
Send asynchronous request to server B to scrap search_terms.
"""
def send_async_req(search_terms):
    req_sent = 0
    for term in search_terms:
        url = f"{_SERVER_B_URL}/amazon/{term}/scrap"
        requests.get(url)
        req_sent = req_sent + 1
    return req_sent

"""
Input query param: {search-phrase} is one of the phrases
in the list from the previous POST request.
Action: Price of product and Size of scrapped page
(without images, just text) retrieved from Server B.
"""
@app.post("/amazon/products-to-scan")
def products_to_scan(search_terms: List[str] = Query(..., title="Search terms", 
                    description="List of phrases that you want to scrap.")):
    # TODO send scrap request to server B
    loop = asyncio.new_event_loop()
    loop.run_in_executor(None, send_async_req, search_terms)
    return {"req_sent": len(search_terms)}


"""
Input query param: {search-phrase} is one of the phrases
in the list from the previous POST request.
Action: Price of product and Size of scrapped page
(without images, just text) retrieved from Server B.
"""
@app.get("/amazon/{search_phrase}/stats")
def products_stats(search_phrase: str = Query(None, title="Get stats that you request to scrap.",
                                              description="Get stats that you request to scrap.",
                                              min_length=5, max_length=200)):
    # TODO retrieve prodInfo from server B

    prodInfo = None
    try:
        scrapInfo = mydb.select_info_by_phrase(search_phrase)
        print(search_phrase)
        if scrapInfo is not None:
            print("success get")
            prodInfo = scrapInfo.prodInfo
            return {"title": prodInfo.title, "price": prodInfo.price, "page_size": prodInfo.page_size}
    except:
        print("Can't search info on database")
    return {"stats": "Not yet."}
