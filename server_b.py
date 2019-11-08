"""
@date 1/11/19
@author dolphin
@description
- Scrapes the price and HTML page size with the search phrase.
- Store scrapped data and manipulate it.
"""

from fastapi import FastAPI, Query
from datetime import datetime, date
from models import ProductInfo, ScrapInfo
from scraper import Scraper
from mydb import MyDB

app = FastAPI()

mydb = MyDB()

scrapInfoList = []


@app.get("/")
def read_root():
    return {"Success": "This is server B on my test project using FastAPI."}


"""
Input query param: {search-phrase} is one of the phrases 
in the list from the previous POST request.
Action: The search-phrase is searched and the 1st product 
in the results list is scrapped. The collected data is the product price 
and the size of the scrapped page (html only, without images).
"""
@app.get("/amazon/{search_phrase}/scrap")
async def do_scrap(search_phrase: str = Query(None, min_length=1, max_length=200)):
    # TODO scrape with search_phrase

    prodInfo = None
    try:
        scrapInfo = mydb.select_info_by_phrase(search_phrase)
        if scrapInfo is not None:
            prodInfo = scrapInfo.prodInfo
            return {"title": prodInfo.title, "price": prodInfo.price, "page_size": prodInfo.page_size}
    except:
        print("Can't search info on database")

    scraper = Scraper()

    prodInfo = scraper.do_scrap(search_phrase)

    scrapInfo = ScrapInfo(search_phrase, prodInfo)
    scrapInfoList.append(scrapInfo)
    try:
        mydb.add_scrape_info(scrapInfo)
    except:
        print("Can't add info to database")

    return {"title": prodInfo.title, "price": prodInfo.price, "page_size": prodInfo.page_size}


"""
Input query param: {search-phrase} is one of the phrases in the list 
from the previous POST request.
Action: Delete the item from the stored results.
"""
@app.delete("/amazon/{search_phrase}")
def delete_prod_info(search_phrase: str = Query(None, min_length=1, max_length=200)):
    try:
        del_cnt = mydb.delete_scrape_info(search_phrase)
        return {"del_cnt", del_cnt}
    except:
        print("Can't delete from database")
        return {"del_cnt", 0}
