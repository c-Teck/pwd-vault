#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 07:58:32 2022

@author: cybree
"""
# Create a Database Class that support MYSQl, psycopg2,
import os
import time
import datetime
import sqlite3
import mysql.connector
from dotenv import load_dotenv
from enum import Enum
from main import exit_program
from mysql.connector import connect, Error, errorcode
import psycopg2
from master_pwd import Validate
from termcolor import colored


load_dotenv()
class Database(Enum):
    SQLITE = "sqlite3"
    MYSQL = "mysql"
    POSTGRES = "postgres"
    ORACLE = "oracle"



    def __init__(self):
        self.host = os.environ.get("DB_HOST")
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PWD")
        self.db_name = os.environ.get("DB_NAME")
        self.sqlite3_connection = sqlite3.connect((self.db_name + ".db"))
        self.mysql_connection = mysql.connector.connect(
                                host=self.host,
                                user=self.user,
                                password=self.password,
                                database=self.db_name
                        )
        self.postgres_connection = psycopg2.connect(user=self.user, password=self.password, host=self.host,
                                                    database=self.db_name
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
            ") ENGINE=InnoDB")
        }

    def all_db(self):
        db_type = os.environ.get("DB_TYPE")
        match db_type:

            case Database.MYSQL:
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
                        print("[-] Invalid input")

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

                    # These functions delete an entry in the database, given a url
                def delete_account(account_to_delete):
                    try:
                        cnx = self.mysql_connection
                        cursor = cnx.cursor()
                        cursor.execute("Delete * FROM VAULT WHERE url = %s'", (account_to_delete,))
                    except (Exception, Error) as error:
                        print(error)

                # Function to Update a given entry in the database
                def update_details(ansa):
                    if ansa == '1':
                        try:
                            app = input("[+] Provide the url where you want to change the Email : ")
                            new = input("[+] provide the new Email \n >>> ")
                            connection = self.mysql_connection
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VAULT set email = %s' WHERE app_name= %s'", (new, app))
                        except (Exception, Error) as error:
                            print(error)

                    elif ansa == '2':
                        try:
                            app = input("[+] Provide the app/site name where you want to change the password : ")
                            new = input("[+] provide the new password \n >>> ")
                            connection = self.mysql_connection
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VAULT set password = %s' WHERE app_name= %s'", (new, app))
                        except (Exception, Error) as error:
                            print(error)

                    elif ansa == '3':
                        try:
                            app = input("[+] Provide the app/site name where you want to change the Username : ")
                            new = input("[+] provide the new username \n >>> ")
                            connection = self.mysql_connection
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VAULT set username = %s' WHERE app_name= %s'", (new, app))
                        except (Exception, Error) as error:
                            print(error)

                    elif ansa == '4':
                        try:
                            app = input("[+] Provide the app/site name where you want to change the Url : ")
                            new = input("[+] provide the new Url \n >>> ")
                            connection = self.mysql_connection
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VAULT set url = %s' WHERE app_name= %s'", (new, app))
                        except (Exception, Error) as error:
                            print(error)

                    else:
                        print("Invalid input")
                        exit_program()

            case Database.SQLITE:
                dbase_name = self.db_name + '.db'

                def create_connection(db_name):
                    """
                    Function creates a connection to db_name database and returns it
                    """
                    connection = self.sqlite3_connection(db_name)
                    return connection

                def create_table(table):
                    conn = create_connection(dbase_name)
                    print(colored("[+] Successfully Authenticated...", 'green'))

                    print("[+] Creating Table {}".format(table), end='')
                    # print(colored("already exists.", 'yellow'))


                    conn.executescript('''CREATE TABLE VAULT
                             (ID INT PRIMARY KEY     NOT NULL   AUTO_INCREMENT,
                             user           varchar(14)    NOT NULL,
                             app_name       varchar(14)    NOT NULL,
                             site_url       CHAR(50)       NOT NULL,
                             email         varchar(20)     NOT NULL,
                             pass           TEXT           NOT NULL,
                             created_date   date           NOT NULL
                             );
                             CREATE TABLE SETTINGS
                             (ID INT PRIMARY KEY     NOT NULL   AUTO_INCREMENT,
                             key           varchar(40)    NOT NULL,
                             value           TEXT           NOT NULL,
                             created_date   date           NOT NULL
                             );
                             ''')

                def write_data_to_db(query, data):
                    """
                    Function awaits arguments:
                    * connection - connection to DB
                    * query - query to execute
                    * data - data to be passed as a list of tuples

                    Function attempts to write all data from *data* list.
                    If data is saved successfully, changes are saved to database and returns True.

                    If an error occurs during the writing process, transaction rolls back and function returns False.

                    """
                    conn = create_connection(dbase_name)
                    try:
                        with conn:
                            conn.executemany(query, data)
                    except sqlite3.IntegrityError as e:
                        print('Error occurred: ', e)
                        return False
                    else:
                        print('[+] Data writing was successful')
                        return True

                def write_rows_to_db_2(query, data, verbose=False):
                    """
                        Function awaits arguments:
                         * connection - connection to DB
                         * query - query to execute
                         * data - data to be passed as a list of tuples

                        Function attempts to write a tuples in turn from *data* list.
                        If tuple can be written successfully, changes are saved to database.
                        If an error occurs while writing the tuple, transaction rolls back.


                        Flag *verbose* controls whether messages about successful or unsuccessful tuple
                        writing attempt.

                    """
                    conn = create_connection(dbase_name)
                    for row in data:
                        try:
                            with conn:
                                conn.execute(query, row)
                        except sqlite3.IntegrityError as e:
                            if verbose:
                                print("Error occurred while writing data '{}'".format(', '.join(row), e))
                        else:
                            if verbose:
                                print("Data writing  was successful '{}'".format(
                                        ', '.join(row)))

                def find_password(app_name):

                    try:
                        connection = create_connection(dbase_name)
                        cursor = connection.cursor()
                        cursor.execute("SELECT pass FROM VAULT WHERE app_name = %s'", (app_name,))
                        connection.commit()
                        result = cursor.fetchone()
                        print('[+] Password is: ', result[0])
                        cursor.close()
                        connection.close()
                    except sqlite3.InterfaceError as e:
                        print(colored("[+] Error :", e, 'red'))

                    else:
                        print(colored("[-] Error...", 'red'))
                        cursor.close()
                        connection.close()
                        exit_program()



                def find_users(user_email):
                    data = ('Password: ', 'Email: ', 'Username: ', 'url: ', 'App/Site name: ')
                    try:
                        connection = create_connection(dbase_name)
                        cursor = connection.cursor()
                        # postgres_select_query = """ SELECT * FROM VAULT WHERE email = '""" + user_email + "'"
                        # cursor.execute(postgres_select_query, user_email)
                        cursor.execute("SELECT * FROM VAULT WHERE email = %s'", (user_email,))
                        connection.commit()
                        result = cursor.fetchall()
                        print('')
                        print('RESULT')
                        print('')
                        for row in result:
                            for i in range(0, len(row) - 1):
                                print(data[i] + row[i])
                        print('')
                        print('-' * 30)
                        cursor.close()
                        connection.close()

                    except sqlite3.InterfaceError as e:
                        print(colored("[+] Error :", e, 'red'))


                # These functions delete an entry in the database, given a url
                def delete_account(account_to_delete):
                    try:
                        connection = create_connection(dbase_name)
                        cursor = connection.cursor()
                        cursor.execute("Delete * FROM VAULT WHERE url = %s'", (account_to_delete,))
                    except (Exception, Error) as error:
                        print(error)


                def store_password(user, email, password):


            case Database.POSTGRES:

                def store_passwords(password, user_email, url):
                    try:
                        connection = connect()
                        cursor = connection.cursor()
                        postgres_insert_query = """ INSERT INTO VAULT (password, email, url) 
                            VALUES (%s, %s, %s)"""
                        record_to_insert = (password, user_email, url)
                        cursor.execute(postgres_insert_query, record_to_insert)
                        connection.commit()
                    except (Exception, psycopg2.Error) as error:
                        print(error)

                def connect():
                    try:
                        return self.postgres_connection
                    except (Exception, psycopg2.Error) as error:
                        print(error + " [-]Failed to connect to Database...")



                def find_password(app_name):
                    try:
                        connection = connect()
                        cursor = connection.cursor()
                        cursor.execute("SELECT password FROM VAULT WHERE app_name = %s'", (app_name,))
                        # postgres_select_query = """ SELECT password FROM VAULT WHERE app_name = '""" + app_name + "'"
                        # cursor.execute(postgres_select_query, app_name)
                        connection.commit()
                        result = cursor.fetchone()
                        print('Password is: ')
                        print(result[0])

                    except (Exception, psycopg2.Error) as error:
                        print(error)

                def find_users(user_email):
                    data = ('Password: ', 'Email: ', 'Username: ', 'url: ', 'App/Site name: ')
                    try:
                        connection = connect()
                        cursor = connection.cursor()
                        # postgres_select_query = """ SELECT * FROM VAULT WHERE email = '""" + user_email + "'"
                        # cursor.execute(postgres_select_query, user_email)
                        cursor.execute("SELECT * FROM VAULT WHERE email = %s'", (user_email,))
                        connection.commit()
                        result = cursor.fetchall()
                        print('')
                        print('RESULT')
                        print('')
                        for row in result:
                            for i in range(0, len(row) - 1):
                                print(data[i] + row[i])
                        print('')
                        print('-' * 30)
                    except (Exception, psycopg2.Error) as error:
                        print(error)

                def update_db_passwd():
                    update_query_passwd = """UPDATE Vault SET passwd = %s WHERE url = %s"""
                    return update_query_passwd

                def delete_account():
                    print("[+] provide app_name or a unique details about the entry you want to delete : ")
                    entry = input()
                    try:
                        connection = connect()
                        cursor = connection.cursor()
                        cursor.execute("Delete * FROM VAULT WHERE app_name = %s'", (entry,))
                    except (Exception, psycopg2.Error) as error:
                        print(error)

                def update_details(ansa):
                    if ansa == '1':
                        try:
                            app = input("[+] Provide the url where you want to change the Email : ")
                            new = input("[+] provide the new Email \n >>> ")
                            connection = connect()
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VAULT set email = %s' WHERE app_name= %s'", (new, app))
                        except (Exception, psycopg2.Error) as error:
                            print(error)
                    elif ansa == '2':
                        try:
                            app = input("[+] Provide the app/site name where you want to change the password : ")
                            new = input("[+] provide the new password \n >>> ")
                            connection = connect()
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VAULT set password = %s' WHERE app_name= %s'", (new, app))
                        except (Exception, psycopg2.Error) as error:
                            print(error)

                    elif ansa == '3':
                        try:
                            app = input("[+] Provide the app/site name where you want to change the Username : ")
                            new = input("[+] provide the new username \n >>> ")
                            connection = connect()
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VAULT set username = %s' WHERE app_name= %s'", (new, app))
                        except (Exception, psycopg2.Error) as error:
                            print(error)

                    elif ansa == '4':
                        try:
                            app = input("[+] Provide the app/site name where you want to change the Url : ")
                            new = input("[+] provide the new Url \n >>> ")
                            connection = connect()
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VAULT set url = %s' WHERE app_name= %s'", (new, app))
                        except (Exception, psycopg2.Error) as error:
                            print(error)

                    else:
                        print("Invalid input")
