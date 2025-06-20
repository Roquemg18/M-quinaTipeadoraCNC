import RPi.GPIO as GPIO
from motoresv3 import inicializar_motores, volver_al_origen, cleanup_motores , ir_y_presionar
from servomotor import inicializar_servo, cleanup as servo_cleanup


GPIO.setmode(GPIO.BCM)

# Este es el Script principal de prueba. Inicializa componentes, escribe un conjunto de
# letras, y vuelve al origen.
# @parametros: ninguno
# Pre-condiciones: GPIO disponible y teclado conectado correctamente
# Post-condiciones: Se escribe la palabra definida y se limpian los recursos
try:
    inicializar_motores()
    inicializar_servo()
    volver_al_origen()
    ir_y_presionar("H")
    ir_y_presionar("O")
    ir_y_presionar("L")
    ir_y_presionar("A")
    volver_al_origen()

finally:
    servo_cleanup()
    cleanup_motores()
    GPIO.cleanup()