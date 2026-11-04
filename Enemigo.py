import math
from Clases_Abs import Entidad
import pygame
from constantes import *

class Enemigo(Entidad):
    def __init__(self, vida, ataque, defensa, x, y, sprite, velocidad=2, intervalo=1500):
        super().__init__(vida, ataque, defensa, x, y, sprite)
        self.velocidad = velocidad
        self.intervalo = intervalo
        self.ultimo_chequeo = 0
        self.objetivo = (x, y)    
        
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
        