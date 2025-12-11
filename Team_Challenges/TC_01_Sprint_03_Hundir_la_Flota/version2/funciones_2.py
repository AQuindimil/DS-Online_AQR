def pedir_coordenadas(filas, columnas):
    """
    Pide coordenadas X, Y al usuario y valida que estén dentro del tablero.
    Devuelve una tupla (x, y).
    """
    while True:
        entrada_x = input(f"Introduce coordenada X (0-{filas - 1}): ")
        if entrada_x.lower() == "salir":
            print("Has salido del juego. Hasta pronto👋🙂") 
            exit() 

        entrada_y = input(f"Introduce coordenada Y (0-{columnas - 1}): ")
        if entrada_y.lower() == "salir":
            print("Has salido del juego. Hasta pronto👋🙂")   # 👉 imprime directamente
            exit()    


        try:
            x = int(entrada_x) #simplificaod cogiendo lo de arriba
            y = int(entrada_y)
            if 0 <= x < filas and 0 <= y < columnas:
                return x, y
            else:
                print("Coordenadas fuera de rango.")
        except ValueError:
            print("Entrada inválida. Usa números enteros.")