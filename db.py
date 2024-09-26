""" This File will hold db connection. """
import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="yasser",          
        password="123456",     
        database="newsfeed_db"      
    )
    return connection
