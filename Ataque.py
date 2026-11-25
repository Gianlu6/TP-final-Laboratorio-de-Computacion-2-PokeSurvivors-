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
        return danio

    def moverse (self, dx, dy): #Recibe parámetros de cuanto hay que moverse
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)

#Base de ataques?
#Rayo: Rayos caen aleatoreamente a los enemigos (anillo de relámpago de VS)
#Cola férrea, ataque normal para los de tierra (látigo de VS)
#Placaje: Ataque normal, daño de contacto
#Bola voltio: Protectil? Varita de fuego? El ataque sube en base a la velocidad

#Proyectiles?

#Enemigo. Ataques segun tipo (daño de contacto y proyectiles):
#Fuego y agua: proyectiles, fuego hace mas daño, agua lanza mas proyectiles
#Lucha, acero, roca: Daño por contacto, mínimo pero varios por segundo en lucha y acero hace mas daño pero el cooldown es mas largo
#Tierra: daño de contacto o area con terremotos

#atacar revisa el cooldown, 
# recibe stats del usuario (atq,def,tipo) 
# y de su o sus target(lista enemigos)

class Rayo (Movimiento):             #Impacto de rayos a enemigos random
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga, rango):
        super().__init__(x, y, sprite, grupo, ataque_base, tiempo_recarga, rango)
        self.ultimo_ataque = 0
        self.image = pygame.Surface((0,0)) #Dejamos el sprite Vacio
        self.rayo_image = sprite

    def atacar(self, autor, objetivos):
        self.t_ahora = pygame.time.get_ticks()
        if self.t_ahora - self.ultimo_ataque >= self.tiempo_recarga and len(objetivos)!=0:
            victima = objetivos[random.randint(0,len(objetivos)-1)]
            victima.quitar_vida(self.ataque_base) #Dañar enemigo aleatorio
            self.image = self.rayo_image
            self.rect = self.image.get_rect(midbottom=autor.buscar_pos(victima))
            self.ultimo_ataque = self.t_ahora
            
        #Mostrar sprite de rayo


class Placaje (Movimiento):     #Daño de contacto de personaje del tipo 'normal' para los que son inmunes al rayo
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga, rango):
        super().__init__(x, y, sprite, grupo, ataque_base, tiempo_recarga, rango)
        self.ataque_base = ataque_base*0.5

    def atacar(self, autor, objetivos):
        super().atacar(autor, objetivos)       
        for enemigo in objetivos:           
            if autor.rect.colliderect(enemigo.rect):
                        enemigo.quitar_vida(self.ataque_base)

class ColaFerrea(Movimiento):               #Daño normal con un poco mas de distancia
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga, rango):
        super().__init__(x, y, sprite, grupo, ataque_base, tiempo_recarga, rango)

    def atacar(self, autor, objetivos):
        super().atacar(autor, objetivos)
        pass

class ElectroTela (Movimiento):     #Area electrica que drena vida cada medio segundo. 
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga,rango):
        super().__init__(x, y, sprite, grupo, ataque_base, tiempo_recarga,rango)
        self.image = pygame.transform.scale_by(self.image,self.rango)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = self.rect.width //2.5 #Creacion de colicion circular
        self.ataque_base = ataque_base*0.3
        self.ultimo_ataque = 0
    
    def atacar(self,autor,objetivos):
        self.t_ahora = pygame.time.get_ticks()
        if self.t_ahora - self.ultimo_ataque > self.tiempo_recarga:
            for enemigo in objetivos:
                if pygame.sprite.collide_circle(self, enemigo):
                    enemigo.quitar_vida(self.ataque_base)
            self.ultimo_ataque = self.t_ahora
