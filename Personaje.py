from Ataque import *
from Clases_Abs import Entidad
from Enemigo import *
from sprites import *

class Personaje(Entidad):
    def __init__(self, vida, ataque, defensa, x, y, image, grupo, rango):
        super().__init__(vida, ataque, defensa, x, y, image, grupo)
        self.__vida = vida
        self.rango = rango
        self.ataque = ataque
        self.grupo = grupo
        self.rect = self.rect.inflate(-50, -50)
        self.rect.center = (x,y)


        self.contador = 0 #PROYECTILES
        

    

    #Property es un decorador intergrado que convierte un metodo getter de un atributo privado
    #en un atributo de solo lectura (o un método sin paréntesis con el mismo nombre que el atributo privado)
    
    #El getter de vida se llama asi:
        #prota.vida 
    @property                   
    def vida(self):
        return self.__vida

    #El decorador .setter toma el nombre del atributo privado y cuando lo llamas 
    # para editarlo como un atributo normal, en realidad pasa por el método setter validador

    #El setter de vida se llama asi:
    # prota.vida = danio
    @vida.setter                                  
    def vida(self, danio):
        if danio >= self.__vida:
            self.__vida = 0
        else:
            self.__vida -= danio
        
    def atacar(self,ene):
        #Podria se una lista que recorra las instancias de ataques que usan de método común atacar
        self.contador+=1

        if self.contador < 30 or not ene:
            return None
        else:
            self.contador = 0
            pos_x,pos_y = self.buscar_pos(ene[0])
            return Proyectil(1,0,rayo_sprite,self.x, self.y, pos_x, pos_y, self.ataque, self.grupo)
    #el personaje recibe un diccionario con todos los enemigos presentes como claves y 
    #sus posiciones relativas al personaje como valores y quien tenga la menor de ellas
    #sera al que ataque.
    
    
        
