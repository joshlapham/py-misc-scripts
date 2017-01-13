#!/usr/bin python

from requests import post
from json import dumps
import kodi_cfg as cfg

HEADERS = {'Content-Type': 'application/json'}
KODI_JSON_RPC_URL = "http://" + cfg.KODI_USERNAME + ":" + cfg.KODI_PASSWORD + "@" + cfg.KODI_HOST + ":" + str(cfg.KODI_PORT) + "/jsonrpc"

def do_video_library_scan(logger=None):
    payload = {"jsonrpc": cfg.KODI_JSON_RPC_VERSION, "method": "VideoLibrary.Scan", "id": "mybash"}
    response = post(KODI_JSON_RPC_URL, data=dumps(payload), headers=HEADERS)
    
    if logger:
        logger.info(response)
    
    return response
        
def do_video_library_clean(logger=None):
    payload = {"jsonrpc": cfg.KODI_JSON_RPC_VERSION, "method": "VideoLibrary.Clean", "id": "mybash"}
    response = post(KODI_JSON_RPC_URL, data=dumps(payload), headers=HEADERS)
    
    if logger:
        logger.info(response)
        
    return response
    
if __name__ == '__main__':
    """ Makes an API call to Kodi Media Center to clean and update the video library. """
    
    try:
        do_video_library_scan()
        do_video_library_clean()
        
    except Exception as e:
        print "Error : %s" % e