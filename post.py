from flask import Blueprint, request, jsonify
from models import db, Post
from flask_jwt_extended import jwt_required, get_jwt_identity

posts = Blueprint("posts", __name__)

@posts.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([
        {"id": p.id, "content": p.content, "user_id": p.user_id}
        for p in posts
    ])

@posts.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.json

    post = Post(content=data["content"], user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify(message="Post creado")
