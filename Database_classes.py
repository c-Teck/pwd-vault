#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 07:58:32 2022

@author: cybree
"""

from mysql.connector import connect, Error
import psycopg2

class Database:

    connection = mysql.connector.connect(
                                host=self.host,
                                user=self.user,
                                password=self.password,
                        )

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def all_db(self, db_type):

        match db_type:

            case MYSQL:
                def connecting():
                    try:
                        with self.connection as conn:
                            return conn
                    except Error as e:
                        print(e)

                def check_database():
                    output = connecting()
                    if output:
                        execution = self.connection.cursor()
                        try:
                            execution.execute("CREATE DATABASE PWDMGR")



                
