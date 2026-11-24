import math
import pygame
from sprites import *
from Clases_Abs import *
from constantes import *

# ---------- PROYECTILES ----------
class Proyectil(Entidad):
    def __init__(self,vida, defensa, image, x, y, objetivo_x, objetivo_y, ataque,  grupo, velocidad=7):
        self.sprite = pygame.Surface((12, 12))
        self.sprite.fill(AMARILLO)
        super().__init__(vida, ataque, defensa, x, y, image, grupo)       
        self.vx = velocidad if objetivo_x > x else -velocidad
        self.vy = velocidad if objetivo_y > y else -velocidad

    def avanzar(self):
        self.moverse(self.vx, self.vy)
        if self.x < 0 or self.y < 0:
            self.estoy_vivo = False

    def atacar(self, vida_enemigo, defensa_enemigo):
        danio = max(1, self.ataque - defensa_enemigo)
        self.estoy_vivo = False
        return vida_enemigo - danio



class Pistola (Ataque):
    def __init__(self, ataque, velocidad_ataque, area, cantidad, grupo, x, y):
        super().__init__(ataque, velocidad_ataque, area, cantidad, grupo, x, y)

    def atacar():
        pass