#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 07:58:32 2022

@author: cybree
"""
# Create a Database Class that support MYSQl, psycopg2,
from master_pwd import Validate

from termcolor import colored

from database_manager import Mysql, Postgres, Sqlite, Oracle


def db_to_run(db_type):

    if db_type == 'postgres':
        return Postgres()

    elif db_type == 'mysql':
        return Mysql()

    elif db_type == 'sqlite':
        return Sqlite()

    elif db_type == 'oracle':
        return Oracle()

    else:
        print(colored("[-] Specified database ({}) does not exist, try specifying your database type...", 'red').
              format(db_type))


def get_salt(db_type, table, salt):
    run = db_to_run(db_type)
    conn = run.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM {} WHERE key = %s'", (salt,)).format(table)
    result = cursor.fetchone()
    cursor.close()
    return result


def get_master(db_type, table, key):
    run = db_to_run(db_type)
    conn = run.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM {} WHERE key = %s'", (key,)).format(table)
    result = cursor.fetchone()
    cursor.close()
    return result


def get_master_plain(db_type, master_input):
    two_factor = get_salt(db_type, 'settings', 'SALT')

    second_fa_location = two_factor.encode()

    master_pwd = Validate(master_input)

    if master_pwd.query_master_pwd(second_fa_location):
        return master_input

    else:
        print("[-] Something went wrong...")


