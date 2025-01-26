"""Este servicio ejecutará la lógica del scraping y estará ubicado en la carpeta services."""
from app import db
from app.models import Data
import subprocess  # Usamos subprocess para ejecutar el script de scraping
import os


# Ruta al script de scraping
SCRAPING_SCRIPT_PATH = os.path.join(os.getcwd(), 'scraping_dian.py')

def ejecutar_scraping(access_token_url, fecha_inicio, fecha_fin, procesar_enviados, procesar_recibidos):
    """
    Ejecuta el script de scraping utilizando los parámetros recibidos.
    """

    # Construir los comandos para pasar al script de scraping
    command = [
        'python', SCRAPING_SCRIPT_PATH,
        access_token_url, fecha_inicio, fecha_fin,
        str(procesar_enviados), str(procesar_recibidos)
    ]

    try:
        # Ejecutar el script de scraping en segundo plano
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            raise Exception(f"Error en la ejecución del scraping: {result.stderr}")
        
        # Procesar la salida del script de scraping
        print("Resultado del scraping:", result.stdout)
        return result.stdout  # O procesar el resultado según tus necesidades

    except Exception as e:
        print(f"Error al ejecutar el scraping: {str(e)}")
        return str(e)
