#!/usr/bin/python3
'''
THis script lists all states from the
database `hbtn_0e_0_usa.
'''

import MySQLdb
from sys import argv

if __name__ == '__main__':
    '''
    Access to the database and get the states
    from the database.
    '''
    # Establish a connection to the MySQL database
    db_connect = MySQLdb.connect(host="localhost", user=argv[1], port=3306, passwd=argv[2], db=argv[3])

    # Create a cursor object to execute SQL queries
    db_cursor = db_connect.cursor()

    # Execute SQL query to select all rows from the 'states' table
    db_cursor.execute("SELECT * FROM states")

    # Fetch all rows selected by the cursor
    row_selected = db_cursor.fetchall()

    # Iterate over the selected rows and print each row
    for row in rows_selected:
        print(row)
