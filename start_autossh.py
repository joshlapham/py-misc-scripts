#!/bin/python

from subprocess import check_output, CalledProcessError
from time import sleep
from helpers import tprint

# NOTE - `autossh_cfg.py` is ignored in `.gitignore`
import autossh_cfg as cfg

CLI_START = [
    '/usr/local/bin/autossh',
    '-M', cfg.REMOTE_MONITOR_PORT,
    '-f',
    '-p', cfg.SSH_REMOTE_PORT, '-N', '-R', '%s:localhost:22' % cfg.REMOTE_PORT_TO_OPEN, cfg.SSH_HOST
]

CLI_CHECK = [
    '/usr/bin/pgrep',
    'autossh'
]
    
def startRunning():
    """ Starts the autossh session. """
    
    try:
        check_output(CLI_START)
        tprint("Started autossh")

    except CalledProcessError as e:
        tprint("Error when trying to start autossh : %s" % e)
        
def checkIfRunning():
    """ Checks if an autossh process is currently running; starts one if not. """
    
    try:
        check_output(CLI_CHECK)

    except CalledProcessError:
        tprint("autossh is not running; restarting")
        startRunning()
        
if __name__ == "__main__":
    """ Checks if an autossh session is currently running; if not it will start one. """
    
    try:
        while True:
            checkIfRunning()
            sleep(60)

    except KeyboardInterrupt:
        tprint("User aborted script")
        