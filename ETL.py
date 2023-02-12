# script to display the info of all the tables present in a database and perform ETL operations

import psycopg2
from tabulate import tabulate

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

def close_database(conn, cur):
    conn.close()
    cur.close()

def info(cur):
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

        # Table Row Count
        table_rows = []
        for table in table_names:
            string = "select count(*) from " + table + ";"
            cur.execute(string)
            table_rows.append(cur.fetchone()[0])

        # Table column name and it's datatype
        tables_info = []
        for table in table_names:
            string = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '" + table + "';"
            cur.execute(string)
            t = []
            row = cur.fetchone()
            while row:
                t.append([row[0], row[1]])
                row = cur.fetchone()
            tables_info.append(t)

        # Displaying all info
        head = ["Column Name", "Data Type"]
        for i in range(0, len(tables_info)):
            print(table_names[i], '[', table_rows[i], ']')
            print(tabulate(tables_info[i], headers=head, tablefmt="grid"))
            print()

    except Exception as e:
        print('\nError! Something has gone wrong.')
        print(e)

def ETL(cur):
    cur.execute(open("ETL.sql", "r").read())
    print('\n ETL Completed! \n')

if __name__ == "__main__":
    # Values for connecting
    host = input('Enter host - ')
    user = input('Enter user - ')
    password = input('Enter password - ')
    database_name = input('Enter database name to connect with - ')

    # Connect to database
    conn, cur = connect_database(host, user, database_name, password)

    # Basic info and ETL
    if conn != None and cur != None:
        info(cur)
        ETL(cur)
        close_database(conn, cur)