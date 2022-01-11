#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 07:58:32 2022

@author: cybree
"""
# Create a Database Class that support MYSQl, psycopg2,

from mysql.connector import connect, Error
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
                            execution.execute("CREATE DATABASE PWDMGR")
                            execution.execute("CREATE TABLE settings (sid INT AUTO_INCREMENT, key VARCHAR(10), "
                                              "value TEXT), PRIMARY KEY (sid)")
                            insert = "INSERT INTO settings (sid, key, value) VALUES (%s, %s, %s)"
                            print(colored("[+] Enter the master password you would use to securely use for yout vault: "
                                  "\n[+] Please save this password as it is not retrievable..", 'green'))
                            pwd_to_insert = input("[+] Enter the password here : ")
                            check_input = Validate(pwd_to_insert)
                            if check_input.validate_password() is True:
                                passwd2 = input("[+] Enter the password again: ")
                                comparison = check_input.compare_passwd(passwd2)
                                if comparison:
                                    values = [(sid, "MASTER", pwd_to_insert),
                                              (sid, "SALT", Validate.two_fact(check_input))]
                                    execution.executemany(insert, values)
                                    output.commit()
                                    del execution
                                elif not comparison:
                                    pass
                            else:
                                pass
                        except Exception as e:
                            execution.execute("SHOW DATABASES")
                            for x in execution:
                                print(x[0])




                
