# El Mapa de teclas (son posiciones relativas desde el origen)
# Diccionario "teclas" que asocia cada tecla a una coordenada (X, Y) que representa su 
# ubicación
# relativa en el teclado
# Pre-condiciones: el origen (0,0) es la tecla Ctrl inferior izquierda
# Post-condiciones: permite utilizar nombres de teclas para realizar movimientos CNC 
# precisos


# Mapa de teclas (posiciones relativas desde el origen)
teclas = teclas = {
    # Fila 0 — inferior
    "Ctrl": (0, 0), "Fn": (0, 1.7), "Win": (0, 2.7), "Alt": (0, 3.7),
    " ": (0, 6.7),  # Espacio (puede ocupar más columnas)
    "AltGr": (0, 9.7), "Menu": (0, 10.7), "CtrlDer": (0, 11.7),

    # Fila 1 — Z, X, C...
    "Shift": (1, 1), "Z": (1, 3.2), "X": (1, 4.2), "C": (1, 4.2),
    "V": (1, 6.2), "B": (1, 7.2), "N": (1, 8.2), "M": (1, 9.2),
    ",": (1, 10.2), ".": (1, 11.2), "/": (1, 12.2), "ShiftDer": (1, 13.2),

    # Fila 2 — A, S, D...
    "Caps": (2, 0), "A": (2, 2), "S": (2, 3.2), "D": (2, 4.2),
    "F": (2, 5.2), "G": (2, 6.2), "H": (2, 7), "J": (2, 8.2),
    "K": (2, 9.2), "L": (2, 10), ";": (2, 11.2), "'": (2, 12.2), "Enter": (2, 13.2),

    # Fila 3 — Q, W, E...
    "Tab": (3, 0), "Q": (3, 1.7), "W": (3, 0.7), "E": (3, 3.7),
    "R": (3, 4.7), "T": (3, 5.7), "Y": (3, 6.7), "U": (3, 7.7),
    "I": (3, 8.7), "O": (3, 9), "P": (3, 10.7), "[": (3, 11.7), "]": (3, 12.7), "\\": (3, 13.7),

    # Fila 4 — números
    "`": (4, 0), "1": (4, 1), "2": (4, 2), "3": (4, 3),
    "4": (4, 4), "5": (4, 5), "6": (4, 6), "7": (4, 7),
    "8": (4, 8), "9": (4, 9), "0": (4, 10), "?": (4, 11), "¿": (4, 12), "Backspace": (4, 13),
}