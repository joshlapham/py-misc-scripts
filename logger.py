#!/usr/bin/python

import logging

def Logger():
    """ Lazy init. a `logging` instance. """
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
        
if __name__ == '__main__':
    pass