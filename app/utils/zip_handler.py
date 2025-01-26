# Procesar los ZIP
import zipfile
import os

def create_folder(folder_path):
    """Crea una carpeta si no existe."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def extract_zip(filepath, output_dir):
    """Extrae archivos de un ZIP."""
    extracted_files = []
    try:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            create_folder(output_dir)
            zip_ref.extractall(output_dir)
            extracted_files = [os.path.join(output_dir, name) for name in zip_ref.namelist()]
            print(f"Archivos extraídos: {extracted_files}")
    except zipfile.BadZipFile:
        print(f"El archivo ZIP está dañado: {filepath}")
    except Exception as e:
        print(f"Error extrayendo ZIP: {e}")
    return extracted_files
