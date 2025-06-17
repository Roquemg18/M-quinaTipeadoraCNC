from flask import Flask, render_template, request
#from cnc_controller import moverCNC

app = Flask(__name__)

def palabra_a_array(palabra):
    return list(palabra.strip().upper())  # Convertimos a mayúscula por si el CNC es case-sensitive

def enviar_a_cnc(array_letras):
    for letra in array_letras:
        moverCNC(letra)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        palabra = request.form["palabra"]
        letras_array = palabra_a_array(palabra)
        enviar_a_cnc(letras_array)
        return render_template("index.html", mensaje="Palabra enviada al CNC correctamente.")
    return render_template("index.html", mensaje=None)

if __name__ == "__main__":
    app.run(debug=True)
