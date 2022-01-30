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
from enum import Enum
import mysql.connector
from dotenv import load_dotenv
from main import exit_program
from mysql.connector import connect, Error, errorcode
from master_pwd import Validate
from termcolor import colored


class Database(object):

    def __init__(self):
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
            ") ENGINE=InnoDB"), 'settings': (
            "CREATE TABLE `settings` ("
            "  `id` int(10) NOT NULL AUTO_INCREMENT,"
            "  `key` varchar(40) NOT NULL,"
            "  `value` TEXT NOT NULL,"
            "  PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB")
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
