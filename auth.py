from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.json

    user = User(
        username=data["username"],
        password=data["password"],
        role=data.get("role", "user")
    )

    db.session.add(user)
    db.session.commit()
    return jsonify(message="Usuario creado")


@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if not user or user.password != data["password"]:
        return jsonify(message="Credenciales incorrectas"), 401

    token = create_access_token(identity=user.id)
    return jsonify(token=token, role=user.role)
