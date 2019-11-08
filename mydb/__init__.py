# -*- coding: utf-8 -*-
""" This package provide you sqlite connection and
 allows you to create sqlite database.
You can select, add and delete scraped info with sqlite database.
"""
from builtins import object
import sqlite3
from sqlite3 import Error
from models import ScrapInfo, ProductInfo

__version__ = '1.0.0'

_DB_FILE = "/home/dolphin/works/projects/python-fastapi/mydb/pythonsqlite.db"
_TABLE_NAME = "amazon_scrape"

class MyDB(object):
    """Class of the database"""

    def __init__(self):
        self.conn = None
        # self.create_connection()

    def create_connection(self):
        """ create a database connection to the SQLite 
            specified by the db_file and create table if not exists.
        """
        try:
            self.conn = sqlite3.connect(_DB_FILE)
            self.create_result_table()
        except Error as e:
            print(e)
            print("DB Connection error.")
            return None

    def close_connection(self):
        """ close a database connection to the SQLite.
        """
        try:
            self.conn.close()
        except Error as e:
            print(e)
            print("DB disonnection error.")
            return None

    def select_info_by_phrase(self, phrase):
        """
        Query scraped info by phrase
        :param phrase: phrase for search
        :return: scraped info {phrase, title, price, page_size}
        """
        self.create_connection()
        try:
            cur = self.conn.cursor()
        except Error as e:
            print(e)
            print("Can't get db cursor.")

        sql = f"SELECT phrase,title,price,page_size FROM {_TABLE_NAME} WHERE phrase='{phrase}'"
        cur.execute(sql)

        rows = cur.fetchall()

        if len(rows) == 0:
            cur.close()
            self.close_connection()
            return None

        scrapeInfo = ScrapInfo(
            rows[0][0], ProductInfo(rows[0][1], rows[0][2], rows[0][3]))

        cur.close()
        self.close_connection()
        return scrapeInfo

    def create_result_table(self):
        """
        Create table for storing scraped data 
        {id, phrase, title, price, page_size}
        """
        cur = self.conn.cursor()
        try:
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {_TABLE_NAME}(id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    phrase varchar(50), title varchar(150), price float, page_size int)")
        except Error as e:
            print("Can't create table")
            print(e)

        cur.close()

    def add_scrape_info(self, scrapInfo):
        """
        Add scraped data into info table
        {id, phrase, title, price, page_size}
        @return: count of added products.
        """
        add_cnt = 0
        print("my step")
        if self.select_info_by_phrase(scrapInfo.phrase) is not None:
            print("Data exist")
        else:
            self.create_connection()
            cur = self.conn.cursor()
            sql = f"INSERT INTO {_TABLE_NAME}('phrase', 'title', 'price', 'page_size') \
                    VALUES('{scrapInfo.phrase}','{scrapInfo.prodInfo.title}',\
                        {scrapInfo.prodInfo.price},{scrapInfo.prodInfo.page_size})"
            
            print(sql)
            cur.execute(sql)
            add_cnt = cur.rowcount
            self.conn.commit()
            cur.close()
            self.close_connection()
        return add_cnt

    def delete_scrape_info(self, phrase):
        """
        Delete scraped data from info table
        @return: count of deleted products.
        """
        del_cnt = 0
        self.create_connection()
        cur = self.conn.cursor()
        sql = f"DELETE FROM {_TABLE_NAME} WHERE phrase = '{phrase}'"
        cur.execute(sql)
        del_cnt = cur.rowcount
        self.conn.commit()
        cur.close()
        self.close_connection()
        return del_cnt
