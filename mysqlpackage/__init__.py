import os
import mysql.connector


database_name = 'db'
table_name = 'informations_real_estate'

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password=os.environ.get('Password'),
    database=database_name
)
