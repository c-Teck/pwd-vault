#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:04:32 2021

@author: cybree
"""

# from hashlib import sha256
from Cryptodome.Cipher import AES 
from pbkdf2 import PBKDF2
import hashlib
from base64 import b64encode, b64decode
from dotenv import load_dotenv
import os
import string
import secrets


load_dotenv()
# Enter salt here in ******* field. Enter binary string.
# salt = b'********'


def salt():
    try:
        os.environ['SALT'] = secrets.token_hex(64)
    except Exception as error:
        print('ERROR', error)


def password_gen(password_length):

    characters = string.ascii_letters + string.digits

    secure_password = ''.join(secrets.choice(characters) for i in range(password_length))

    return secure_password


def master_password_gen():
    # os.environ["SALT"] = salt().
    master_pwd = input("Enter your master password to use for your vault : ").encode()
    two_factor = os.environ.get("SALT").encode()
    compile_factor_together = hashlib.sha256(master_pwd + two_factor).hexdigest()
    print("\n[+] Generating your hashed password...\n...\n[+] Your hashed password has been generated")
    hashed = (str(compile_factor_together))
    os.environ["MASTER"] = hashed


def query_master_pwd(master_password, second_fa_location):

    # Enter password hash in ******** field. Use PBKDF2 and Salt from above.
    # Use master_password_hash_generator.py to generate a master password hash.
    master_password_hash = os.environ.get("MASTER")

    compile_factor_together = hashlib.sha256(master_password + second_fa_location).hexdigest()

    if compile_factor_together == master_password_hash: 
        return True
    else:
        return False


def encrypt_password(password_to_encrypt, master_password_hash): 
    salt_auth = os.environ.get('SALT')
    key = PBKDF2(str(master_password_hash), salt_auth).read(32)
    
    data_convert = str.encode(password_to_encrypt)

    cipher = AES.new(key, AES.MODE_EAX) 

    nonce = cipher.nonce

    ciphertext, tag = cipher.encrypt_and_digest(data_convert) 

    add_nonce = ciphertext + nonce

    encoded_ciphertext = b64encode(add_nonce).decode()

    return encoded_ciphertext


def decrypt_password(password_to_decrypt, master_password_hash): 
    
    if len(password_to_decrypt) % 4:
     
        password_to_decrypt += '=' * (4 - len(password_to_decrypt) % 4)

    convert = b64decode(password_to_decrypt)
    salt_auth = os.environ.get('SALT')
    key = PBKDF2(str(master_password_hash), salt_auth).read(32)

    nonce = convert[-16:]

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    plaintext = cipher.decrypt(convert[:-16]) 

    return plaintext
