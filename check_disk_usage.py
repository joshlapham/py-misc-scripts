#!/usr/bin/python3

import sys
import time
import subprocess
import datetime
import threading
import argparse
import logger
import prowl_notify

# TODO: add `notify` method to `prowl_notify` module? it is used by multiple scripts now
def _notify(event_text, description_text, logger):
   logger.info("Posting notification to Prowl")
   thread = threading.Thread(target=prowl_notify.post_to_prowl, args=["jFake", event_text, description_text])
   thread.start()
   
def _check_disk_space_for_path(path):
    cli = [
        'df',
        '-h',
        '{}'.format(path)
    ]
    
    output = subprocess.check_output(cli)
    space_used = output.split()[12]
    space_available = output.split()[13]
    drive_capacity = output.split()[14]
    return space_used, space_available, drive_capacity
    
def main(path, send_notification, logger):
    used, available, capacity = _check_disk_space_for_path(path)
    msg = "Used: {}\nAvailable: {}\nCapacity: {}".format(used, available, capacity)
    logger.info(msg.split())
    
    if send_notification is True:
        now = datetime.datetime.now()
        msg_with_time = "{}\nTime: {}".format(msg, now.time())
        _notify("{} - Disk Usage".format(path), msg_with_time, logger)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Path to check disk usage for', required=True)
    parser.add_argument('--notify', help='Send notification with disk usage results', required=False, action='store_true', default=False)
    args = parser.parse_args()
    
    logger = logger.Logger()
    
    # NOTE - 15mins
    # TODO: add optional arg for `TIME_TO_WAIT`, although there should be a default value
    TIME_TO_WAIT = 900
    
    while True:
        try:
            main(args.path, args.notify, logger)
            # TODO: `sleep` won't be called if there is an error; creates endless loop
            time.sleep(TIME_TO_WAIT)
            
        except subprocess.CalledProcessError as e:
            logger.error("Error calling command: {}".format(e))
            time.sleep(TIME_TO_WAIT)
            
        except KeyboardInterrupt:
            sys.exit("User aborted script")
            
        except Exception as e:
            sys.exit("Error: {}".format(e))
            
