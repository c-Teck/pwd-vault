#!/usr/bin/env python3

# from secrets import get_secret_key
import time
import os.path
from Database_classes import db_to_run
from vault_registeration import signup
from dotenv import load_dotenv
from Menu import menu, create, find, find_accounts, update
from pyfiglet import Figlet
from termcolor import colored
from master_pwd import Validate

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
    print(colored(f_font.renderText("C-TECK PASSWORD MANAGER"), 'red'))
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
    from main import exit_program

    if run_type:
        try:
            from main import main_prog
            main_prog()
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
                env_file.write(i + '=\n')
        env_file.close()

        load_dotenv()
        signup()
        print(colored("[+] Enter the master password you would use to securely use "
                      "for your vault: "
                      "\n[+] Please save this password as it is not retrievable..", 'green'))
        pwd_to_insert = input("[+] Enter the password here : ")
        check_input = Validate(pwd_to_insert)

        if check_input.validate_password() is True:
            passwd2 = input("[+] Enter the password again: ")
            comparison = check_input.compare_passwd(passwd2)

            # if password1 == password2
            if comparison:
                db_type = os.environ.get('DB_TYPE')
                table = 'settings'
                master_password = check_input.master_password_gen()
                values = [("MASTER", master_password),
                          ("SALT", check_input.two_fact())]
                execute = db_to_run(db_type)

                conn = execute.connect_db()
                if conn:
                    execute.create_table()
                    execute.insert_into_table(table, values)

                else:
                    print("[+] Internal error occurred.")

                # return values  # work here, this can't return values, it should write it to db.
            elif not comparison:
                print(colored("[-] Password do not match...", 'red'))
        else:
            print(colored("[-] Password is not strong enough", 'red'))

        print(colored("[+] Saving your details...", 'yellow'))
        time.sleep(3)
        print(colored("[+] Details Successfully Saved..."
                      "Run the program again to gain access to full features of the program.", 'green'))

        os.environ['signup'] = "True"

        time.sleep(2)
        exit_program()


start()
