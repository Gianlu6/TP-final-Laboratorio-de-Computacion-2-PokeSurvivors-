from Ataque import *
from Clases_Abs import SerVivo
from Enemigo import *
from sprites import *

class Personaje(SerVivo):
    def __init__(self, vida_max, ataque, defensa, tipo, x, y, image, grupo, rango,velocidad):
        super().__init__(vida_max, ataque, defensa, tipo, x, y, image, grupo,velocidad)
        self.vida = vida_max        #Esto fue privatizado y convertido con @property en la clase SerVivo
        self.rango = rango
        self.grupo = grupo
        self.rect = self.rect.inflate(-50, -50)
        self.rect.center = (x,y)

        self.inventario = [ElectroTela(self.x, self.y, electroTela_sprite, grupo, self.ataque,0.5,self.rango)]

        self.contador = 0 #PROYECTILES



        
    # def atacar(self,ene):    
    #     self.contador+=1

    #     if self.contador < 30 or not ene:
    #         return None
    #     else:
    #         self.contador = 0
    #         pos_x,pos_y = self.buscar_pos(ene[0])
    #         return Proyectil(rayo_sprite,self.x, self.y, pos_x, pos_y, self.grupo,1000)
    #el personaje recibe un diccionario con todos los enemigos presentes como claves y 
    #sus posiciones relativas al personaje como valores y quien tenga la menor de ellas
    #sera al que ataque.
    def atacar(self, ene):
        for movimiento in self.inventario:
            movimiento.atacar(self,enemigos)

    def actualizar_posicion_armas(self):    #Refresca pocicion de ataques que siguen a personaje y se desfasan por separacion
        for movimiento in self.inventario:
            if type(movimiento) is ElectroTela:
                dx = (self.x + movimiento.offset_x) - movimiento.x
                dy = (self.y + movimiento.offset_y) - movimiento.y
                movimiento.moverse(dx, dy)