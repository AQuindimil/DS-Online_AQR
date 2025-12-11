'''Este es el archivo prinicpal el cual tienes que ejecutar en bash inciar el juego'''
from clases import Juego
# Lo primero que hago es importar la clase juego que tenemos en el archivo clases 

'''__name__ es una variable especial de python y toma el valor de __main__ cuando lo ejecutas pero cuando 
lo importas toma el valor del modulo '''

if __name__ == "__main__":
    #Aqui llamo al contructor de clase init
    juego = Juego()
    #Aqui lo que hago es usar el objeto juego para llamar a su funcion o mejor dicho metodo que estamos en clase inciar
    juego.iniciar()