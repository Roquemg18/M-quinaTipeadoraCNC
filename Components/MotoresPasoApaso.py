import RPi.GPIO as GPIO
import time
from configCNC import teclas

# Pines motores paso a paso (modo BCM)
MOTOR_X_STEP = 17
MOTOR_X_DIR  = 27
MOTOR_Y_STEP = 13
MOTOR_Y_DIR  = 19

# Configuración CNC
PASOS_POR_TECLA_X = 2800  # Ajustable según calibración
PASOS_POR_TECLA_Y = 2600  # Ajustable según calibración
pos_actual = [0.0, 0.0]   # Posición actual X, Y en float



# Inicializa los pines GPIO asociados a los motores paso a paso.
# @parametros: ninguno
# Pre-condiciones: GPIO.setmode(GPIO.BCM) ya debe estar configurado
# Post-condiciones: los pines de salida quedan configurados para emitir pulsos a los drivers A4988
def inicializar_motores():
    GPIO.setup(MOTOR_X_STEP, GPIO.OUT)
    GPIO.setup(MOTOR_X_DIR, GPIO.OUT)
    GPIO.setup(MOTOR_Y_STEP, GPIO.OUT)
    GPIO.setup(MOTOR_Y_DIR, GPIO.OUT)


# Mueve un motor una cantidad arbitraria (float) de pasos con direccion y retardo ajustable.
# @parametros: step_pin (GPIO del pin de paso), dir_pin (GPIO del pin de dirección),
#              pasos_float (cantidad de pasos, puede ser decimal), direccion (True = adelante), delay
# Pre-condiciones: Los pines deben estar inicializados
# Post-condiciones: el motor se movera en la dirección y pasos especificados
def mover_motor(step_pin, dir_pin, pasos_float, direccion=True, delay=0.001):
    """
    Mueve un motor paso a paso una cantidad (float) de pasos.
    """
    GPIO.output(dir_pin, GPIO.HIGH if direccion else GPIO.LOW)
    acumulador = 0.0
    pasos_realizados = 0
    pasos_totales = int(pasos_float) + 1  # Redondeamos hacia arriba

    while pasos_realizados < pasos_totales:
        acumulador += pasos_float / pasos_totales
        if acumulador >= 1.0:
            GPIO.output(step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(step_pin, GPIO.LOW)
            time.sleep(delay)
            pasos_realizados += 1
            acumulador -= 1.0

# Mueve ambos motores hacia la posición absoluta deseada, actualizando la posición actual.
# @parametros: destino (tupla de coordenadas X, Y)
# Pre-condiciones: El sistema debe estar inicializado. El valor destino debe ser un par numérico.
# Post-condiciones: El sistema se posiciona en el nuevo punto.
def mover_a(destino):
    global pos_actual
    dx = destino[0] - pos_actual[0]
    dy = destino[1] - pos_actual[1]

    mover_motor(MOTOR_X_STEP, MOTOR_X_DIR, abs(dx) * PASOS_POR_TECLA_X, direccion=(dx >= 0))
    mover_motor(MOTOR_Y_STEP, MOTOR_Y_DIR, abs(dy) * PASOS_POR_TECLA_Y, direccion=(dy >= 0))

    pos_actual = list(destino)

# Mueve el cabezal hacia una tecla específica y activa el servo para presionarla.
# @parametros: tecla (string con el nombre de la tecla, según el mapa de teclas)
# Pre-condiciones: Servo inicializado. La tecla debe estar en el diccionario.
# Post-condiciones: Se simula la pulsación física de la tecla.
def ir_y_presionar(tecla):
    from servomotor import presionar_tecla  # Importación interna para evitar errores si el servo no está conectado

    if tecla not in teclas:
        raise ValueError(f"Tecla {tecla} no reconocida.")
    
    destino = teclas[tecla]
    mover_a(destino)
    presionar_tecla()

# Regresa el cabezal al punto de origen (0.0, 0.0)
# @parametros: ninguno
# Pre-condiciones: motores inicializados
# Post-condiciones: el sistema vuelve al origen
def volver_al_origen():
    mover_a((0.0, 0.0))

# Detiene los motores apagando la señal de paso.
# @parametros: ninguno
# Pre-condiciones: motores inicializados
# Post-condiciones: se liberan los recursos de control de motores
def cleanup_motores():
    GPIO.output(MOTOR_X_STEP, GPIO.LOW)
    GPIO.output(MOTOR_Y_STEP, GPIO.LOW)