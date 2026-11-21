from PokeAtaque import *
from Clases_Abs import Entidad

class Personaje(Entidad):
    def __init__(self, vida, ataque, defensa, x, y, image, grupo, rango, ataques):
        super().__init__(vida, ataque, defensa, x, y, image, grupo)
        self.vida_maxima = 100
        self.rango = rango
        self.ataques = ataque
        
    def atacar(self, posicion_enemigo, indice=0):
        return self.ataques[indice].lanzar(self, posicion_enemigo)
    
    #el personaje recibe un diccionario con todos los enemigos presentes como claves y 
    #sus posiciones relativas al personaje como valores y quien tenga la menor de ellas
    #sera al que ataque.
    
    
        
