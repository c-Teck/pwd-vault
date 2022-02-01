#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 07:58:32 2022

@author: cybree
"""
# Create a Database Class that support MYSQl, psycopg2,

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
