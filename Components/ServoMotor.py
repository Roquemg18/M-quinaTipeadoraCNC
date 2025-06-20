# servomotor.py
import RPi.GPIO as GPIO
import time

# Pin del servo en modo BCM
SERVO_PIN = 26
servo = None

# Convierte un ángulo de 0 a 180 grados a un duty cycle compatible con servos SG90
# @parametros: angle (número entre 0 y 180)
# Pre-condiciones: valor numérico dentro del rango
# Post-condiciones: retorna el valor del duty cycle equivalente
def angle_to_percent(angle):
    """
    Convierte un ángulo (0–180°) a porcentaje de duty cycle
    para un PWM de 50 Hz en servos estándar.
    """
    return 2.5 + (angle / 180.0) * 10

# Inicializa el PWM en el pin definido para el servo y lo posiciona en el punto inicial (90º)
# @parametros: ninguno
# Pre-condiciones: GPIO ya inicializado (setmode y setup)
# Post-condiciones: servo listo para ser usado
def inicializar_servo():
    """
    Configura el pin y arranca el PWM del servo en 0°.
    Debe llamarse *tras* GPIO.setmode(...) en el main.
    Previene crear múltiples instancias de PWM.
    """
    global servo
    # Si ya existe un objeto PWM, detenelo primero
    if servo is not None:
        try:
            servo.stop()
        except Exception:
            pass

    GPIO.setup(SERVO_PIN, GPIO.OUT)
    servo = GPIO.PWM(SERVO_PIN, 50)  # Frecuencia: 50 Hz
    servo.start(angle_to_percent(90))
    time.sleep(0.3)
    servo.ChangeDutyCycle(0)

# Simula una pulsación: baja a 0º (presión), vuelve a 90º (reposo)
# @parametros: ninguno
# Pre-condiciones: servo inicializado
# Post-condiciones: el servo realiza el movimiento de "presionar"
def presionar_tecla():
    """
    Baja el servo a 45° y vuelve a 0° para simular una pulsación.
    """
    if servo is None:
        raise RuntimeError("El servo no está inicializado. Llamá a inicializar_servo() primero.")
    # Baja a 45°
    servo.ChangeDutyCycle(angle_to_percent(20))
    time.sleep(0.2)
    # Vuelve a 0°
    servo.ChangeDutyCycle(angle_to_percent(90))
    time.sleep(0.2)
    servo.ChangeDutyCycle(0)

# Libera el canal PWM del servo
# @parametros: ninguno
# Pre-condiciones: servo inicializado
# Post-condiciones: el PWM queda detenido y el recurso liberado
def cleanup():
    """
    Detiene el PWM del servo. Llamar antes de GPIO.cleanup().
    """
    global servo
    if servo is not None:
        servo.stop()
        servo = None