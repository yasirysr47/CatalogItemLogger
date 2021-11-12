#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from collections import deque
from scrapper.postgre_db import PostgreSQL
from scrapper.config import url_head, catalog_url, re_manufacturer, re_category, re_model, re_part_text
 

class Scraper():
    def __init__(self):
        """initialize regex patterns, level details and DB connections"""
        self.levels_name = ["manufacture", "category", "model", "parts"]
        self.regex_pattern = {
            self.levels_name[0]: re_manufacturer,
            self.levels_name[1]: re_category,
            self.levels_name[2]: re_model,
            self.levels_name[3]: re_part_text
            }
        # start the connection to DB
        self.db = PostgreSQL()

    def get_urls_from_link(self, url: str, level: int = 0, url_que = deque()):
        """Start crawling through the given url and process all the valid links.
        And Store the processed links into DB.

        Args:
            url ([string]): URL to crawl
            level ([int]): Currrent Depth level of the Crawler. Default is 0.
            url_que ([type], optional): [description]. Defaults to deque().
        """
        if level > 3:
            return
        reqs = requests.get(url)
        # using lxml for fast processing
        soup = BeautifulSoup(reqs.text, 'lxml')
        # extract urls
        for link in soup.find_all('a'):
            full_url = url_head+link.get('href')
            level_name = self.levels_name[level]
            if level == 3:
                link_text = link.text.strip()
                if self.regex_pattern.get(level_name).match(link_text):
                    # process the url to get the parameter names and their values.
                    manufacturer, category, model = url.split('/')[-3:]
                    # part and part_category is the text data of the link.
                    part, part_category = [elem.strip() for elem in link_text.split('-', 1)]

                    record = (manufacturer, category, model, part, part_category,)
                    # save the record into DB
                    self.db.insert_record(record)
                    
            elif self.regex_pattern.get(level_name).match(full_url):
                url_que.append((full_url, level))

        # if que not empty, pop a url and goto next depth level.
        while len(url_que) > 0:
            next_link, level = url_que.popleft()
            self.get_urls_from_link(next_link, level+1, deque())

    def start(self):
        """Start the Crawler"""
        self.get_urls_from_link(catalog_url, 0, deque())
        # close the connection to DB
        self.db.disconnect()


if __name__ == "__main__":    
    obj = Scraper()
    obj.start()

