""" This File will contain middlware for the app """
from flask import jsonify
from db import get_db_connection 

def is_owner(model, id, current_user_email):
    """
    Mehthod that checks if authenticated user is the owner of the instance.

    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (current_user_email,))
    user = cursor.fetchone()

    query = "SELECT * FROM {} WHERE id = %s".format(model)
    cursor.execute(query, (id,))
    instance = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    if instance.get("user_id") != user.get('id'):
        return False
    return True
    