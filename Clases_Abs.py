from abc import ABC, abstractmethod
from constantes import *

class Entidad(pygame.sprite.Sprite, ABC):
    def __init__(self, vida, ataque, defensa, x, y, sprite, grupo):    # x, y -> Coordenadas de posición
        super().__init__(grupo)         #Pygame
        self.__vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.x = x
        self.y = y
        self.estoy_vivo = True

        #Atributos específicos de la clase tipo pygame Sprite:
        self.image = sprite
        self.rect = self.image.get_rect (center=(x,y))


    def moverse (self, dx, dy): #Recibe parámetros de cuanto hay que moverse
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)
        
    @abstractmethod
    def atacar(self, vida_enemigo, defensa_enemigo):
        pass
   
    def buscar_pos(self, Ent_Enemiga):
        return (Ent_Enemiga.x, Ent_Enemiga.y)