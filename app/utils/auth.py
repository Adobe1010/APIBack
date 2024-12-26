from flask import request, jsonify
import jwt

SECRET_KEY = "your_secret_key"

def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization', None)

        if not token:
            return jsonify({"message": "Token es requerido"}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token ha expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorator
