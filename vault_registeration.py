#!/usr/bin/env python3

# import smtplib, ssl
# from master_pwd import master_password_gen
import os
import getpass
from termcolor import colored


def signup():
    '''email = input("[+] Enter your email address to use with this vault : ")
    fullname = input(" [+] Enter your Fullname : ")
    username = input(" [+] What nickname should i call you : ")
    sender = ''
    receiver = email
    port = 587
    smtp_server = 'smtp.gmail.com'
    pwd = '##'
    message = """\
    Subject: WELCOME TO PASSWORD MANAGER VAULT BY C-TECK

    Dear {} welcome aboard, these are the details to access your vault, keep well...
    Username : {}
    Hashed_pwd : {}
    Salt : has been saved for secured purpose. """.format(fullname, username, master_password_gen())
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        try:
            server.login(sender, pwd)
            server.sendmail(sender, receiver, message)
            print("[+] Successfully created, check your Email for further action...")
        except SMTPException :
            print(" Account created Successfully but email verification failed ")'''
    user = getpass.getuser()
    print(colored("Welcome ", user), 'yellow')
    print("[+] What is your database type:")
    print("Mysql, Postgres, Oracle, Maria DB, SQL Server...")
    db_type = input()
    os.environ['DB_TYPE'] = db_type
    db_name = input("[+] Enter your database name here :")
    db_host = input("[+] Enter your database Host/IP here: ")
    db_user = input("[+] Enter your database Username: ")
    db_pwd = input("[+] Enter password")
    db_port = int(input("[+] Enter your database port number: "))
    os.environ['DB_PORT'] = db_port
    os.environ['DB_NAME'] = db_name
    os.environ['DB_HOST'] = db_host
    os.environ['DB_USER'] = db_user
    os.environ['DB_PWD'] = db_pwd


