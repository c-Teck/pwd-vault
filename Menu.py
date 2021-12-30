#!/usr/bin/env python3

#from hash_maker import password
import subprocess
#from database_manager.py import store_passwords, find_users, find_password,update_details
from master_pwd.py import password_gen
import database_manager.py

def menu():
    print('-'*30)
    print(('-'*13) + 'Menu'+ ('-' *13))
    print('1. Create new password')
    print('2. Find all sites and apps connected to an email')
    print('3. Find a password for a site or app')
    print('4. Update a site details')
    print('5. Delete entire site or app entry or details' )
    print('6. Update Database details ')
    print('Q. Exit')
    print('-'*30)
    return input(': ')

def create():
    print('Please proivide the name of the site or app you want to generate a password for')
    app_name = input()
    print('[+]Please provide a simple password for this site or leave empty to generate a secure password for you :')
    if input() != "" :
       plaintext = input()
    else :
        plaintext = password_gen(8)

    passw = password(plaintext, app_name, 12)
    subprocess.run('xclip', universal_newlines=True, input=passw)
    print('-'*30)
    print('')
    print('Your password has now been created and copied to your clipboard')
    print('')
    print('-' *30)
    user_email = input('Please provide a user email for this app or site')
    username = input('Please provide a username for this app or site (if applicable)')
    if username == None:
       username = ''
    url = input('Please paste the url to the site that you are creating the password for')
    store_passwords(passw, user_email, username, url, app_name)

def find():
   print('Please provide the name of the site or app you want to find the password to')
   app_name = input()
   find_password(app_name)

def find_accounts():
   print('Please proivide the email that you want to find accounts for')
   user_email = input()
   find_users(user_email)

def Update():
    print("[+] What details would you like to update \n >>> email \n >>> passowrd \n >>> Username \n >>> Url \n [+] Reply with 1,2,3,4 as arranged above... ")
    Ansa = input()
    update_details(Ansa)



