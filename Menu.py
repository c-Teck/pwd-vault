#!/usr/bin/env python3

import os
import master_pwd
import subprocess
from pyfiglet import Figlet
from termcolor import colored
from dotenv import load_dotenv
from master_pwd import password_gen
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
    print('Please provide the name of the site or app you want to generate a password for')
    app_name = input()
    print('[+]Please provide a simple password for this site or leave empty to generate a secure password for you :')
    if input() != "":
        plaintext = input()
    else:
        plaintext = password_gen(12)

    # passw = password(plaintext, app_name, 12)
    subprocess.run('xclip', universal_newlines=True, input=plaintext)
    print(colored('-'*30, 'red'))
    print('')
    print(colored('[+] Your password has now been created and copied to your clipboard', 'green'))
    print('')
    print(colored('-'*30, 'red'))
    user_email = input('[+] Please provide a user email for this app or site')
    username = input('[+] Please provide a username for this app or site (if applicable)')
    if username == "None":
        username = ''
    url = input('Please paste the url to the site that you are creating the password for')
    secure_pwd = master_pwd.encrypt_password(plaintext, os.environ.get("MASTER"))
    store_passwords(secure_pwd, user_email, username, url, app_name)


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
