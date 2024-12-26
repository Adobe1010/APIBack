from flask_jwt_extended import jwt_required, get_jwt_identity

def protected_route():
    @jwt_required()
    def inner_function():
        user_email = get_jwt_identity()
        return {"message": f"Hello, {user_email}"}
    return inner_function
