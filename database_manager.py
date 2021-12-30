#!/usr/bin/env python3

import psycopg2

def store_passwords(password, user_email, username, url, app_name):
    try:
        connection = connect()
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO VAULT (password, email, username, url, app_name) VALUES (%s, %s, %s, %s, %s)"""
        record_to_insert = (password, user_email, username, url, app_name)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print(error)

def connect():
    try:
        #connection = psycopg2.connect(user='kalle', password='kalle', host='127.0.0.1', database='password_manager')
            # Enter password under ******** field.
        data_base = input("[+] Enter your databse name here :")
        user_name = input("[+] Enter your database username here :")
        pwd = input ("[+] Enter your database password here :")
        host = input("[+] Enter your Database Ip here : ")
        connection = psycopg2.connect(user=user_name, password=pwd, host=host, database=data_base)
        return connection
    except (Exception, psycopg2.Error) as error:
        print(error + " [-]Failed to connect to Database...")

def find_password(app_name):
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM VAULT WHERE app_name = %s'", (app_name, ));
        #postgres_select_query = """ SELECT password FROM VAULT WHERE app_name = '""" + app_name + "'"
        #cursor.execute(postgres_select_query, app_name)
        connection.commit()
        result = cursor.fetchone()
        print('Password is: ' )
        print(result[0])

    except (Exception, psycopg2.Error) as error:
        print(error)
def find_users(user_email):
    data = ('Password: ', 'Email: ', 'Username: ', 'url: ', 'App/Site name: ')
    try:
        connection = connect()
        cursor = connection.cursor()
        #postgres_select_query = """ SELECT * FROM VAULT WHERE email = '""" + user_email + "'"
        #cursor.execute(postgres_select_query, user_email)
        cursor.execute("SELECT * FROM VAULT WHERE email = %s'", (user_email, ));
        connection.commit()
        result = cursor.fetchall()
        print('')
        print('RESULT')
        print('')
        for row in result:
            for i in range(0, len(row)-1):
                print(data[i] + row[i])
        print('')
        print('-'*30)
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
        cursor.execute("Delete * FROM VAULT WHERE app_name = %s'", (entry, ));
    except (Exception, psycopg2.Error) as error:
        print(error)

def update_details(ansa):


    if ansa == '1' :
        try:
            App = input("[+] Provide the url where you want to change the Email : ")
            New = input("[+] provide the new Email \n >>> ")
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("UPDATE VAULT set email = %s' WHERE app_name= %s'", (New, App));
        except (Exception, psycopg2.Error) as error:
            print(error)
    elif ansa == '2':
        try:
            App = input("[+] Provide the url where you want to change the password : ")
            New = input("[+] provide the new password \n >>> ")
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("UPDATE VAULT set password = %s' WHERE app_name= %s'", (New, App));
        except (Exception, psycopg2.Error) as error:
            print(error)

    elif ansa == '3' :
        try:
            App = input("[+] Provide the url where you want to change the Username : ")
            new = input("[+] provide the new username \n >>> ")
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("UPDATE VAULT set username = %s' WHERE app_name= %s'", (new, App));
        except (Exception, psycopg2.Error) as error:
            print(error)

    elif ansa == '4' :
        try:
            App = input("[+] Provide the url where you want to change the Url : ")
            New = input("[+] provide the new Url \n >>> ")
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("UPDATE VAULT set url = %s' WHERE app_name= %s'", (New, App));
        except (Exception, psycopg2.Error) as error:
            print(error)

    else :
        print("Invalid input")
