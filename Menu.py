#!/usr/bin/env python3

import os
import master_pwd
import subprocess
from pyfiglet import Figlet
from termcolor import colored
from dotenv import load_dotenv
from master_pwd import password_gen, Validate
from database_manager import store_passwords, find_users, find_password, update_details


f = Figlet(font='isometric2')
f_font = Figlet(font='banner3-D')
load_dotenv()


def menu():
    # colors = ['yellow', 'red', 'green', 'blue']
    print(colored('-'*30, 'red'))
    # for color in colors:
    # print(colored(f_font.renderText("C-TECK PASSWORD MANAGER"), color))
    print(colored(f.renderText(('-'*13) + 'Menu' + ('-' * 13)), 'green'))
    print(colored('1. Create new password', 'yellow'))
    print(colored('3. Find a password for a site or app', 'yellow'))
    print(colored('4. Update a site details', 'yellow'))
    print(colored('5. Delete entire site or app entry or details', 'yellow'))
    print(colored('6. Update Database details ', 'yellow'))
    print(colored('Q. Exit', "red"))
    print(colored('-'*30, 'red'))
    return input(': ')


def create():
    print('[+] Please provide the name of the site or app you want to generate a password for')
    app_name = input()
    print('[+] Please provide a simple password for this site or leave '
          'empty to generate a secure password for you :')
    while True:
        text = input()
        if text != "":
            plaintext = text
            check_input = Validate(plaintext)
            if check_input.validate_password() is True:
                passwd2 = input("[+] Enter the password again: ")
                comparison = check_input.compare_passwd(passwd2)
                if comparison:
                    return plaintext
                elif not comparison:
                    continue
            else:
                continue
        else:
            plaintext = password_gen(12)
            return plaintext
        # if validate_password(plaintext):
    subprocess.run('xclip', universal_newlines=True, input=plaintext)
    user_email = input('[+] Please provide an email/username for this app or site')
    secure_pwd = master_pwd.encrypt_password(plaintext, os.environ.get("MASTER"))
    store_passwords(secure_pwd, user_email, app_name)
    print(colored('-' * 30, 'red'))
    print('')
    print(colored('[+] Your password has now been created and copied to your clipboard', 'green'))
    print('')
    print(colored('-' * 30, 'red'))


def find():
    print('[+] Please provide the name of the site or app you want to find the password to: ')
    app_name = input()
    find_password(app_name)


def find_accounts():
    print('[+]Please provide the email that you want to find accounts for: ')
    user_email = input()
    find_users(user_email)


def update():
    print("[+] What details would you like to update \n >>> email \n >>> "
          "password \n >>> Username \n >>> Url \n [+] Reply with 1,2,3,4 as arranged above... ")
    ansa = input()
    update_details(ansa)
