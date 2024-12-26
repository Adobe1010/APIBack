#Este archivo configura la conexión a la base de datos y proporciona utilidades para manejar la base de datos.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Inicializa la base de datos con la aplicación Flask."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
