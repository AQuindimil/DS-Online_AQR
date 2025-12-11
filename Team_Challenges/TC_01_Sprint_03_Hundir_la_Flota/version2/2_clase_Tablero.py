import numpy as np
import random
from Variables import agua, barco, impacto, fallo, filas_tablero, columnas_tablero, simbolos

class Tablero:
    def __init__(self, filas_tablero, columnas_tablero):
        self.tablero_filas=filas_tablero
        self.tablero_columnas=columnas_tablero
        
        #Me genero una tupla de las dimensiones de la matriz 
        dimensiones=(self.tablero_filas, self.tablero_columnas)
        
        #Creamos matriz con las dimensiones. Esta matriz sirve para ver su propio tablero con barcosa e impactos recibidos
        self.tablero=np.full(dimensiones, agua)
        #Creamos matriz de disparos, sirve para ver los disparo que has hecho al enemigo sin ver los barcos del rival
        self.disparos=np.full(dimensiones, agua)
        
        print(self.tablero)#Prueba para ver el tablero
        print(dimensiones)#prueba para ver dimensiones
    
    #creo metodo de disparo 
       
    