#!/usr/bin/python3

from argparse import ArgumentParser
from threading import Thread
from requests import post
from json import dumps
import kodi_cfg as cfg

HEADERS = {'Content-Type': 'application/json'}
KODI_JSON_RPC_URL = "http://" + cfg.KODI_USERNAME + ":" + cfg.KODI_PASSWORD + "@" + cfg.KODI_HOST + ":" + str(cfg.KODI_PORT) + "/jsonrpc"

# TODO: right now we're calling `print response` to ensure the API calls actually happen; don't do this. Must be to do with `threading` library.

def do_video_library_scan():
    payload = {"jsonrpc": cfg.KODI_JSON_RPC_VERSION, "method": "VideoLibrary.Scan", "id": "mybash"}
    response = post(KODI_JSON_RPC_URL, data=dumps(payload), headers=HEADERS)
    print(response)
    return response
    
def do_video_library_clean():
    payload = {"jsonrpc": cfg.KODI_JSON_RPC_VERSION, "method": "VideoLibrary.Clean", "id": "mybash"}
    response = post(KODI_JSON_RPC_URL, data=dumps(payload), headers=HEADERS)
    print(response)
    return response
    
if __name__ == '__main__':
    """ Makes an API call to Kodi Media Center to update/clean the video library. """
    
    args = ArgumentParser()
    args.add_argument("--clean", help="Make API call to clean the video library", required=False, action="store_true")
    args = args.parse_args()
    
    try:
        # TODO: `response` variables don't do anything here
        
        update_thread = Thread(target=do_video_library_scan)
        update_thread.start()
        update_response = update_thread.join()
        print(update_response)
        
        if args.clean is True:
            clean_thread = Thread(target=do_video_library_clean)
            clean_thread.start()
            clean_response = clean_thread.join()
            print(clean_response)
            
    except Exception as e:
        print("Error: {}".format(e))