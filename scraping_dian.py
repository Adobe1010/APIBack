#%% Super mejor este se ejecuta en segundo plano
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import re
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
# Parámetros pasados desde la línea de comandos
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Error: Se requieren 5 parámetros: access_token_url, fecha_inicio, fecha_fin, procesar_enviados, procesar_recibidos")
        sys.exit(1)

    access_token_url = sys.argv[1]
    fecha_inicio = sys.argv[2]
    fecha_fin = sys.argv[3]
    procesar_enviados = sys.argv[4].lower() == 'true'
    procesar_recibidos = sys.argv[5].lower() == 'true'

    if not is_valid_url(access_token_url):
        print("Error: 'access_token_url' no es una URL válida")
        sys.exit(1)

    # Lógica del scraping usando las variables
    print(f"Access Token URL: {access_token_url}")
    print(f"Fecha Inicio: {fecha_inicio}, Fecha Fin: {fecha_fin}")
    print(f"Procesar Enviados: {procesar_enviados}, Procesar Recibidos: {procesar_recibidos}")

# Variables dinámicas
received_docs_url = "https://catalogo-vpfe.dian.gov.co/Document/Received"
sent_docs_url = "https://catalogo-vpfe.dian.gov.co/Document/Sent"
# access_token_url = input("Por favor, introduce el access token: ")
# fecha_inicio = "2024/12/01"
# fecha_fin = "2024/12/31"

# Configuración del navegador en modo headless
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # Modo headless (ejecución en segundo plano)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")  # Opcional, mejora rendimiento en ciertos entornos
options.add_argument("--log-level=3")  # Reduce la salida de logs
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

def acceder_token(access_token_url):
    try:
        driver.get(access_token_url)
        print("Página de DIAN abierta exitosamente.")
        WebDriverWait(driver, 15).until(EC.url_contains("catalogo-vpfe.dian.gov.co"))
    except TimeoutException:
        print("Error al acceder al token o redirección fallida.")
        driver.quit()

def abrir_documentos(url):
    driver.get(url)
    print(f"Panel de documentos {'Recibidos' if 'Received' in url else 'Enviados'} abierto exitosamente.")

def establecer_rango_fechas(fecha_inicio, fecha_fin):
    try:
        fecha_rango_input = wait.until(EC.presence_of_element_located((By.ID, "dashboard-report-range")))
        fecha_rango_input.clear()
        fecha_rango_input.send_keys(f"{fecha_inicio} - {fecha_fin}")
        fecha_rango_input.send_keys(Keys.TAB)
        print(f"Rango de fechas establecido: {fecha_inicio} - {fecha_fin}")
        time.sleep(2)
                    
    except TimeoutException:
        print("Error al establecer el rango de fechas.")
        driver.quit()
        
def cerrar_menu ():
    # Verificar si el menú está visible e intentar cerrarlo
    try:
        boton_cerrar_menu = driver.find_element(By.ID, "close-menu-button")
        if boton_cerrar_menu.is_displayed():
            boton_cerrar_menu.click()
            print("Menú lateral cerrado.")
    except NoSuchElementException:
        print("Menú lateral no está visible o ya está cerrado.")

def buscar_documentos():
    try:
        boton_buscar = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-success btn-radian-success" and @type="submit"]')))
        boton_buscar.click()
        print("Búsqueda de documentos realizada exitosamente.")
        time.sleep(2)
    except TimeoutException:
        print("Error al realizar la búsqueda de documentos.")
        driver.quit()

def descargar_documentos():
    while True:
        # Buscar elementos con ambas clases
        botones_descarga = driver.find_elements(By.CLASS_NAME, "download-document")
        botones_descarga_extra = driver.find_elements(By.CSS_SELECTOR, ".fa.fa.fa-download.add-tooltip")
        
        # Combinar ambas listas de botones
        todos_los_botones = botones_descarga + botones_descarga_extra
        print(f"Descargando {len(todos_los_botones)} documentos en la página actual.")
        
        # Intentar descargar cada documento
        for boton in todos_los_botones:
            try:
                boton.click()
                time.sleep(2)
            except Exception as e:
                print(f"Error al descargar documento: {e}")
                
                # Navegar a la siguiente página
        try:
            boton_siguiente = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "paginate_button next") and not(contains(@class, "disabled"))]')))
            boton_siguiente.click()
            print("Navegando a la siguiente página.")
            time.sleep(3)
        except (TimeoutException, NoSuchElementException):
            print("Última página alcanzada. Terminando proceso.")
            break

def procesar_documentos(url, descripcion, fecha_inicio, fecha_fin):
    abrir_documentos(url)
    establecer_rango_fechas(fecha_inicio, fecha_fin)
    cerrar_menu()
    buscar_documentos()
    cerrar_menu()
    descargar_documentos()
    print(f"Proceso completado para documentos {descripcion}.")

def iniciar_scraping(access_token_url, fecha_inicio, fecha_fin, procesar_enviados, procesar_recibidos):
    if not access_token_url or not fecha_inicio or not fecha_fin:
        return {"error": "Todos los campos son obligatorios"}, 400
    
    resultados = {}
    try:
        # Acceder al portal de la DIAN
        acceder_token(access_token_url)

        # Procesar documentos recibidos
        if procesar_recibidos:
            procesar_documentos(received_docs_url, "Recibidos", fecha_inicio, fecha_fin)
            resultados['recibidos'] = "Procesado con éxito"
        else:
            resultados['recibidos'] = "Omitido"

        # Procesar documentos enviados
        if procesar_enviados:
            procesar_documentos(sent_docs_url, "Enviados", fecha_inicio, fecha_fin)
            resultados['enviados'] = "Procesado con éxito"
        else:
            resultados['enviados'] = "Omitido"
    finally:
        driver.quit()
        print("Proceso completado y navegador cerrado.")

    return resultados

if __name__ == "__main__":
    iniciar_scraping()
