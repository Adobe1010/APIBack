# Módulo para manejar los archivos adjuntos
import os
from app.Utils.xml_handler import process_xml
from app.Utils.zip_handler import extract_zip
import tempfile
import shutil


def process_attachment(filepath):
    """Procesa los archivos adjuntos recibidos."""
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Procesando archivo: {filepath}")
        if filepath.endswith(".xml"):
            process_xml(filepath)
        elif filepath.endswith(".zip"):
            extracted_files = extract_zip(filepath, temp_dir) # Usa el directorio temporal
            for file in extracted_files:
                if file.endswith(".xml"):
                    process_xml(file)
        else:
            print(f"Formato no soportado: {filepath}")  
