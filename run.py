# from app import create_app
# from email_listener import listen_for_emails

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)

#     try:
#         listen_for_emails()
#     except KeyboardInterrupt:
#         print("Cerrando conexión...")

import threading
from app import create_app
from email_listener import listen_for_emails  # Asegúrate de que este importe sea correcto


def run_flask(app):
    """Ejecuta el servidor Flask."""
    app.run(debug=False, use_reloader=False)  # Evitar usar reloader en subprocesos

def run_email_listener():
    """Ejecuta el listener de correos."""
    listen_for_emails()

if __name__ == "__main__":
    # Crear instancia de Flask utilizando la fábrica de aplicaciones
    app = create_app()

    # Iniciar el servidor Flask en un hilo
    flask_thread = threading.Thread(target=run_flask, args=(app,))
    flask_thread.start()

    # Ejecutar el listener de correos en el hilo principal
    run_email_listener()


# from app import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)