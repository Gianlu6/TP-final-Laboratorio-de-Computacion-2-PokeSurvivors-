import math
from Clases_Abs import Entidad
import pygame
from constantes import *
from sprites import *
import random


class Enemigo(Entidad):
    def __init__(self, vida, ataque, defensa, x, y, image, grupo, velocidad=2):
        super().__init__(vida, ataque, defensa, x, y, image, grupo)
        self.velocidad = velocidad
        self.intervalo = 500
        self.ultimo_chequeo = 0
        self.objetivo = (x, y)    
        #self.cantidad += 1
        
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



ultimo_spawn = 0
enemigos = []

def spawneo_enemigos(personaje, grupo):
    global ultimo_spawn
    ahora = pygame.time.get_ticks()
    x = random.choice([0, WIDTH])
    y = random.randint(0, HEIGHT)   
    if len (enemigos) < 8 and ahora - ultimo_spawn >= 2000:
        ultimo_spawn = ahora
        enemigos.append(Enemigo(100, 50, 50, x, y, malo_sprite, grupo))

    for enemigo in enemigos:
        enemigo.avanzar(personaje)
        separar(enemigo,personaje)
    separar_todos(enemigos)