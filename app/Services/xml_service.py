from flask import request, jsonify

def process_xml():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No se proporcionó un archivo XML"}), 400

    # Procesa el archivo XML (lógica personalizada aquí)
    # Ejemplo: datos_extraidos = parse_xml(file)
    datos_extraidos = {"example_key": "example_value"}  # Placeholder

    return jsonify(datos_extraidos), 200
