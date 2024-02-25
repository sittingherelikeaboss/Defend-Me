import string
import random
import bcrypt

def encrpytPassword(password):
    # converting password to array of bytes 
    bytes = password.encode('utf-8') 
    
    # generating the salt 
    salt = bcrypt.gensalt() 
    
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt)
    
    return hash