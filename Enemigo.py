import math
from Clases_Abs import Entidad
import pygame
from constantes import *
from PokeSurv import malo_sprite

class Enemigo(Entidad):
    cantidad = 0
    
    def __init__(self, vida, daño, defensa, x, y, sprite, velocidad=2, intervalo=1500):
        super().__init__(vida, daño, defensa, x, y, sprite)
        self.velocidad = velocidad
        self.intervalo = intervalo
        self.ultimo_chequeo = 0
        self.objetivo = (x, y)    
        self.cantidad += 1
        
    def atacar():
        pass
        
    def avanzar(self, Personaje):
        ahora = pygame.time.get_ticks() #devuelve cuantos segundos pasaron desde pygame.init()
        
        #cada intervalo actualiza el objetivo
        if ahora - self.ultimo_chequeo >= self.intervalo:
            self.objetivo = self.buscar_pos(Personaje)
            self.ultimo_chequeo = ahora 
            
        #se mueve hacia el obj
        dx = self.objetivo[0] - self.x 
        dy = self.objetivo[1] - self.y
        distancia = math.hypot(dx, dy)
        
        #chequea si la distancia es mayor a la velocidad para ir asi no hay mov raros
        if distancia > self.velocidad:
            self.moverse(dx / distancia * self.velocidad, dy / distancia * self.velocidad)

enemigos = []

def generador_enemigos():
    ahora = pygame.time.get_ticks()
    ultimo_chequeo = 0
    
    if len(enemigos) < 7:
        if ahora - ultimo_chequeo >= 2000:
            ultimo_chequeo = ahora 
            yield Enemigo(100, 50, 50, WIDTH//4, HEIGHT//4, malo_sprite)
 
def spawneo_enemigos():
              