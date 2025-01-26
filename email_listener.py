from imapclient import IMAPClient
from email import message_from_bytes
from email.header import decode_header
import os
from file_processor import process_attachment
from config import EMAIL_CONFIG
from concurrent.futures import ThreadPoolExecutor
import time

def create_folder(folder_path):
    """Crea una carpeta si no existe."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def connect_to_gmail():
    """Establece conexión con Gmail usando IMAPClient."""
    try:
        conn = IMAPClient(EMAIL_CONFIG["imap_server"], ssl=True)
        print("Conexión al servidor IMAP establecida.")
        conn.login(EMAIL_CONFIG["email"], EMAIL_CONFIG["password"])
        print("Inicio de sesión exitoso.")
        conn.select_folder(EMAIL_CONFIG["mailbox"])
        print(f"Buzón seleccionado: {EMAIL_CONFIG['mailbox']}")
        return conn
    except IMAPClient.Error as e:
        print(f"Error al conectar con Gmail: {e}")
        raise
    except Exception as e:
        print(f"Error al conectar con Gmail: {e}")
        raise


def process_new_email(msg_data):
    """Procesa un correo nuevo."""
    msg = message_from_bytes(msg_data[b"RFC822"])
    subject = decode_header(msg["Subject"])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode()  # Decodificar si es necesario
    sender = msg.get("From")
    print(f"Correo recibido de {sender} con asunto: {subject}")
    
    # Procesar adjuntos si existen
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    save_path = os.path.join("attachments", filename)
                    create_folder("attachments")
                    with open(save_path, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Adjunto guardado: {save_path}")
                    process_attachment(save_path)  # Procesa el archivo adjunto

def listen_for_emails():
    """Escucha correos en tiempo real usando IMAPClient.idle()."""
    conn = connect_to_gmail()
    print("Conexión establecida. Escuchando nuevos correos...")
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                messages = conn.search("UNSEEN")  # Buscar correos no leídos
                for msg_id in messages:
                    msg_data = conn.fetch(msg_id, ["RFC822"])[msg_id]
                    executor.submit(process_new_email, msg_data)

                # Entrar en modo idle y esperar interrupciones manuales
                conn.idle() # Pone al cliente en modo "idle" para escuchar nuevos correos.
                print("En modo idle...")
                time.sleep(300)  # Hace que el programa espere 5 minutos (300 segundos) antes de buscar correos nuevamente.
                conn.idle_done()  # Sale del modo "idle" para realizar otra búsqueda de correos.
    except KeyboardInterrupt:
        print("Cerrando conexión...")
    finally:
        conn.logout()
