#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 07:58:32 2022

@author: cybree
"""
# Create a Database Class that support MYSQl, psycopg2,
import time
import datetime
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
        self.db_name = "PWDMGR"
        self.mysql_connection = mysql.connector.connect(
                                host=self.host,
                                user=self.user,
                                password=self.password,
                        )
        self.TABLES = {'VAULT': (
            "CREATE TABLE `VAULT` ("
            "  `id` int(10) NOT NULL AUTO_INCREMENT,"
            "  `user` varchar(14) NOT NULL,"
            "  `app_name` varchar(20) NOT NULL,"
            "  `site_url` varchar(20) NOT NULL,"
            "  `email` varchar(20) NOT NULL,"
            "  `pass` TEXT NOT NULL,"
            "  `created_date` date NOT NULL,"
            "  PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB"), 'settings': (
            "CREATE TABLE `settings` ("
            "  `id` int(10) NOT NULL AUTO_INCREMENT,"
            "  `key` varchar(40) NOT NULL,"
            "  `value` TEXT NOT NULL,"
            "  PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB")}

    def all_db(self, db_type):

        match db_type:

            case MYSQL:
                def connecting():
                    try:
                        with self.mysql_connection as conn:
                            return conn
                    except Error as e:
                        print(e)

                def create_database(cursor):
                    try:
                        cursor.execute(
                            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.db_name)
                        )
                    except mysql.connector.Error as err:
                        print(colored("[-] Failed creating database: {}".format(err), 'red'))
                        time.sleep(2)
                        exit_program()
                        time.sleep(1)
                    # cnx.close()
                # Check if Database exist and connect to it and if not create one and insert necessary tables
                def connect_to_db():
                    output = connecting()
                    execution = self.mysql_connection.cursor()
                    db_name = self.db_name
                    if output:
                        try:
                            conn = execution.execute("SHOW DATABASES")
                            for x in conn:
                                if x[0] == db_name:
                                    print("[+] Database {} existed...Connecting...".format(db_name))
                            execution.execute("USE {}".format(db_name))

                        except mysql.connector.Error as err:

                            if err.errno == errorcode.ER_BAD_DB_ERROR:
                                print("Database {} does not exist...\n[+] Creating database...".format(db_name))
                                time.sleep(2)
                                print("Loading...")
                                create_database(execution)
                                self.mysql_connection.database = db_name

                def create_db_tables(cursor):
                    for table_name in self.TABLES:
                        table_description = self.TABLES[table_name]
                        try:
                            print("Creating table {}: ".format(table_name), end='')
                            cursor.execute(table_description)
                        except mysql.connector.Error as err:
                            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                                print(colored("already exists.", 'yellow'))
                            else:
                                print(err.msg)
                        else:
                            print(colored("OK", 'green'))

                    cursor.close()

                def insert_into_dbTable(table, val):
                    cnx = self.mysql_connection
                    cursor = cnx.cursor()
                    if table == "settings":
                        insert = "INSERT INTO {} (key, value) VALUES (%s, %s)".format(table)
                        # values = [("MASTER", master_password),
                         #         ("SALT", check_input.two_fact())] Use this value populate settings table
                        cursor.execute(insert, val)
                        # return insert
                    elif table == "VAULT":
                        insert = "INSERT INTO {} (user, app_name, site_url, email, pass, created_date) " \
                                 "VALUES (%s, %s, %s, %s, %s, %s)".format(table)
                        cursor.execute(insert, val)
                        # return insert
                    else:
                        print(colored("[-] Specified table({}) does not exist", 'red').format(table))

                    cnx.commit()
                    cursor.close()
                    cnx.close()

                def find_password(table, app_name, user_email)
                    cnx = self.mysql_connection
                    cursor = cnx.cursor()
                    reply = input(" Would you like to find passwords and sites associated to an email or "
                                  "Fetch password for a site/app??\n [+] Reply 1 or 2 :")
                    #cursor = self.mysql_connection.cursor()
                    if reply == 1:
                        cursor.execute("SELECT password FROM {} WHERE app_name = %s'", (app_name, )).format(table)
                        cnx.commit()
                        result = cursor.fetchone()
                        print('Password is: ')
                        print(result[0])

                    elif reply == 2:
                        data = ('Password: ', 'Email: ', 'Username: ', 'url: ', 'App/Site name: ')
                        try:
                            # postgres_select_query = """ SELECT * FROM VAULT WHERE email = '""" + user_email + "'"
                            # cursor.execute(postgres_select_query, user_email)
                            cursor.execute("SELECT * FROM VAULT WHERE email = %s'", (user_email,))
                            cnx.commit()
                            result = cursor.fetchall()
                            print('')
                            print('RESULT')
                            print('')
                            for row in result:
                                for i in range(0, len(row) - 1):
                                    print(data[i] + row[i])
                            print('')
                            print('-' * 30)

                    else:
                        print(" Invalid input")

                    cursor.close()
                    cnx.close()

                # select date in form YYYY-MM-DD
                def query_pwd_date(app_name, site_name, start_date, end_date):
                    cnx = self.mysql_connection
                    cursor = cnx.cursor()
                    query = ("SELECT {}, {}, created_date FROM VAULT "
                             "WHERE created_date BETWEEN %s AND %s").format(app_name, site_name)

                    start = datetime.date(0,0,0)
                    end = datetime.date(0,0,0)
                    cursor.execute(query, (start, end))

                    for (app_name, url, created_date) in cursor:
                        print("{}, {} was created on {:%d %b %Y}".format(
                            app_name, url, created_date))

                    cursor.close()
                    cnx.close()
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

                def store_password(user, email, password):



