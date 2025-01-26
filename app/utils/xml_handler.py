# Procesar los XML
import os
import xml.etree.ElementTree as ET

# Definir los namespaces que usaremos
namespaces = {
    'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
    'sts': 'dian:gov:co:facturaelectronica:Structures-2-1',
    'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
    'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
    'xmlns': 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2',
    'xades': 'http://uri.etsi.org/01903/v1.3.2#',
    'xades141': 'http://www.uri.etsi.org/01903/v1.4.1#',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'ds': 'http://www.w3.org/2000/09/xmldsig#',
    'ns5': 'urn:oasis:names:specification:ubl:schema:xsd:SignatureBasicComponents-2',
    'ns7': 'urn:oasis:names:specification:ubl:schema:xsd:SignatureAggregateComponents-2',
    'ns9': 'urn:oasis:names:specification:ubl:schema:xsd:CommonSignatureComponents-2',
    'smb': 'http://www.simba.co/DocumentoElectronico',
    'nomina': 'dian:gov:co:facturaelectronica:NominaIndividual'
}

def extract_unique_data(tree, xpath, namespaces, attribute=None):
    """Extrae datos únicos de un nodo XML usando XPath."""
    try:
        element = tree.find(xpath, namespaces)
        if element is not None:
            return element.get(attribute) if attribute else element.text
        return "No encontrado"
    except Exception as e:
        return f"Error: {e}"
    

def process_xml(filepath):
    """Procesa un archivo XML y extrae datos clave."""
    try:
        print(f"Extrayendo datos del XML: {filepath}")

        # Parsear el archivo XML
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Extraer datos clave usando el prefijo y los espacios de nombres
        id_value = extract_unique_data(root, ".//cbc:ID", namespaces)
        profile_id_value = extract_unique_data(root, ".//cbc:ProfileID", namespaces)

        # Mostrar los valores extraídos
        print(f"ID: {id_value}, ProfileID: {profile_id_value}")
        
        # Aquí puedes guardar los datos en la base de datos o procesarlos
    except ET.ParseError as e:
        print(f"Error al procesar el XML {filepath}: {e}")
    except AttributeError as e:
        print(f"Error al extraer datos del XML {filepath}: {e}")
    finally:
        os.remove(filepath)  # Limpieza del archivo procesado

    # Aquí puedes guardar los datos en la base de datos
