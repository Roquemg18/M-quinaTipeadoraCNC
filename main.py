from flask import Flask, render_template, request
import RPi.GPIO as GPIO
from motoresv3 import inicializar_motores, volver_al_origen, cleanup_motores, ir_y_presionar
from servomotor import inicializar_servo, cleanup as servo_cleanup

app = Flask(__name__)

# Configuración GPIO
GPIO.setmode(GPIO.BCM)

# Inicialización del sistema al arrancar
inicializar_motores()
inicializar_servo()
volver_al_origen()

def palabra_a_array(palabra):
    letras = list(palabra.strip().upper())
    print("Array de letras:", letras)
    return letras

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        palabra = request.form["palabra"]
        print("Palabra recibida del formulario:", palabra)
        letras_array = palabra_a_array(palabra)

        try:
            for letra in letras_array:
                print(f"Presionando letra: {letra}")
                ir_y_presionar(letra)
            volver_al_origen()
        except Exception as e:
            print(f"Error durante el movimiento: {e}")
        finally:
            servo_cleanup()
            cleanup_motores()
            GPIO.cleanup()

        return render_template("index.html", mensaje="Palabra procesada con éxito.")
    
    return render_template("index.html", mensaje=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
