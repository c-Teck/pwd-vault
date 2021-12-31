import os
import sys
import getpass
from termcolor import colored
from dotenv import load_dotenv
import master_pwd
import hashlib


load_dotenv()
def exit_program():
    print(colored("Exiting...", "red"))
    sys.exit()

def main():

    master_password_input = getpass.getpass("Master Password: ").encode()
    Two_Factor = input("[+] Enter your two factor authenticator here : ")

    second_FA_location = Two_Factor.encode()
    #second_FA_location = "Dee Boo Dah".encode()

    master_password_hash = hashlib.sha256(master_password_input + second_FA_location).hexdigest()

    if master_pwd.query_master_pwd(master_password_input, second_FA_location) is True:

        connection = db_connect.connection_db()

        print("\nSucessfully Authenticated.\n")

    else:
        print("Failed to authenticate into server. Run the program again.")
        sys.exit()


