""" Posts APIs """
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .serializers import (
    PostShema,
    ReadPostSchema,
    PostCommentSchema
)
from marshmallow import ValidationError
from db import get_db_connection
import json
from middleware import is_owner
from mysql.connector.errors import IntegrityError

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    schema = PostShema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    content = validated_data.get("content",None)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (get_jwt_identity(),))
    user = cursor.fetchone()
   
    cursor.execute(
        "INSERT INTO posts (user_id, content) VALUES (%s, %s)",
        (user[0], content)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(message="Post created"), 201

@posts_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT 
            p.id, 
            p.content, 
            u.id AS author_id, 
            u.username,
            (
                SELECT COUNT(*)
                FROM likes l
                WHERE l.post_id = p.id
            ) AS like_count,
            (
                SELECT JSON_ARRAYAGG(
                    JSON_OBJECT('username', user_u.username, 'content', c.content)
                )
                FROM comments c
                JOIN users user_u ON c.user_id = user_u.id
                WHERE c.post_id = p.id
            ) AS comments
        FROM posts p
        JOIN users u ON p.user_id = u.id
        WHERE p.id = %s
            ''', (post_id,))
    post = cursor.fetchone() 
    cursor.close()
    conn.close()
    if not post:
        return jsonify({"message": "Post not found"}), 404  

    post['author'] = {'id': post['author_id'], 'username': post['username']} 
    post ['likes'] = post.get('likes_count',0)
    post['comments'] = json.loads(post.get('comments', '[]')) if post.get('comments') else [] 
    post_schema = ReadPostSchema()
    result = post_schema.dump(post) 
    return jsonify(result), 200

@posts_bp.route('/<int:post_id>', methods=['PATCH'])
@jwt_required()
def update_post(post_id):
    
    if not is_owner('posts',post_id,get_jwt_identity()):
        return jsonify({"message": "Forbidden!"}), 403

    data = request.get_json()
    schema = PostShema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    content = validated_data.get("content",None)
    conn = get_db_connection()
    cursor = conn.cursor()
        
    cursor.execute(
        "UPDATE posts SET content = %s WHERE id = %s",
        (content, post_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(message="Post updated"), 200

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):

    if not is_owner('posts',post_id,get_jwt_identity()):
        return jsonify({"message": "Forbidden!"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Post deleted successfully!'}), 200


@posts_bp.route('/comment', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    schema = PostCommentSchema()
    try:
        validated_data = schema.load(data)
    
        content = validated_data.get("content",None)
        post_id = validated_data.get("post_id",None)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (get_jwt_identity(),))
        user = cursor.fetchone()
    
        cursor.execute(
            "INSERT INTO comments (user_id, content, post_id) VALUES (%s, %s, %s)",
            (user[0], content, post_id)
        )
    
    except ValidationError as err:
        return jsonify(err.messages), 400
    except IntegrityError as e:
       return jsonify({"error": "Invalid post_id. The referenced post does not exist."}), 400
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(message="Comment created"), 201