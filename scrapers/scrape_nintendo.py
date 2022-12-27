#!/bin/python3

import os
import sys
import threading
import requests
from bs4 import BeautifulSoup

from prowl_notify import post_to_prowl


STR_IN_STOCK = 'In stock'
STR_NOT_IN_STOCK = 'Out of stock'


def _notify(event_text, description_text, prowl_title):
    thread = threading.Thread(target=post_to_prowl, args=[prowl_title, event_text, description_text])
    thread.start()


class Item:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.in_stock = None


def parse_page(item):
    url = item.url
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # TODO: this is the part of the script that is unique to Nintendo -- make everything else in script reusable for other sites/items to check
    elements = soup.find(class_='stock')
    span_elements = elements.find_all('span')

    # print(elements)
    # print(span_elements)

    for span in span_elements:
        # print(span.prettify())
        # print(span.contents[0])

        if span.contents[0] == STR_IN_STOCK:
            item.in_stock = True
        elif span.contents[0] == STR_NOT_IN_STOCK:
            item.in_stock = False


if __name__ == "__main__":
    try:
        item_name = os.environ['JL_ITEM_NAME']
        item_url = os.environ['JL_ITEM_URL']

    except KeyError as e:
        sys.exit('Environment variable not loaded: {}'.format(e))

    try:
        item_to_check = Item(item_name, item_url)

        parse_page(item_to_check)

        # TODO: send prowl notification if in stock
        # TODO: write last check datetime & result (if True/in stock) to file/DB -- persist it; so that we don't send another notification

        print('{} is in stock: {}'.format(
            item_to_check.name, item_to_check.in_stock))
        
        if item_to_check.in_stock is True:
            _notify('{} in stock'.format(item_to_check.name), 'Item is in stock', 'scrape_nintendo.py')

    except Exception as e:
        print('Exception when parsing page: {}'.format(e))
