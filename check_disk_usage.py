#!/usr/bin/python3

from subprocess import check_output, CalledProcessError
from threading import Thread
from datetime import datetime
from time import sleep
from prowl_notify import post_to_prowl
from logger import Logger

# TODO: don't use global for `logger`; use DI
logger = Logger()

# TODO: testing only -- add `notify` method to `prowl_notify` module?
def _notify(event_text, description_text):
    logger.info("Posting notification to Prowl")
    thread = Thread(target=post_to_prowl, args=["jFake", event_text, description_text])
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
    
def main():
    # TODO: don't harcode `path`
    path = "/Volumes/Media 1"
    used, available, capacity = _check_disk_space_for_path(path)
    msg = "Used: %s\nAvailable: %s\nCapacity: %s" % (used, available, capacity)
    logger.info(msg.split())
    
    # Testing only
    now = datetime.now()
    msg_with_time = "%s\nTime: %s" % (msg, now.time())
    _notify("%s - Disk Usage" % path, msg_with_time)
    
if __name__ == '__main__':
    # TODO: testing only -- refactor logic to some sort of script that can do commands and post to prowl at certain intervals
    
    # NOTE - 15mins
    TIME_TO_WAIT = 900
    
    while True:
        try:
            main()
            # TODO: `sleep` won't be called if there is an error; creates endless loop
            sleep(TIME_TO_WAIT)
            
        except KeyboardInterrupt:
            exit("User aborted script")
            
        except CalledProcessError as e:
            logger.error("Error calling command: %s" % e)
            sleep(TIME_TO_WAIT)
            
        except:
            exit("Something went wrong")
            
