#!/usr/bin python

from requests import post
from json import dumps

# NOTE - `kodi_cfg.py` is ignored in `.gitignore`
import kodi_cfg as cfg

HEADERS = {'content-type': 'application/json'}
KODI_JSON_RPC_URL = "http://" + cfg.KODI_USERNAME + ":" + cfg.KODI_PASSWORD + "@" + cfg.KODI_HOST + ":" + str(cfg.KODI_PORT) + "/jsonrpc"

def do_video_library_scan():
    payload = {"jsonrpc": "2.0", "method": "VideoLibrary.Scan"}
    response = post(KODI_JSON_RPC_URL, data=dumps(payload), headers=HEADERS)
    print(response)
    
def do_video_library_clean():
    payload = {"jsonrpc": "2.0", "method": "VideoLibrary.Clean"}
    response = post(KODI_JSON_RPC_URL, data=dumps(payload), headers=HEADERS)
    print(response)
    
if __name__ == '__main__':
    """ Makes an API call to Kodi media center to clean and perform an update on the video library. """
    
    try:
        do_video_library_scan()
        do_video_library_clean()
        
    except Exception as e:
        print "Error : %s" % e
         