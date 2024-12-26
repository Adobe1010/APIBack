from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializa la app y la base de datos
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define el modelo User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

with app.app_context():
    # Crea las tablas en la base de datos
    db.create_all()

    # Verificar si el usuario ya existe
    existing_user = User.query.filter_by(email="martinezzapata1010@gmail.com").first()

    if existing_user:
        print("El usuario ya existe")
    else:
        # Hashea la contraseña para almacenamiento seguro
        hashed_password = generate_password_hash("1000452782")
        
        # Crea el nuevo usuario
        user = User(email="martinezzapata1010@gmail.com", password=hashed_password)
        db.session.add(user)
        db.session.commit()
        print("Usuario creado exitosamente")

# Código para verificar la contraseña durante el login (Ejemplo)
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return True  # Contraseña válida
    else:
        return False  # Contraseña incorrecta o usuario no encontrado
