import os
import sys
import time
import getpass
from Database_classes import db_to_run
from termcolor import colored
from dotenv import load_dotenv
from master_pwd import Validate
from database_manager import Database


load_dotenv()


def exit_program():
    print(colored("[-] Exiting...", "red"))
    time.sleep(2)
    sys.exit()


def main():
    password_attempt = 0
    master_password_input = getpass.getpass("[+] Enter your Master Password: ").encode()
    two_factor = os.environ.get("SALT")

    second_fa_location = two_factor.encode()
    # second_FA_location = "Dee Boo Dah".encode()
    # master_password_hash = hashlib.sha256(master_password_input + second_FA_location).hexdigest()

    if not (Validate.query_master_pwd(master_password_input, second_fa_location)):
        if password_attempt >= 3:
            print(colored("[-] Too many wrong attempt, please try again after few minutes...", 'red'))
            exit_program()
        else:
            print(colored("[-] Master password incorrect...\n >>>Try again.", 'red'))
            password_attempt += 1
        # connection = database_manager.connect()
    else:
        db_type = os.environ.get('DB_TYPE')
        execute = db_to_run(db_type)
        connect = execute.connect_db()
        if connect():
            print(colored("[+] Authenticating...", "green"))
            time.sleep(2)
            print(colored("\n[+] Successfully Authenticated.\n\n", "green"))
            time.sleep(2)
            print(colored("[+] Opening your Vault...", "green"))
        else:
            print(colored("[-] Failed to connect to database. "
                          "Ensure yo have an active connection and try again..", 'red'))
            exit_program()

        # return connection
