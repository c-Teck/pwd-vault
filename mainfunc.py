#!/usr/bin/env python3

# from secrets import get_secret_key
import time
import os.path
from main import main
from vault_registeration import signup
from dotenv import load_dotenv
from Menu import menu, create, find, find_accounts, update
from main import exit_program
from pyfiglet import Figlet
from termcolor import colored
# from master_pwd import query_master_pwd

# menu
# 1. create new password for a site
# 2. find password for a site
# 3. Find all sites connected to an email

'''secret = get_secret_key()
pwd = input('[+] Please provide the master password to start using your password vault manager : ')

if pwd == secret:
    print('>>>\n>>>\n>>>\n [+] Successfully Authenticated...')

else:
    print('no luck, try again')
    exit()'''
terminate_buttons = ["Q", "Exit", "exit", "EXIT", "terminate", "stop"]
f_font = Figlet(font='banner3-D')
# env_file = load_dotenv()


def start():
    print(colored('-' * 30, 'red'))
    print('')
    colors = ['yellow', 'red', 'green', 'blue']
    for color in colors:
        print(colored(f_font.renderText("C-TECK PASSWORD MANAGER"), color))
    print('')
    print(colored('-' * 30, 'red'))

    # Check for env file and if not one, Create Signup and fix database details into the env file!!!
    def check_first_run():
        file_exists = os.path.exists('.env')
        if file_exists:
            return True
        else:
            return False

    run_type = check_first_run()

    if run_type:
        try:
            main()
            choice = menu()
            while choice not in terminate_buttons:
                try:
                    if choice == '1':
                        create()
                    if choice == '2':
                        find_accounts()
                    if choice == '3':
                        find()
                    if choice == '4':
                        update()
                    if choice == '6':
                        print(colored('[+] Relax we are working on this update soon...', 'blue'))
                    if choice == '7':
                        print(colored(' [+] This update will be rolled over soon....', 'blue'))
                    else:
                        choice = menu()

                except Exception as e:
                    print(e)
                    print(colored("[-] Internal error occurred. Contact the administrator...", 'red'))
                    break
        except Exception as error:
            print(colored(str(error), 'red'))
            time.sleep(2)
            exit_program()
    # else the program is first run...hence register, request database details and create a .env file
    else:
        file_to_write = ['DB_HOST', 'DB_TYPE', 'DB_NAME', 'DB_USER', 'DB_PORT', 'DB_PWD', 'signup']
        with open('.env', 'w') as env_file:
            for i in file_to_write:
                env_file.write(i + '=')
        env_file.close()
        load_dotenv()
        signup()
        print(colored("[+] Saving your details...", 'yellow'))
        time.sleep(3)
        print(colored("[+] Details Successfully Saved..."
                      "Run the program again to gain access to full features of the program.", 'green'))
        os.environ['signup'] = "True"
        time.sleep(2)
        exit_program()
