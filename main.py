# Importación de librerías necesarias
from flask import Flask, render_template, request  # Flask para el servidor web
import RPi.GPIO as GPIO                            # Control de los pines GPIO de la Raspberry Pi

# Importación de funciones personalizadas para motores y servomotor
from motoresv3 import (
    inicializar_motores,    # Inicializa los motores paso a paso
    volver_al_origen,       # Mueve el cabezal al origen (posición inicial)
    cleanup_motores,        # Libera los recursos GPIO usados por los motores
    ir_y_presionar          # Mueve el cabezal a la letra especificada y presiona la tecla
)

from servomotor import (
    inicializar_servo,      # Inicializa el servomotor que presiona las teclas
    cleanup as servo_cleanup  # Libera los recursos del servomotor (renombrado para evitar confusión)
)

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración del modo de numeración de pines GPIO
GPIO.setmode(GPIO.BCM)  # Usa la numeración BCM (basada en el chip) para identificar los pines

# Inicialización del sistema al arrancar el servidor
inicializar_motores()     # Configura los motores paso a paso
inicializar_servo()       # Configura el servomotor
volver_al_origen()        # Asegura que el cabezal comience desde una posición conocida (cero)

# Función auxiliar: convierte una palabra en una lista de letras en mayúscula
def palabra_a_array(palabra):
    """
    Convierte una palabra en una lista de letras mayúsculas.

    Parámetros:
    - palabra (str): la palabra a convertir.

    Retorna:
    - list: lista de letras mayúsculas.
    """
    letras = list(palabra.strip().upper())  # Elimina espacios y convierte en mayúsculas
    print("Array de letras:", letras)       # Muestra las letras para depuración
    return letras

# Ruta principal del sitio web ("/"), permite GET y POST
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Se recibe la palabra desde el formulario HTML
        palabra = request.form["palabra"]
        print("Palabra recibida del formulario:", palabra)

        # Se convierte la palabra en una lista de letras
        letras_array = palabra_a_array(palabra)

        try:
            # Recorre cada letra y ejecuta el movimiento correspondiente
            for letra in letras_array:
                print(f"Presionando letra: {letra}")
                ir_y_presionar(letra)  # Mueve el cabezal y presiona la tecla correspondiente

            # Vuelve a la posición inicial una vez terminado
            volver_al_origen()

        except Exception as e:
            # Si ocurre algún error durante el proceso, lo muestra por consola
            print(f"Error durante el movimiento: {e}")

        finally:
            # Libera recursos siempre, ocurra o no un error
            servo_cleanup()       # Libera el servomotor
            cleanup_motores()     # Libera los motores
            GPIO.cleanup()        # Libera todos los pines GPIO usados

        # Vuelve a cargar la página con un mensaje de éxito
        return render_template("index.html", mensaje="Palabra procesada con éxito.")

    # Si la solicitud es GET (usuario carga la página sin enviar datos)
    return render_template("index.html", mensaje=None)

# Punto de entrada del programa
if __name__ == "__main__":
    # Inicia el servidor Flask en todas las interfaces de red en el puerto 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
