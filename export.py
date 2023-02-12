# script to export the tables of a database to CSV file

import psycopg2
import sys
import os
import subprocess

def connect_database(host, user, dbname, password):
    try:
        con_string = "host = " + host + " dbname = " + dbname + " user = " + user + " password = " + password
        conn = psycopg2.connect(con_string)
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        return conn, cur
    except Exception as e:
        print('\nError! Something has gone wrong.')
        print(e)
        return None, None

def display(cur):
    try:
        # All table names from database
        string = '''SELECT table_name 
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;'''
        cur.execute(string)

        # Table names
        table_names = []
        row = cur.fetchone()
        while row:
            table_names.append(row[0])
            row = cur.fetchone()

        return table_names
    except Exception as e:
        print('\nError! Something has gone wrong.')
        print(e)

def export_CSV(cur, table_name):
    try:
        string = "COPY (select * from " + table_name + ") TO STDOUT WITH(FORMAT CSV, HEADER);"

        # Dir to be exported
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, r'exported/')
        file_path = file_path + table_name + '.csv'

        with open(file_path, "w") as file:
            cur.copy_expert(string, file)

        print("Exported Successful!")
    except Exception as e:
        print('\nError! Something has gone wrong.')
        print(e)


if __name__ == "__main__":
    # Values for connecting
    host = input('Enter host - ')
    user = input('Enter user - ')
    password = input('Enter password - ')
    database_name = input('Enter database name to connect with - ')
    print()

    # Connect to database
    conn, cur = connect_database(host, user, database_name, password)

    if conn != None and cur != None:
        # Displaying all the available tables in a database
        print('Please select from the available tables:-')
        for table in display(cur):
            print(table)
        table_name = input('Enter - ')
        print()

        # Exporting it to CSV
        export_CSV(cur, table_name)