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


def inicializar_motores():
    GPIO.setup(MOTOR_X_STEP, GPIO.OUT)
    GPIO.setup(MOTOR_X_DIR, GPIO.OUT)
    GPIO.setup(MOTOR_Y_STEP, GPIO.OUT)
    GPIO.setup(MOTOR_Y_DIR, GPIO.OUT)


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


def mover_a(destino):
    global pos_actual
    dx = destino[0] - pos_actual[0]
    dy = destino[1] - pos_actual[1]

    mover_motor(MOTOR_X_STEP, MOTOR_X_DIR, abs(dx) * PASOS_POR_TECLA_X, direccion=(dx >= 0))
    mover_motor(MOTOR_Y_STEP, MOTOR_Y_DIR, abs(dy) * PASOS_POR_TECLA_Y, direccion=(dy >= 0))

    pos_actual = list(destino)


def ir_y_presionar(tecla):
    from servomotor import presionar_tecla  # Importación interna para evitar errores si el servo no está conectado

    if tecla not in teclas:
        raise ValueError(f"Tecla {tecla} no reconocida.")
    
    destino = teclas[tecla]
    mover_a(destino)
    presionar_tecla()


def volver_al_origen():
    mover_a((0.0, 0.0))


def cleanup_motores():
    GPIO.output(MOTOR_X_STEP, GPIO.LOW)
    GPIO.output(MOTOR_Y_STEP, GPIO.LOW)