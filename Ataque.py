import math
import pygame
from sprites import *
from Clases_Abs import *
from constantes import *

# ---------- PROYECTILES ----------
class Proyectil(Entidad):
    def __init__(self, image, x, y, objetivo_x, objetivo_y,  grupo, rango, velocidad=7):
        super().__init__(x, y, image, grupo) 

        #Calculo del angulo apuntando al enemigo (SOH - CAH - TOA)
        angulo = math.atan2(objetivo_y - y, objetivo_x - x)
        self.vx = math.cos(angulo) * velocidad
        self.vy = math.sin(angulo) * velocidad
        
        self.ataque = 100
        self.rango = rango
        self.image = pygame.Surface((12, 12))
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect(center=(x, y))
        self.estoy_vivo = True

    def avanzar(self):
        self.moverse(self.vx, self.vy)
        #if self.x < 0 or self.y < 0:
        #    self.estoy_vivo = False


    def atacar(self, vida_enemigo, defensa_enemigo):
        danio = max(1, self.ataque - defensa_enemigo)
        self.estoy_vivo = False
        return vida_enemigo - danio

    def moverse (self, dx, dy): #Recibe parámetros de cuanto hay que moverse
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)
