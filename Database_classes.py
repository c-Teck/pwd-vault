#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 07:58:32 2022

@author: cybree
"""
# Create a Database Class that support MYSQl, psycopg2,
import time
from main import exit_program
from mysql.connector import connect, Error, errorcode
import psycopg2
from master_pwd import Validate
from termcolor import colored


class Database:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.mysql_connection = mysql.connector.connect(
                                host=self.host,
                                user=self.user,
                                password=self.password,
                        )

    def all_db(self, db_type):

        match db_type:

            case MYSQL:
                def connecting():
                    try:
                        with self.mysql_connection as conn:
                            return conn
                    except Error as e:
                        print(e)

                # Check if Database exist and connect to it and if not create one and insert necessary tables
                def check_database():
                    output = connecting()
                    if output:
                        execution = self.mysql_connection.cursor()
                        try:
                            conn = execution.execute("SHOW DATABASES")
                            for x in conn:
                                if x[0] == PWDMGR:
                                    db_conn = mysql.connector.connect(database="PWDMGR")
                                    return db_conn

                        except mysql.connector.Error as err:
                            if err.errno == errorcode.ER_BAD_DB_ERROR:
                                print("Database does not exist...\n[+] Creating database...")
                                time.sleep(2)
                                execution.execute("CREATE DATABASE PWDMGR")
                                execution.execute("CREATE TABLE settings (id INT AUTO_INCREMENT, key VARCHAR(30), "
                                                  "value TEXT), PRIMARY KEY (id)")
                                insert = "INSERT INTO settings (key, value) VALUES (%s, %s)"
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
                                        master_password = check_input.master_password_gen()
                                        values = [("MASTER", master_password),
                                                  ("SALT", check_input.two_fact())]
                                        execution.executemany(insert, values)
                                        output.commit()
                                        del execution
                                        exit_program()
                                    elif not comparison:
                                        print(colored("[-] Password do not match...", 'red'))
                                else:
                                    print(colored("[-] Password is not strong enough", 'red'))

                            elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                                print("[-] Something is wrong with your user name or password.")

                            else:
                                print(err)

                        else:
                            conn.close()


