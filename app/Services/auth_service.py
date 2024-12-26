from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuario registrado con éxito"}), 201

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify({"access_token": access_token}), 200
