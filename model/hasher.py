#!/usr/bin/env python3

import bcrypt

def get_pw_hash(plain_text_pw):
    salt = bcrypt.gensalt()
    #salt resets everytime the function is run
    # printint the salt here just to demonstrate whre it is in the returned hash
    print(f'salt:  {salt}')
    print(bcrypt.hashpw(plain_text_pw, salt))
    # this can and should be written one line
    # return bcrypt.hashpw(plain_text_pw, bcrypt.gensalt())

def check_pw(plain_text_pw, hashed_pw):
    #arguements need to be byte strings b'string'
    return bcrypt.checkpw(plain_text_pw, hashed_pw)

