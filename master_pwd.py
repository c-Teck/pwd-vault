#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:04:32 2021

@author: cybree
"""

# from hashlib import sha256

from Crypto.Cipher import AES
from pbkdf2 import PBKDF2
import hashlib
from base64 import b64encode, b64decode
from dotenv import load_dotenv
import os
import string
import secrets
from termcolor import colored


load_dotenv()
# Enter salt here in ******* field. Enter binary string.
# salt = b'********'


# hash given password
'''def hashpassword(password, length):
    # salt = secrets.token_hex(64)
    salt_env = os.environ.get('SALT')
    hashed = hashlib.sha512((salt_env + password).encode('utf-8')).hexdigest()
    hashed = hashed[:length]
    return hashed'''

'''def validate_password(pwd):
    while True:
        try:
            passwd = input("[+] Enter password again: ")
            special_symbols = ['$', '@', '#', '%', '!', '&', '*', '+', '+', '_', '-']
            val = True

            if len(passwd) < 8:
                print(colored('[-] Password length should be at least 8', 'red'))
                val = False

            if len(passwd) > 20:
                print(colored('[-] Password length should be not be greater than 15', 'red'))
                val = False

            if not any(char.isdigit() for char in passwd):
                print(colored('[-] Password should contain at least one numeral', 'red'))
                val = False

            if not any(char.isupper() for char in passwd):
                print(colored('[-] Password should have at least one uppercase letter', 'red'))
                val = False

            if not any(char.islower() for char in passwd):
                print(colored('[-] Password should contain at least one lowercase letter', 'red'))
                val = False

            if not any(char in special_symbols for char in passwd):
                print(colored('[-] Password should contain at least a special character', 'red'))
                val = False

            if val:
                return True
        except KeyboardInterrupt:
            pass'''


class Validate:
    def __init__(self, password):
        self.password = password
        self.salt = secrets.token_hex(12)

    def two_fact(self):
        return self.salt

    def validate_password(self):
        from main import exit_program
        try:
            passwd = self.password
            special_symbols = ['$', '@', '#', '%', '!', '&', '*', '+', '+', '_', '-']
            val = True

            if len(passwd) < 8:
                print(colored('[-] Password length should be at least 8', 'red'))
                val = False

            if len(passwd) > 20:
                print(colored('[-] Password length should be not be greater than 15', 'red'))
                val = False

            if not any(char.isdigit() for char in passwd):
                print(colored('[-] Password should contain at least one numeral', 'red'))
                val = False

            if not any(char.isupper() for char in passwd):
                print(colored('[-] Password should have at least one uppercase letter', 'red'))
                val = False

            if not any(char.islower() for char in passwd):
                print(colored('[-] Password should contain at least one lowercase letter', 'red'))
                val = False

            if not any(char in special_symbols for char in passwd):
                print(colored('[-] Password should contain at least a special character', 'red'))
                val = False

            if val:
                return True
        except KeyboardInterrupt:
            exit_program()

    def compare_passwd(self, psswd2):

        if self.password == psswd2:
            return True
        else:
            print(colored("[-] Passwords do not match, please try again.", 'red'))

    def password_gen(self, password_length):

        characters = string.ascii_letters + string.digits

        secure_password = ''.join(secrets.choice(characters) for i in range(password_length))

        return secure_password

    def master_password_gen(self):
        # os.environ["SALT"] = salt().
        master_pwd = self.password.encode()
        # two_factor = os.environ.get("SALT").encode()
        # salt to be taken from database
        two_factor = self.salt.encode()
        compile_factor_together = hashlib.sha256(master_pwd + two_factor).hexdigest()
        print("\n[+] Generating your hashed password...\n...\n[+] Your hashed password has been generated")
        hashed = (str(compile_factor_together))
        return hashed
        # os.environ["MASTER"] = hashed

    def query_master_pwd(self, second_fa_location):
        from Database_classes import get_master
        # Enter password hash in ******** field. Use PBKDF2 and Salt from above.
        # Use master_password_hash_generator.py to generate a master password hash.
        # master password to be fetched from database
        # master_password_hash = os.environ.get("MASTER")
        db_name = os.environ.get("DB_TYPE")
        master_password_hash = get_master(db_name, 'settings', 'MASTER')

        compile_factor_together = hashlib.sha256(self.password + second_fa_location).hexdigest()

        if compile_factor_together == master_password_hash:
            return True
        else:
            return False

    def encrypt_password(self, master_password_hash):
        # salt_auth = os.environ.get('SALT')
        # salt to be taken from the database after connection
        salt_auth = self.salt
        key = PBKDF2(str(master_password_hash), salt_auth).read(32)

        data_convert = str.encode(self.password)

        cipher = AES.new(key, AES.MODE_EAX)

        nonce = cipher.nonce

        ciphertext, tag = cipher.encrypt_and_digest(data_convert)

        add_nonce = ciphertext + nonce

        encoded_ciphertext = b64encode(add_nonce).decode()

        return encoded_ciphertext

    def decrypt_password(self, master_password_hash):

        if len(self.password) % 4:
            self.password += '=' * (4 - len(self.password) % 4)

        convert = b64decode(self.password)
        salt_auth = self.salt
        key = PBKDF2(str(master_password_hash), salt_auth).read(32)

        nonce = convert[-16:]

        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

        plaintext = cipher.decrypt(convert[:-16])

        return plaintext
