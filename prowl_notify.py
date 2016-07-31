#!/usr/bin python
# -*- coding: utf-8 -*-

from requests import post
from json import dumps
from argparse import ArgumentParser

# NOTE - `prowl_cfg.py` is ignored in `.gitignore`
import prowl_cfg as cfg

# TODO: do we still need this? For https support?
# import urllib3
# import urllib3.contrib.pyopenssl
# urllib3.contrib.pyopenssl.inject_into_urllib3()

HEADERS = {'content-type': 'application/json'}
API_URL = "https://api.prowlapp.com/publicapi/add"

def post_to_prowl(app_name, event_text, description_text):
    payload = {"apikey": cfg.PROWL_API_KEY, "application": app_name, "event": event_text, "description": description_text}
    response = post(API_URL, data=dumps(payload), headers=HEADERS)
    print(response)
    
if __name__ == '__main__':
    """ Posts a notification to the Prowl API. """

    args = ArgumentParser(description='Posts a notification to the Prowl API')
    args.add_argument('--app', help='App name for notification text', required=True)
    args.add_argument('--event', help='Event name for notification text', required=True)
    args.add_argument('--description', help='Description for notification text', required=True)
    args = args.parse_args()
    
    try:
        post_to_prowl(args.app, args.event, args.description)
        
    except Exception as e:
        print e
        
