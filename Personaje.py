from PokeAtaque import *
from Clases_Abs import Entidad

class Personaje(Entidad):
    def __init__(self, vida, ataque, defensa, x, y, image, grupo, rango, ataques):
        super().__init__(vida, ataque, defensa, x, y, image, grupo)
        self.__vida = vida
        self.rango = rango
        self.ataques = ataque

    #El getter de vida se llama asi:
    #prota.vida
    @property
    def vida(self):
        return self.__vida

    #El setter de vida se llama asi:
    # prota.vida = danio
    @vida.setter                     
    def vida(self, danio):
        if danio >= self.__vida:
            self.__vida = 0
        else:
            self.__vida -= danio
        
    def atacar(self, posicion_enemigo, indice=0):
        return self.ataques[indice].lanzar(self, posicion_enemigo)
    
    #el personaje recibe un diccionario con todos los enemigos presentes como claves y 
    #sus posiciones relativas al personaje como valores y quien tenga la menor de ellas
    #sera al que ataque.
    
    
        
