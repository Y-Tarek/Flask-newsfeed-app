""" Posts APIs """
from flask import Blueprint, request, jsonify

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('', methods=['POST'])
def create_post():
    # Your logic to create a post
    return jsonify(message="Post created"), 201

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    # Your logic to get a post
    return jsonify(post_id=post_id), 200

@posts_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    # Your logic to update a post
    return jsonify(message="Post updated"), 200

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Your logic to delete a post
    return jsonify(message="Post deleted"), 200
