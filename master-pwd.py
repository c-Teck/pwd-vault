#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:04:32 2021

@author: cybree
"""

#from hashlib import sha256
from Cryptodome.Cipher import AES 
from pbkdf2 import PBKDF2
import hashlib
from base64 import b64encode, b64decode
#from password_gen_func import master_password_gen
import smtplib, ssl



# Enter salt here in ******* field. Enter binary string.
salt = b'********'



def master_password_gen():

    master_pwd = input("Enter your master password to use for your vault : ").encode()

    compile_factor_together = hashlib.sha256(master_pwd).hexdigest()
    print("\n[+] Generating your hashed password...\n...\n[+] Your password has been generated")

    return (str(compile_factor_together))


def signup():
    Email = input("[+] Enter your email address to use with this vault : ")
    Username = input(" [+] What nickname should i call you : ")
    sender = "pwdvault@gmail.com"
    receiver = Email
    port = 587
    smtp_server = 'smtp.gmail.com'
    pwd = 'passw0RD'
    message = """\
    Subject: WELCOME TO PASSWORD MANAGER VAULT

    Dear {} welcome aboard, these are the details to access your vault, keep well...
    Username : {}
    Hashed_pwd : {}
    Salt : """.format(Username, Username, master_password_gen())
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        try:
            server.login(sender, pwd)
            server.sendmail(sender, receiver, message)
            print("[+] Successfully created, check your Email for further action...")
        except SMTPException :
            print(" Account created Successfully but email verification failed ")


def query_master_pwd(master_password, second_FA_location): 

    # Enter password hash in ******** field. Use PBKDF2 and Salt from above. Use master_password_hash_generator.py to generate a master password hash.
    master_password_hash = master_password_gen()

    compile_factor_together = hashlib.sha256(master_password + second_FA_location).hexdigest()

    if compile_factor_together == master_password_hash: 
        return True 
    
def encrypt_password(password_to_encrypt, master_password_hash): 
    
    key = PBKDF2(str(master_password_hash), salt).read(32)
    
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

    key = PBKDF2(str(master_password_hash), salt).read(32)

    nonce = convert[-16:]

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    plaintext = cipher.decrypt(convert[:-16]) 

    return plaintext


