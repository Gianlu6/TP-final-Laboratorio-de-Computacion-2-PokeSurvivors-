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
#Rayo: Tiene mas daño que impactrueno
#Impactrueno: rayos caen aleatoreamente a los enemigos (anillo de relámpago de VS)
#Cola férrea, ataque normal para los de tierra (látigo de VS)
#Placaje: Ataque normal, daño de contacto
#Placaje eléctrico: Ataque eléctrico, daño de contacto (mas daño que rayo, deja estela de daño?)
#Electro tela/red: escudo electrico (ajo VS)
#Bola voltio: Protectil? Varita de fuego? El ataque sube en base a la velocidad
#Mega-punch, headbutt: Normales
#Volt Switch: Eléctrico. Pega y cambia, poco daño
#Proyectiles?

#Modificadores pasivos para evolucion

#Enemigo. Ataques segun tipo (daño de contacto y proyectiles):
#Fuego y agua: proyectiles, fuego hace mas daño, agua lanza mas proyectiles
#Lucha, acero, roca: Daño por contacto, mínimo pero varios por segundo en lucha y acero hace mas daño pero el cooldown es mas largo
#Tierra: daño de contacto o area con terremotos

#atacar revisa el cooldown, 
# recibe stats del usuario (atq,def,tipo) 
# y de su o sus target(lista enemigos)

class Impactrueno (Movimiento):
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga):
        super().__init__(x, y, sprite, grupo, ataque_base, tiempo_recarga)

    def atacar(self):
        pass

class Placaje (Movimiento):     #Daño de contacto de personaje
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga):
        super().__init__(x, y, sprite, grupo, ataque_base, tiempo_recarga)

    def atacar(self):
        pass

class ElectroTela (Movimiento):     
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga,rango):
        super().__init__(x, y, sprite, grupo, ataque_base, tiempo_recarga,rango)
        #self.rect = self.rect.inflate(50*self.rango, 50*self.rango)
        #self.rect.center = (x,y)
        self.image = pygame.transform.scale_by(self.image,self.rango)
        self.rect = self.image.get_rect(center=(x, y))
        
        self.ultimo_ataque = 0
    
    def atacar(self,autor,objetivos):
        self.t_ahora = pygame.time.get_ticks()
        if self.t_ahora - self.ultimo_ataque > self.tiempo_recarga:
            for enemigo in objetivos:
                if self.rect.colliderect(enemigo.rect):
                    enemigo.quitar_vida(0.3)
            self.ultimo_ataque = self.t_ahora
