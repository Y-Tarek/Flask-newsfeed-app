""" This File will hold db connection. """
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  

def get_db_connection():
    connection = mysql.connector.connect(
        host= os.getenv("SQL_HOST", 'localhost'),
        user=os.getenv("SQL_USER","yasser"),          
        password=os.getenv("SQL_PASSWORD","123456"),     
        database=os.getenv("SQL_DB","newsfeed_db" )     
    )
    return connection
