# servomotor.py
import RPi.GPIO as GPIO
import time

# Pin del servo en modo BCM
SERVO_PIN = 26
servo = None

def angle_to_percent(angle):
    """
    Convierte un ángulo (0–180°) a porcentaje de duty cycle
    para un PWM de 50 Hz en servos estándar.
    """
    return 2.5 + (angle / 180.0) * 10

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

def cleanup():
    """
    Detiene el PWM del servo. Llamar antes de GPIO.cleanup().
    """
    global servo
    if servo is not None:
        servo.stop()
        servo = None