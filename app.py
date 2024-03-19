from flask import Flask, render_template, request, send_file
import re
import os



app = Flask(__name__, static_folder='static')

# Función para simplificar el texto
def simplify_text(input_text):
    # Elimina la sección 'TAKES SCRIPT' junto con la referencia y la línea de guiones
    simplified_text = re.sub(
        r"TAKES SCRIPT\s+Ref:.*?={30,}\n", "", input_text, flags=re.DOTALL
    )
    # Elimina las líneas que contienen 'Title:', 'Engineer:' y 'Chapter:'
    simplified_text = re.sub(
        r"Title:.*?\nEngineer:.*?\nChapter:.*?\n", "", simplified_text
    )
    # Elimina las líneas que contienen 'DURATION: '
    simplified_text = re.sub(r"DURATION: .*?\n", "", simplified_text)
    # Elimina las líneas que contienen 'TAKES SCRIPT '
    simplified_text = re.sub(r"TAKES SCRIPT .*?\n", "", simplified_text)
    # Elimina 'IN: '
    simplified_text = re.sub(r"IN: ", "", simplified_text)
    # Mantiene el tiempo después de 'IN: '
    simplified_text = re.sub(
        r"(IN: \d{2}:\d{2}:\d{2}:\d{2})", r"\n\1", simplified_text
    )  # Agrega un salto de línea antes del tiempo de IN
    # Elimina 'OUT: ' y agrega un salto de línea antes
    simplified_text = re.sub(r"OUT: ", "\n", simplified_text)
    # Mantiene el tiempo después de 'OUT: '
    simplified_text = re.sub(
        r"(OUT: \d{2}:\d{2}:\d{2}:\d{2})", r"\1\n", simplified_text
    )  # Agrega un salto de línea después del tiempo de OUT
    # Agrega un salto de línea antes de cada instancia de 'TAKE'
    simplified_text = re.sub(r"(TAKE \d+\s+Track \d+)", r"\n\1", simplified_text)
    # Elimina líneas con una serie de caracteres repetidos
    simplified_text = re.sub(r"(-+.*?(\n|$))", "", simplified_text)
    simplified_text = re.sub(r"={10,}", "", simplified_text)
    # Elimina las líneas que contienen 'DURATION: '
    simplified_text = re.sub(r"Dialog Spotting 2.0.*?\n", "", simplified_text)
    return simplified_text


# Ruta para la página de inicio
@app.route("/")
def index():
    return render_template("index.html")


# Ruta para procesar el archivo de entrada y mostrar el resultado
@app.route("/process", methods=["POST"])
def process():
    if request.method == "POST":
        input_file = request.files["inputFile"]
        if input_file:
            input_text = input_file.read().decode("latin-1")  # Cambio a latin-1
            simplified_text = simplify_text(input_text)
            # Obtiene el nombre del archivo sin la extensión
            filename_no_extension = os.path.splitext(input_file.filename)[0]
            # Crea el nombre del archivo modificado
            modified_filename = f"{filename_no_extension}-simplificado.txt"
            # Guarda el texto simplificado en un archivo temporal
            with open(modified_filename, "w") as file:
                file.write(simplified_text)
            # Envía el archivo como respuesta para descargar
            return send_file(modified_filename, as_attachment=True)


# Si se ejecuta como script principal, inicia la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)
