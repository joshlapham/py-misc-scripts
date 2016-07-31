#!/bin/python

from subprocess import call, STDOUT
from os import devnull
from datetime import datetime
from time import strftime

def tprint(message):
    """ Prints a given `message` with a timestamp prepended. """
    
    print strftime("%c") + " - %s" % message
    
def file_timestamp():
    """ Returns a timestamp for use in a filename. """
    
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")

def call_cli(cli_commands):
    """ Calls command-line commands but supresses output. """
    
    try:
        FNULL = open(devnull, 'w')
        call(cli_commands, stdout=FNULL, stderr=STDOUT)

    except Exception as e:
        raise Exception(e)
        