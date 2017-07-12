#!/usr/bin/python3

from subprocess import check_output, CalledProcessError
from datetime import datetime
import threading
import time
import logger
import prowl_notify
import argparse

# TODO: don't use global for `logger`; use DI
logger = logger.Logger()

# TODO: add `notify` method to `prowl_notify` module?
def _notify(event_text, description_text):
   logger.info("Posting notification to Prowl")
   thread = threading.Thread(target=prowl_notify.post_to_prowl, args=["jFake", event_text, description_text])
   thread.start()
    
def _check_disk_space_for_path(path):
    cli = [
        'df',
        '-h',
        '%s' % path
    ]
    
    output = check_output(cli)
    space_used = output.split()[12]
    space_available = output.split()[13]
    drive_capacity = output.split()[14]
    return space_used, space_available, drive_capacity
    
def main(path, send_notification):
    used, available, capacity = _check_disk_space_for_path(path)
    msg = "Used: %s\nAvailable: %s\nCapacity: %s" % (used, available, capacity)
    logger.info(msg.split())
    
    # TODO: refactor this to a 'notify' method or something
    # Testing only
    if send_notification is True:
        now = datetime.now()
        msg_with_time = "%s\nTime: %s" % (msg, now.time())
        _notify("%s - Disk Usage" % path, msg_with_time)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Path to check disk usage for', required=True)
    parser.add_argument('--notify', help='Send notification with disk usage results', required=False, action='store_true', default=False)
    args = parser.parse_args()
    
    # TODO: testing only -- refactor logic to some sort of script that can do commands and post to prowl at certain intervals
    
    # NOTE - 15mins
    # TODO: add optional arg for `TIME_TO_WAIT`, although there should be a default value
    TIME_TO_WAIT = 900
    
    while True:
        try:
            main(args.path, args.notify)
            # TODO: `sleep` won't be called if there is an error; creates endless loop
            time.sleep(TIME_TO_WAIT)
            
        except KeyboardInterrupt:
            exit("User aborted script")
            
        except CalledProcessError as e:
            logger.error("Error calling command: %s" % e)
            time.sleep(TIME_TO_WAIT)
            
        except:
            exit("Something went wrong")
            
