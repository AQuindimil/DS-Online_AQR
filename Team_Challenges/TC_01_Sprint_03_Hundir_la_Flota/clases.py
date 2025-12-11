import random
import numpy as np
from Variables import (
    FILAS_TABLERO, COLUMNAS_TABLERO,
    BARCOS,
    AGUA, BARCO, IMPACTO, FALLO,
    SIMBOLOS
)

class Barco:
    """
    Representa un barco con nombre, eslora y coordenadas ocupadas.
    Lleva la cuenta de impactos y permite saber si está hundido.
    """
    def __init__(self, nombre, eslora):
        self.nombre = nombre
        self.eslora = eslora
        self.coordenadas = []
        self.impactos = 0

    def registrar_impacto(self):
        self.impactos += 1

    def esta_hundido(self):
        return self.impactos >= self.eslora


class Tablero:
    """
    Gestiona el tablero de un jugador:
    *tablero: array con barcos e impactos recibidos (lo que ve el propietario).
    *disparos: array con los impactos/fallos realizados al oponente (sin barcos).
    Permite colocar barcos, disparar y mostrar el tablero.
    """
    def __init__(self, filas=FILAS_TABLERO, columnas=COLUMNAS_TABLERO):
        self.tablero_filas = filas
        self.tablero_columnas = columnas

        dimensiones = (self.tablero_filas, self.tablero_columnas)
        self.tablero = np.full(dimensiones, AGUA, dtype=np.int8)
        self.disparos = np.full(dimensiones, AGUA, dtype=np.int8)

    def dentro_de_tablero(self, x, y):
        return 0 <= x < self.tablero_filas and 0 <= y < self.tablero_columnas

    def hay_espacio_libre(self, coords):
        return all(self.tablero[x, y] == AGUA for x, y in coords)

    def colocar_barco(self, barco, coordenadas):
        for x, y in coordenadas:
            self.tablero[x, y] = BARCO
        barco.coordenadas = coordenadas

    def generar_coordenadas_validas(self, eslora):
        """
        Genera coordenadas válidas aleatorias para un barco de 'eslora',
        con orientación N/S/E/O, asegurando que esté dentro del tablero y sin solaparse.
        """
        orientaciones = ['N', 'S', 'E', 'O']
        intentos_max = 1000
        for _ in range(intentos_max):
            x = random.randint(0, self.tablero_filas - 1)
            y = random.randint(0, self.tablero_columnas - 1)
            orientacion = random.choice(orientaciones)
            coords = []

            for i in range(eslora):
                nx, ny = x, y
                if orientacion == 'N':
                    nx -= i# se desplaza hacia arriba en el tablero
                elif orientacion == 'S':
                    nx += i# se desplaza hacia abajo en el tablero
                elif orientacion == 'E':
                    ny += i# se desplaza hacia la derecha en el tablero
                elif orientacion == 'O':
                    ny -= i# se desplaza hacia la izquierda en el tablero

                if not self.dentro_de_tablero(nx, ny):
                    coords = []
                    break
                coords.append((nx, ny))

            if coords and len(coords) == eslora and self.hay_espacio_libre(coords):
                return coords

        raise RuntimeError("No se pudieron generar coordenadas válidas para un barco.")

    def disparar(self, x, y):
        """
        Disparo que recibe este tablero.
        Devuelve True si se ha impactado un barco; False si es agua.
        Marca IMPACTO o FALLO en self.tablero.
        """
        if not self.dentro_de_tablero(x, y):
            return False

        if self.tablero[x, y] == BARCO:
            self.tablero[x, y] = IMPACTO
            return True
        elif self.tablero[x, y] == AGUA:
            self.tablero[x, y] = FALLO
            return False
        else:
            # Ya se había disparado aquí (IMPACTO o FALLO). Lo tratamos como fallo para flujo de juego.
            return False

    def registrar_disparo(self, x, y, acierto):
        """
        Registra en el tablero de disparos propio el resultado de un disparo
        realizado contra el oponente.
        """
        if not self.dentro_de_tablero(x, y):
            return
        self.disparos[x, y] = IMPACTO if acierto else FALLO

    def mostrar(self, mostrar_barcos=True):
        """
        Muestra el tablero:
        - mostrar_barcos=True: se imprime el tablero propio con barcos e impactos.
        - mostrar_barcos=False: se imprime el tablero de disparos efectuados al rival.
        """
        matriz = self.tablero if mostrar_barcos else self.disparos
        for fila in matriz:
            print(" ".join(SIMBOLOS[celda] for celda in fila))


class Jugador:
    """
    Representa a un jugador con su tablero y barcos.
    Gestiona inicialización de barcos, recibir disparos y disparar al oponente.
    """
    def __init__(self, nombre, filas=FILAS_TABLERO, columnas=COLUMNAS_TABLERO):
        self.nombre = nombre
        self.tablero = Tablero(filas, columnas)
        self.barcos = []
        self.vidas = 0  # Total de casillas de barco
        self.objetivos_disponibles = {(x, y) for x in range(filas) for y in range(columnas)}  # Para la máquina

    def inicializar_barcos(self):
        for nombre, eslora in BARCOS.items():
            barco = Barco(nombre, eslora)
            coords = self.tablero.generar_coordenadas_validas(eslora)
            self.tablero.colocar_barco(barco, coords)
            self.barcos.append(barco)
            self.vidas += eslora

    def recibir_disparo(self, x, y):
        acierto = self.tablero.disparar(x, y)
        if acierto:
            for barco in self.barcos:
                if (x, y) in barco.coordenadas:
                    barco.registrar_impacto()
                    if barco.esta_hundido():
                        print(f"¡{self.nombre} ha perdido el {barco.nombre}!")
                    break
            self.vidas -= 1
        return acierto

    def disparar_a(self, oponente, x, y):
        acierto = oponente.recibir_disparo(x, y)
        self.tablero.registrar_disparo(x, y, acierto)
        # Elimina este objetivo de los disponibles para evitar repetir disparos
        if (x, y) in self.objetivos_disponibles:
            self.objetivos_disponibles.remove((x, y))
        return acierto


class Juego:
    """
    Controla el flujo del juego:
    - Bienvenida e instrucciones.
    - Inicialización de jugadores y sus barcos.
    - Bucle de turnos hasta victoria/derrota.
    """
    def __init__(self, filas=FILAS_TABLERO, columnas=COLUMNAS_TABLERO):
        self.filas = filas
        self.columnas = columnas
        self.id_jugador = input("Por favor introduce tu nombre:")
        self.jugador = Jugador(self.id_jugador, filas, columnas)
        self.maquina = Jugador("Máquina", filas, columnas)

    def iniciar(self):
        print(f"¡Bienvenido a Batalla Naval {self.id_jugador}!")
        print("Reglas: Dispara a coordenadas (X, Y). Si aciertas, repites turno. El tablero es de 10x10.")
        print("Símbolos: 💧 Agua | 🚢 Barco | 💥 Impacto | 😞 Fallo\n")

        # Inicializar barcos una sola vez
        self.jugador.inicializar_barcos()
        self.maquina.inicializar_barcos()

        turno = "jugador"

        while True:
            # Vista del turno
            print("\nTu tablero (barcos e impactos recibidos):")
            self.jugador.tablero.mostrar(mostrar_barcos=True)
            print("\nTus disparos al enemigo (sin barcos):")
            self.jugador.tablero.mostrar(mostrar_barcos=False)

            if turno == "jugador":
                x, y = self.pedir_coordenadas_usuario()
                acierto = self.jugador.disparar_a(self.maquina, x, y)
                if self.maquina.vidas == 0:
                    print("\n¡Has ganado! Todos los barcos enemigos han sido hundidos.")
                    break
                turno = "jugador" if acierto else "maquina"
            else:
                # Máquina escoge un objetivo aleatorio no repetido
                x, y = self.elegir_objetivo_maquina()
                print(f"\nLa máquina dispara a ({x}, {y})")
                acierto = self.maquina.disparar_a(self.jugador, x, y)
                if self.jugador.vidas == 0:
                    print("\n¡Has perdido! Todos tus barcos han sido hundidos.")
                    break
                turno = "maquina" if acierto else "jugador"

    def pedir_coordenadas_usuario(self):
        from funciones import pedir_coordenadas
        return pedir_coordenadas(self.filas, self.columnas)

    def elegir_objetivo_maquina(self):
        """
        Elige un objetivo aleatorio de los disponibles (no dispara dos veces al mismo sitio).
        """
        if not self.maquina.objetivos_disponibles:
            # Fallback: debería no ocurrir, pero por seguridad
            return random.randint(0, self.filas - 1), random.randint(0, self.columnas - 1)
        return random.choice(tuple(self.maquina.objetivos_disponibles))