#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 07:58:32 2022

@author: cybree
"""
# Create a Database Class that support MYSQl, psycopg2,
import os
import time
import datetime
import sqlite3
import psycopg2
import mysql.connector
from dotenv import load_dotenv
from main import exit_program
from mysql.connector import Error, errorcode
from psycopg2 import OperationalError, errorcodes, errors
from sqlite3 import Error as sqlite_Error
from termcolor import colored


class Database:

    def __init__(self):
        load_dotenv()
        self.db_type = os.environ.get('DB_TYPE')
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
            ), 'settings': (
            "CREATE TABLE `settings` ("
            "  `id` int(10) NOT NULL AUTO_INCREMENT,"
            "  `key` varchar(40) NOT NULL,"
            "  `value` TEXT NOT NULL,"
            "  PRIMARY KEY (`id`)"
            )
        }


class Mysql(Database):

    def __init__(self):
        Database.__init__(self)
        self.connect = mysql.connector.connect(
                                host=self.host,
                                user=self.user,
                                password=self.password,
                        )

    def connect_db(self):
        try:
            with self.mysql_connection as conn:
                return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database {} does not exist...\n[+] Creating database...".format(self.db_name))
                time.sleep(2)
                print(">>> Loading...")
                cursor = self.connect.cursor()
                cursor.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.db_name)
                )
                cursor.execute("USE {}".format(self.db_name))
                cursor.close()

            else:
                print(colored("[-] Failed with the following error: ", 'red'), err.errno, err)

    def create_tables(self):
        cursor = self.connect.cursor()
        for table_name in self.TABLES:
            table_description = self.TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print(colored("[-] already exists.", 'yellow'))
                else:
                    print(err.msg)
            else:
                print(colored("OK", 'green'))

        cursor.close()

    def insert_into_table(self, table, val):
        cursor = self.mysql_connection.cursor()
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

        self.mysql_connection.commit()
        cursor.close()
        self.mysql_connection.close()

    def find_password(self, table, app_name, user_email):
        cnx = self.mysql_connection
        cursor = cnx.cursor()
        reply = input(" >>> Would you like to find all passwords and sites associated to an email or "
                      "Fetch password for a site/app??\n [+] Reply 1 or 2 :")
        # cursor = self.mysql_connection.cursor()
        if reply == 1:
            cursor.execute("SELECT password FROM {} WHERE app_name = %s'", (app_name,)).format(table)
            cnx.commit()
            result = cursor.fetchone()
            print('[+] Password is: ', result[0])

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
            except (Exception, Error) as error:
                print(error)
        else:
            print("[-] Invalid input")

        cursor.close()
        cnx.close()

    def query_pwd_date(self, app_name, site_name, start_date, end_date):
        cnx = self.mysql_connection
        cursor = cnx.cursor()
        query = ("SELECT {}, {}, created_date FROM VAULT "
                 "WHERE created_date BETWEEN %s AND %s").format(app_name, site_name)

        start = datetime.datetime.strptime(start_date, "%d/%m/%Y").date()
        end = datetime.datetime.strptime(end_date, "%d/%m/%Y").date()
        cursor.execute(query, (start, end))

        for (app_name, url, created_date) in cursor:
            print("{}, {} was created on {:%d %b %Y}".format(
                app_name, url, created_date))

        cursor.close()
        cnx.close()

    # These functions delete an entry in the database, given a url
    def delete_account(self, entry_to_delete):
        cnx = self.mysql_connection
        cursor = cnx.cursor()
        try:
            cursor.execute("Delete * FROM VAULT WHERE url = %s'", (entry_to_delete,))
        except (Exception, Error) as error:
            print(error)
        cursor.close()

        # Function to Update a given entry in the database

    def update_details(self, ansa):
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


class Postgres(Database):

    def __init__(self):
        super().__init__()

    def connect_db(self):
        try:
            return self.postgres_connection
        except (errors, OperationalError) as error:
            if error == errorcodes.INVALID_DATABASE_DEFINITION:
                print("Database {} does not exist...\n[+] Creating database...".format(self.db_name))
                time.sleep(2)
                print(">>> Loading...")
                cursor = self.postgres_connection.cursor()
                cursor.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.db_name)
                )
                cursor.execute("USE {}".format(self.db_name))
                cursor.close()

            else:
                print(colored("[-] Failed with the following error: ", 'red'), error, errorcodes)

            print(error, " [-] Failed to connect to Database...")

    def create_tables(self):
        cursor = self.postgres_connection.cursor()
        for table_name in self.TABLES:
            table_description = self.TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except (errors, OperationalError) as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print(colored("[-] already exists.", 'yellow'))
                else:
                    print(err.msg)
            else:
                print(colored("OK", 'green'))

        cursor.close()

    def insert_into_table(self, table, val):
        cursor = self.postgres_connection.cursor()
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

        self.postgres_connection.commit()
        cursor.close()
        self.postgres_connection.close()

    def find_password(self, table, app_name, user_email):
        cursor = self.postgres_connection.cursor()
        reply = input(" >>> Would you like to find all passwords and sites associated to an email or "
                      "Fetch password for a site/app??\n [+] Reply 1 or 2 :")
        # cursor = self.mysql_connection.cursor()
        if reply == 1:
            cursor.execute("SELECT password FROM {} WHERE app_name = %s'", (app_name,)).format(table)
            self.postgres_connection.commit()
            result = cursor.fetchone()
            print('[+] Password is: ', result[0])

        elif reply == 2:
            data = ('Password: ', 'Email: ', 'Username: ', 'url: ', 'App/Site name: ')
            try:
                # postgres_select_query = """ SELECT * FROM VAULT WHERE email = '""" + user_email + "'"
                # cursor.execute(postgres_select_query, user_email)
                cursor.execute("SELECT * FROM VAULT WHERE email = %s'", (user_email,))
                self.postgres_connection.commit()
                result = cursor.fetchall()
                print('')
                print('RESULT')
                print('')
                for row in result:
                    for i in range(0, len(row) - 1):
                        print(data[i] + row[i])
                print('')
                print('-' * 30)
            except (Exception, Error) as error:
                print(error)
        else:
            print("[-] Invalid input")

        cursor.close()
        self.postgres_connection.close()

    def query_pwd_date(self, app_name, site_name, start_date, end_date):
        cnx = self.mysql_connection
        cursor = cnx.cursor()
        query = ("SELECT {}, {}, created_date FROM VAULT "
                 "WHERE created_date BETWEEN %s AND %s").format(app_name, site_name)

        start = datetime.datetime.strptime(start_date, "%d/%m/%Y").date()
        end = datetime.datetime.strptime(end_date, "%d/%m/%Y").date()
        cursor.execute(query, (start, end))

        for (app_name, url, created_date) in cursor:
            print("{}, {} was created on {:%d %b %Y}".format(
                app_name, url, created_date))

        cursor.close()
        cnx.close()

    # These functions delete an entry in the database, given a url
    def delete_account(self, entry_to_delete):
        cnx = self.postgres_connection
        cursor = cnx.cursor()
        try:
            cursor.execute("Delete * FROM VAULT WHERE url = %s'", (entry_to_delete,))
        except (Exception, Error) as error:
            print(error)
        cursor.close()

        # Function to Update a given entry in the database

    def update_details(self, ansa):
        if ansa == '1':
            try:
                app = input("[+] Provide the url where you want to change the Email : ")
                new = input("[+] provide the new Email \n >>> ")
                connection = self.postgres_connection
                cursor = connection.cursor()
                cursor.execute("UPDATE VAULT set email = %s' WHERE app_name= %s'", (new, app))
            except (Exception, Error) as error:
                print(error)

        elif ansa == '2':
            try:
                app = input("[+] Provide the app/site name where you want to change the password : ")
                new = input("[+] provide the new password \n >>> ")
                connection = self.postgres_connection
                cursor = connection.cursor()
                cursor.execute("UPDATE VAULT set password = %s' WHERE app_name= %s'", (new, app))
            except (Exception, Error) as error:
                print(error)

        elif ansa == '3':
            try:
                app = input("[+] Provide the app/site name where you want to change the Username : ")
                new = input("[+] provide the new username \n >>> ")
                connection = self.postgres_connection
                cursor = connection.cursor()
                cursor.execute("UPDATE VAULT set username = %s' WHERE app_name= %s'", (new, app))
            except (Exception, Error) as error:
                print(error)

        elif ansa == '4':
            try:
                app = input("[+] Provide the app/site name where you want to change the Url : ")
                new = input("[+] provide the new Url \n >>> ")
                connection = self.postgres_connection
                cursor = connection.cursor()
                cursor.execute("UPDATE VAULT set url = %s' WHERE app_name= %s'", (new, app))
            except (Exception, Error) as error:
                print(error)

        else:
            print("Invalid input")
            exit_program()


class Sqlite(Database):

    def __init__(self):
        super().__init__()
        self.cursor = self.sqlite3_connection.cursor()

    def connect_db(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = self.sqlite3_connection
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                return conn

    def create_table(self):
        cursor = self.sqlite3_connection.cursor()
        for table_name in self.TABLES:
            table_description = self.TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except sqlite_Error as err:
                if err == errorcode.ER_TABLE_EXISTS_ERROR:
                    print(colored("[-] already exists.", 'yellow'))
                else:
                    print(err)
            else:
                print(colored("OK", 'green'))

        cursor.close()

    def write_data_to_db(self, query, data):
        """
        Function awaits arguments:
        * connection - connection to DB
        * query - query to execute
        * data - data to be passed as a list of tuples

        Function attempts to write all data from *data* list.
        If data is saved successfully, changes are saved to database and returns True.

        If an error occurs during the writing process, transaction rolls back and function returns False.

        """
        conn = self.sqlite3_connection.cursor()
        try:
            with conn:
                conn.executemany(query, data)
        except sqlite3.IntegrityError as e:
            print('Error occurred: ', e)
            return False
        else:
            print('[+] Data writing was successful')
            return True

    def insert_into_table(self, table, value):
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
        cursor = self.sqlite3_connection.cursor()
        if table == "settings":
            insert = "INSERT INTO {} (key, value) VALUES (%s, %s)".format(table)
            # values = [("MASTER", master_password),
            #         ("SALT", check_input.two_fact())] Use this value populate settings table
            cursor.execute(insert, value)
            # return insert
        elif table == "VAULT":
            insert = "INSERT INTO {} (user, app_name, site_url, email, pass, created_date) " \
                     "VALUES (%s, %s, %s, %s, %s, %s)".format(table)
            cursor.execute(insert, value)
            # return insert
        else:
            print(colored("[-] Specified table({}) does not exist", 'red').format(table))
        self.sqlite3_connection.commit()
        cursor.close()
        self.sqlite3_connection.close()
        '''for row in table:
            try:
                with conn:
                    conn.execute(value, row)
            except sqlite3.IntegrityError as e:
                if verbose:
                    print("Error occurred while writing data '{}'".format(', '.join(row), e))
            else:
                if verbose:
                    print("Data writing  was successful '{}'".format(
                        ', '.join(row)))'''

    def query_pwd_date(self, app_name, site_name, start_date, end_date):
        cnx = self.sqlite3_connection
        cursor = cnx.cursor()
        query = ("SELECT {}, {}, created_date FROM VAULT "
                 "WHERE created_date BETWEEN %s AND %s").format(app_name, site_name)

        start = datetime.datetime.strptime(start_date, "%d/%m/%Y").date()
        end = datetime.datetime.strptime(end_date, "%d/%m/%Y").date()
        cursor.execute(query, (start, end))

        for (app_name, url, created_date) in cursor:
            print("{}, {} was created on {:%d %b %Y}".format(
                app_name, url, created_date))

        cursor.close()
        cnx.close()

    # These functions delete an entry in the database, given a url
    def delete_account(self, entry_to_delete):
        cursor = self.sqlite3_connection.cursor()
        try:
            cursor.execute("Delete * FROM VAULT WHERE url = %s'", (entry_to_delete,))
        except (Exception, Error) as error:
            print(error)
        cursor.close()

    def find_password(self, app_name):

        try:
            connection = self.sqlite3_connection
            cursor = connection.cursor()
            cursor.execute("SELECT pass FROM VAULT WHERE app_name = %s'", (app_name,))
            connection.commit()
            result = cursor.fetchone()
            print('[+] Password is: ', result[0])
            cursor.close()
            connection.close()
        except sqlite3.InterfaceError as e:
            print(colored("[+] Error :", 'red'), e)

        else:
            print(colored("[-] Error...", 'red'))
            cursor.close()
            connection.close()
            exit_program()

    def find_users(self, user_email):
        data = ('Password: ', 'Email: ', 'Username: ', 'url: ', 'App/Site name: ')
        try:
            connection = self.sqlite3_connection
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
            print(colored("[+] Error :", 'red'), e)


class Oracle(Database):

    def __init__(self):
        super().__init__()
