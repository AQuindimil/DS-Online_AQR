def pedir_coordenadas(filas, columnas, disparos_previos=None):
    """
    Pide coordenadas X, Y al usuario y valida que estén dentro del tablero.
    Devuelve una tupla (x, y).
    """
    if disparos_previos is None:
        disparos_previos = set()

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
            if not 0 <= x < filas and 0 <= y < columnas:
                print("Coordenadas fuera de rango.")
                continue
            if (x,y) in disparos_previos:
                print("Ya has disparado en esas coordenadas. Elige otras")
            return x,y
                
        except ValueError:
            print("Entrada inválida. Usa números enteros.")