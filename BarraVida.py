import pygame
from constantes import *

class BarraVida():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h 
        self.max_hp = max_hp
        
    def dibujar(self, superficie, hp):
        ratio = hp / self.max_hp
        pygame.draw.rect(superficie, ROJO, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(superficie, VERDE, (self.x, self.y, self.w * ratio, self.h))