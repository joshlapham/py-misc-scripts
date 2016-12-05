#!/bin/python

import bcrypt

if __name__ == '__main__':
    password = '123456789'
    
    # Hash a password for the first time, with a randomly-generated salt
    # hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    # gensalt's log_rounds parameter determines the complexity.
    # The work factor is 2**log_rounds, and the default is 12
    # hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
    
    # print hashed
    
    hashed = '$2b$10$vsI9EAKTstas5lrMLaDiVez/0Ma7m4U6RGGJvNuUZFlbA1zADX3ZW'

    # Check that an unencrypted password matches one that has
    # previously been hashed
    if bcrypt.hashpw(password, hashed) == hashed:
        print "It matches"
    else:
        print "It does not match"