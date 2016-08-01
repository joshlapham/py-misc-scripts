#!/bin/python

from subprocess import check_output, CalledProcessError
from time import sleep
from helpers import tprint
from argparse import ArgumentParser
from sys import exit

# Default time to wait between ping attempts
TIME_TO_WAIT = 60

def do_reboot():
    """ Reboots machine. """

    try:
        check_output(['sudo', 'reboot'])

    except CalledProcessError:
        tprint("Error when trying to reboot")
        
    except KeyboardInterrupt:
        tprint("User aborted reboot")

if __name__ == "__main__":
    """ Pings a given host just once every so often; and reboots machine if ping fails. """
    
    args = ArgumentParser(description="Pings a given host just once every so often; and reboots machine if ping fails")
    args.add_argument("--host", help="Host address to ping", required=True)
    args.add_argument("--time-to-wait", help="Time to wait between ping attempts", required=False)
    args = args.parse_args()
    
    if args.time_to_wait is not None:
        TIME_TO_WAIT = args.time_to_wait
        
    while True:
        try:
            check_output(['ping', '-c1', args.host])
            sleep(TIME_TO_WAIT)

        except CalledProcessError:
            tprint("Host is down, rebooting ..")
            do_reboot()
            break
            
        except KeyboardInterrupt:
            exit("User aborted script")
            
        except:
            exit("Something went wrong")
            