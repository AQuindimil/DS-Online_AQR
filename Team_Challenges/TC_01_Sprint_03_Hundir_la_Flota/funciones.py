def pedir_coordenadas(filas, columnas):
    """
    Pide coordenadas X, Y al usuario y valida que estén dentro del tablero.
    Devuelve una tupla (x, y).
    """
    while True:
        try:
            x = int(input(f"Introduce coordenada X (0-{filas - 1}): "))
            y = int(input(f"Introduce coordenada Y (0-{columnas - 1}): "))
            if 0 <= x < filas and 0 <= y < columnas:
                return x, y
            else:
                print("Coordenadas fuera de rango.")
        except ValueError:
            print("Entrada inválida. Usa números enteros.")