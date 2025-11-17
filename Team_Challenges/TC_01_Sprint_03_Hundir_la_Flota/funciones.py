def coloca_barco_plus(tablero, barco):
    # Nos devuelve el tablero si puede colocar el barco, si no devuelve False, y avise por pantalla
    tablero_temp = tablero.copy()
    num_max_filas = tablero.shape[0]
    num_max_columnas = tablero.shape[1]
    for pieza in barco:
        fila = pieza[0]
        columna = pieza[1]
        if fila < 0  or fila >= num_max_filas:
            print(f"No puedo poner la pieza {pieza} porque se sale del tablero")
            return False
        if columna < 0 or columna >= num_max_columnas:
            print(f"No puedo poner la pieza {pieza} porque se sale del tablero")
            return False
        if tablero[pieza] == "O" or tablero[pieza] == "X":
            print(f"No puedo poner la pieza {pieza} porque hay otro barco")
            return False
        
        tablero_temp[pieza] = "O"
    return tablero_temp


def crea_barco_aleatorio(tablero, eslora = 4, num_intentos = 100):
    num_max_filas = tablero.shape[0]
    num_max_columnas = tablero.shape[1]
    contador = 0
    while contador <= num_intentos:
        contador += 1
        barco = []
        pieza_inicio = (random.randint(0,num_max_filas-1), random.randint(0, num_max_columnas -1))
        print("Pieza original:", pieza_inicio)
        barco.append(pieza_inicio)
        orientacion = random.choice(["N","S","O","E"])
        print("Con orientacion", orientacion)
        fila = pieza_inicio[0]
        columna = pieza_inicio[1]
        for i in range(eslora - 1):
            if orientacion == "N":
                fila -= 1
            elif orientacion  == "S":
                fila += 1
            elif orientacion == "E":
                columna += 1
            elif orientacion == "O":
                columna -= 1
            pieza = (fila,columna)
            barco.append(pieza)
        
        tablero_temp = coloca_barco_plus(tablero, barco)
        if type(tablero_temp) == np.ndarray:
            return tablero_temp
        
        print("Tengo que intentar colocar otro barco, intento:", contador)
