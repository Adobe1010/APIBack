from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Data
from app import db

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

# Ruta para agregar un nuevo registro
@service_routes.route('/data', methods=['POST'])
def add_data():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "El campo 'name' es obligatorio"}), 400

    # Agregar nuevo registro
    new_data = Data(name=name, description=description)
    db.session.add(new_data)
    db.session.commit()

    # Obtener todos los registros para devolver
    all_data = Data.query.all()
    data_list = [{"id": d.id, "name": d.name, "description": d.description} for d in all_data]

    return jsonify({
        "message": "Datos agregados con éxito",
        "data": data_list
    }), 201


# Ruta para obtener todos los registros
@service_routes.route('/data', methods=['GET'])
def get_all_data():
    all_data = Data.query.all()
    data_list = [{"id": d.id, "name": d.name, "description": d.description} for d in all_data]
    return jsonify(data_list), 200

# Ruta para editar un registro
@service_routes.route('/data/<int:id>', methods=['PUT'])
def edit_data(id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "El campo 'name' es obligatorio"}), 400

    item = Data.query.get(id)
    if not item:
        return jsonify({"error": "Registro no encontrado"}), 404

    item.name = name
    item.description = description
    db.session.commit()

    return jsonify({"message": "Registro actualizado con éxito"}), 200

# Ruta para borrar un registro
@service_routes.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    item = Data.query.get(id)
    if not item:
        return jsonify({"error": "Registro no encontrado"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Registro eliminado con éxito"}), 200