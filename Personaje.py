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
        
        self.rect = self.rect.inflate(-55, -55)
        self.rect.center = (x,y)

        #Instancia de los ataques
        self.inventario = [ElectroTela(self.x, self.y, electroTela_sprite, grupo, self.ataque,500,self.rango),
                         Placaje(self.x, self.y, pygame.Surface((0,0)), grupo, self.ataque,500,0),
                         Rayo(x,y,rayoATQ_sprite,grupo,self.ataque*0.2,500,1), 
                         Chispitas(self.x, self.y,rayito_sprite,self.grupo,self.ataque,500,600,self.velocidad)]


    def atacar(self, ene):
        for movimiento in self.inventario:
            movimiento.atacar(self,enemigos)

    def actualizar_posicion_armas(self):    #Refresca pocicion de ataques que siguen a personaje y se desfasan por separacion
        for movimiento in self.inventario:
            if type(movimiento) is ElectroTela:
                dx = (self.x + movimiento.offset_x) - movimiento.x
                dy = (self.y + movimiento.offset_y) - movimiento.y
                movimiento.moverse(dx, dy)

    def subir_stats(self,incrementador):
        #Ataque,def,velocidad,rango,recarga,vida_max
        #Tiempo_recarga vs invulnerabilidad
        #Rango modifica la colicion y la imagen
        #A pj y armas (las armas tienen modificadores en el ataque y velocidad base del personaje)
        pass