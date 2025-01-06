from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import jsonify

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Importa configuración desde config.py
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})  # Permite solicitudes desde cualquier origen (puedes restringirlo según necesidad)
#Reemplaza "http://localhost:4200" con el dominio de producción cuando estés listo

    # Inicialización de extensiones
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Registro de Blueprints - Registro de rutas
    from app.routes import auth_routes, service_routes
    app.register_blueprint(auth_routes, url_prefix='/api/auth')
    app.register_blueprint(service_routes, url_prefix='/api/services')

    # Ruta raíz
    @app.route('/')
    def index():
        return jsonify({"message": "Bienvenido al backend de la API"}), 200    
    
    with app.app_context():
        db.create_all()

    return app
