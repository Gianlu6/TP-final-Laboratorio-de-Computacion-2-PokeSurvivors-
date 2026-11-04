from abc import ABC, abstractmethod
from constantes import *

class Entidad(ABC):
    def __init__(self, vida, ataque, defensa, x, y, sprite):    # x, y -> Coordenadas de posición
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.x = x
        self.y = y
        self.sprite = sprite
        self.rect = self.sprite.get_rect(center=(x, y))
        self.estoy_vivo = True

    def dibujar(self):                     
       VENTANA.blit(self.sprite, (self.x, self.y))

    def moverse (self, dx, dy): #Recibe parámetros de cuanto hay que moverse
        self.x += dx
        self.y += dy
        
    @abstractmethod
    def atacar(self, vida_enemigo, defensa_enemigo):
        pass
   
    def buscar_pos(self, Ent_Enemiga):
        return (Ent_Enemiga.x, Ent_Enemiga.y)