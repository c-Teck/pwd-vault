#!/usr/bin/env python3

import smtplib, ssl
from master-pwd.py import master_password_gen



def signup():
    Email = input("[+] Enter your email address to use with this vault : ")
    Fullname = input(" [+] Enter your Fullname : ")
    Username = input(" [+] What nickname should i call you : ")
    sender = "pwdvault@gmail.com"
    receiver = Email
    port = 587
    smtp_server = 'smtp.gmail.com'
    pwd = 'passw0RD'
    message = """\
    Subject: WELCOME TO PASSWORD MANAGER VAULT BY C-TECK

    Dear {} welcome aboard, these are the details to access your vault, keep well...
    Username : {}
    Hashed_pwd : {}
    Salt : has been saved for secured purpose. """.format(Fullname, Username, master_password_gen())
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        try:
            server.login(sender, pwd)
            server.sendmail(sender, receiver, message)
            print("[+] Successfully created, check your Email for further action...")
        except SMTPException :
            print(" Account created Successfully but email verification failed ")

