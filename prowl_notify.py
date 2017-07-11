#!/usr/bin python
# -*- coding: utf-8 -*-

from requests import post
from argparse import ArgumentParser
import prowl_cfg as cfg

HEADERS = {'content-type': 'application/json'}
API_URL = "https://api.prowlapp.com/publicapi/add"

def post_to_prowl(app_name, event_text, description_text):
    params = {'apikey': cfg.PROWL_API_KEY, 'application': app_name, 'event': event_text, 'description': description_text}
    # TODO: implement error handling here -- `try-except`
    post(API_URL, params=params, headers=HEADERS)
    
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
        print(e)
        