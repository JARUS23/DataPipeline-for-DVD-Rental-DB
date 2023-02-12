# script to create database in postgresQL

import psycopg2

def create_database(host, user, password, dbname):
    try:
        con_string = "host = " + host + " dbname = postgres" + " user = " + user + " password = " + password
        conn = psycopg2.connect(con_string)
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        cur.execute('create database ' + dbname + ';')

        print('\n', dbname, ' DATABASE CREATED')

        cur.close()
        conn.close()
    except Exception as e:
        print('\nError! Something has gone wrong.')
        print(e)

if __name__ == "__main__":
    # Values for connecting
    host = input('Enter host - ')
    user = input('Enter user - ')
    password = input('Enter password - ')
    database_name = input('Enter database name to be created - ')

    # Creating a database
    create_database(host, user, password, database_name)