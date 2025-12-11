#Tamaño por defecto del tablero
FILAS_TABLERO = 10
COLUMNAS_TABLERO = 10

# Barcos y sus esloras (nombre: eslora)
# 4 barcos de 1, 3 de 2, 2 de 3, 1 de 4
BARCOS = {
    "barco_1": 1,
    "barco_2": 1,
    "barco_3": 1,
    "barco_4": 1,
    "barco_5": 2,
    "barco_6": 2,
    "barco_7": 2,
    "barco_8": 3,
    "barco_9": 3,
    "barco_10": 4
}

# Estados de las casillas
AGUA = 0
BARCO = 1
IMPACTO = 2
FALLO = 3

# Símbolos visuales para mostrar el tablero
SIMBOLOS = {
    AGUA: "💧",
    BARCO: "🚢",
    IMPACTO: "💥",
    FALLO: "😞"
}