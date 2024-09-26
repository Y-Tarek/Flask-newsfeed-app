""" Authentication APIs """
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from marshmallow import ValidationError
from .serializers import UserRegisterSchema, UserLoginSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    schema = UserRegisterSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    username = validated_data.get('username',None)
    email = validated_data.get('email',None)
    password = validated_data.get('password',None)
    
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_password)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(message="User registered"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    schema = UserLoginSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    email = validated_data.get('email')
    password = validated_data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user[3], password):
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
    else:
        return jsonify({"error": "email or password is incorrect" }), 200
