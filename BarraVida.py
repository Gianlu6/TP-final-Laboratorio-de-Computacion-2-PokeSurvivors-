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



class NumeroDanio (pygame.sprite.Sprite):
    def __init__(self, pos, valor,grupo):
        super().__init__(grupo)
        self.image = FUENTE_DANIO.render(str(valor), True, AZUL)
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.velocidad = -1.5
        self.alfa = 255
        self.vel_degrade = 5

    def update(self):           #grupo_camara cuando se actualiza llama a esta funcion tambien
        self.pos.y += self.velocidad        #Hace una animacion fade-out del numero de daño
        self.rect.center = (round(self.pos.x),round(self.pos.y))

        self.alfa -= self.vel_degrade
        
        if self.alfa <=0:
            self.kill()
        else:
            self.image.set_alpha(int(self.alfa))