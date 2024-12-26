from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User

auth_routes = Blueprint('auth_routes', __name__)
service_routes = Blueprint('services', __name__)

@auth_routes.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):  # Verifica el hash de la contraseña
        access_token = create_access_token(identity=user.email)
        return jsonify({"token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth_routes.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenido a la API. Usa las rutas documentadas."}), 200

# Importar endpoints para cada Blueprint
from app.Services.auth_service import register, login
from app.Services.xml_service import process_xml
from app.Services.pdf_service import process_pdf

# Autenticación
auth_routes.add_url_rule('/auth/register', 'register', register, methods=['POST'])
#auth_routes.add_url_rule('/login', 'login_post', login_post, methods=['POST'])

# Servicios
service_routes.add_url_rule('/services/xml', 'process_xml', process_xml, methods=['POST'])
service_routes.add_url_rule('/services/pdf', 'process_pdf', process_pdf, methods=['POST'])
