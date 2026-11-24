from Ataque import *
from Clases_Abs import SerVivo
from Enemigo import *
from sprites import *

class Personaje(SerVivo):
    def __init__(self, vida_max, ataque, defensa, x, y, image, grupo, rango):
        super().__init__(vida_max, ataque, defensa, x, y, image, grupo)
        self.rango = rango
        self.grupo = grupo
        self.rect = self.rect.inflate(-50, -50)
        self.rect.center = (x,y)


        self.contador = 0 #PROYECTILES
        

    


        
    def atacar(self,ene):
        #Podria se una lista que recorra las instancias de ataques que usan de método común atacar
        
        
        
        
        pass
        
        
        
        
        # self.contador+=1

        # if self.contador < 30 or not ene:
        #     return None
        # else:
        #     self.contador = 0
        #     pos_x,pos_y = self.buscar_pos(ene[0])
        #     return Proyectil(rayo_sprite,self.x, self.y, pos_x, pos_y, self.grupo,1000)
    #el personaje recibe un diccionario con todos los enemigos presentes como claves y 
    #sus posiciones relativas al personaje como valores y quien tenga la menor de ellas
    #sera al que ataque.
    
    
        
