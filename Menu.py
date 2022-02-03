#!/usr/bin/env python3

import os
import datetime
import subprocess
from main import exit_program
from pyfiglet import Figlet
from termcolor import colored
from dotenv import load_dotenv
from master_pwd import Validate
from Database_classes import get_master_plain, db_to_run


f = Figlet(font='isometric2')
f_font = Figlet(font='banner3-D')
load_dotenv()
db_type = os.environ.get('DB_TYPE')


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
    table = 'VAULT'
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
                    print(colored("Passwords do not match \n Try again", 'red'))
                    passwd2 = input("[+] Enter the password again: ")
                    comparison = check_input.compare_passwd(passwd2)
                    if comparison:
                        return plaintext
                    else:
                        print("Error...Run the program again")
                        exit_program()
            else:
                continue
        else:
            text = ''
            plaintext = Validate(text)
            plaintext = plaintext.password_gen(12)
            return plaintext
        # if validate_password(plaintext):
    username = input("[+] Provide a username for this account or leave empty if not applicable.")
    subprocess.run('xclip', universal_newlines=True, input=plaintext)
    user_email = input('[+] Please provide an email/username for this app or site: ')
    pwd = Validate(plaintext)
    master_encrypt = get_master_plain(db_type, plaintext)
    secure_pwd = pwd.encrypt_password(master_encrypt)
    to_run = db_to_run(db_type)
    # (user, app_name, site_url, email, pass, created_date)
    values = [("user", username),
              ("app_name", app_name),
              ("site_url", ),
              ("email", user_email),
              ("pass", secure_pwd),
              ("created_date", datetime.date.today())]
    conn = to_run.connect_db()
    if conn:
        to_run.insert_into_table(table, values)

    else:
        print("[+] Internal error occurred.")
    # to_run.insert_into_table(secure_pwd, user_email, app_name)
    if to_run.insert_into_table(table, values):
        print(colored('-' * 30, 'red'))
        print('')
        print(colored('[+] Your password has now been created and copied to your clipboard', 'green'))
        print('')
        print(colored('-' * 30, 'red'))

    else:
        print(">>> An error occurred when performing the operations above...")


def find():
    print('[+] Please provide the name of the site or app you want to find the password to: ')
    app_name = input()
    execute = db_to_run(db_type)
    conn = execute.connect_db()
    if conn:
        try:
            execute.find_password(app_name)

        except Exception as e:
            print(e)

    else:
        print("failed to connect to database.")


def find_accounts():
    print('[+]Please provide the email that you want to find accounts for: ')
    user_email = input()
    execute = db_to_run(db_type)
    conn = execute.connect_db()
    if conn:
        try:
            execute.find_users(user_email)

        except Exception as e:
            print(e)

    else:
        print("failed to connect to database.")


def update():
    print("[+] What details would you like to update \n >>> email \n >>> "
          "password \n >>> Username \n >>> Url \n [+] Reply with 1,2,3,4 as arranged above... ")
    ansa = input()
    execute = db_to_run(db_type)
    conn = execute.connect_db()
    if conn:
        try:
            execute.update_details(ansa)

        except Exception as e:
            print(e)

    else:
        print("failed to connect to database.")


def delete_entry():
    to_delete = input("Enter the url or site name you want to delete: ")
    execute = db_to_run(db_type)
    conn = execute.connect_db()
    if conn:
        try:
            execute.delete(to_delete)

        except Exception as e:
            print(e)

    else:
        print("failed to connect to database.")
