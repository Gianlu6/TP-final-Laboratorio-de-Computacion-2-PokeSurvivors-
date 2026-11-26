import math
import pygame
from sprites import *
from Clases_Abs import *
from constantes import *

#Base de ataques?
#Cola férrea, ataque normal para los de tierra (látigo de VS)
#Bola voltio: Protectil? Varita de fuego? El ataque sube en base a la velocidad

#Proyectiles?

#Enemigo. Ataques segun tipo (daño de contacto y proyectiles):
#Fuego y agua: proyectiles, fuego hace mas daño, agua lanza mas proyectiles
#Lucha, acero, roca: Daño por contacto, mínimo pero varios por segundo en lucha y acero hace mas daño pero el cooldown es mas largo
#Tierra: daño de contacto o area con terremotos

# ---------- PROYECTILES ----------
class Proyectiles(Entidad):
    def __init__(self, x, y, sprite, grupo,objetivo,velocidad):
        super().__init__(x, y, sprite, grupo)
        #Calculo del angulo apuntando al enemigo y cuanto tiene que moverse (SOH - CAH - TOA)
        self.velocidad = velocidad
        self.angulo = math.atan2(objetivo.y - y, objetivo.x - x)
        self.vx = math.cos(self.angulo) * self.velocidad
        self.vy = math.sin(self.angulo) * self.velocidad

        #Ajustar rotacion del sprite
        self.image = pygame.transform.rotate(self.image, -math.degrees(self.angulo)) #El rompepelotas de pygame quiere los grados en grados y el angulo se calculo en radianes pipipi
        self.rect = self.image.get_rect(center=(x, y))

    def moverse (self): #Recibe parámetros de cuanto hay que moverse
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)


#--------------------------------------Ataques---------------------------------------------
class Chispitas (Movimiento):
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga, rango, velocidad):
        super().__init__(x, y, sprite, grupo, ataque_base, tiempo_recarga, rango)
        self.velocidad = velocidad*5
        self.proyectiles = []
        self.tiempo_disparo = 0
        self.ataque_base *= 0.3
        self.sprite_original = self.image
        self.image = pygame.Surface((0,0)) #Dejamos el sprite Vacio
        
    #Pasado el tiempo de recarga, crea el proyectil 
    #Este proyectil tiene asignado un enemigo target: el que este mas cerca en el momento de la creacion
    #Durante el ciclo de atacar constante, fuera del tiempo de recarga o en el .update los proyectiles se moveran hacia su target
    #Los proyectiles mueren pasado un rango (rango, pj*1000)
    #Los proyectiles se mueves y si colicionan con un enemigo de la lista quitan vida y mueren
    def atacar(self, autor, objetivos):
        if len(objetivos)!=0:
            if pygame.time.get_ticks() - self.tiempo_disparo >= self.tiempo_recarga: #Creacion de proyectiles segun tiempo recarga
                dist_mas_cercana = self.rango
                victima = None
                for enemigo in objetivos:
                    if distancia_entre_puntos(autor.posicion(),enemigo.posicion()) < dist_mas_cercana:    #Calculo del enemigo mas cercano
                        dist_mas_cercana = distancia_entre_puntos(autor.posicion(),enemigo.posicion())
                        victima = enemigo
                #Disparo a enemigo
                if victima is not None:
                    self.proyectiles.append(Proyectiles(autor.x, autor.y,self.sprite_original,autor.grupo,victima,self.velocidad))
                    self.tiempo_disparo = pygame.time.get_ticks()
       
        #Movimiento constante de proyectiles
            if len(self.proyectiles)!=0:    
                for proyectil in self.proyectiles:
                    proyectil.moverse()
                    #Deteccion de colicion o limite de rango
                    if distancia_entre_puntos(proyectil.posicion(),autor.posicion()) > self.rango:  #Los proyectiles mueren pasado su rango
                        proyectil.estoy_vivo = False
                        proyectil.kill()        #Kill las saca del sprite group para que no se renderice mas
                        continue

                    for enemigo in objetivos:
                        if proyectil.estoy_vivo and proyectil.rect.colliderect(enemigo.rect):
                            enemigo.quitar_vida(self.ataque_base)
                            proyectil.estoy_vivo = False
                            proyectil.kill()
    def update(self):
        self.proyectiles[:] = [p for p in self.proyectiles if p.estoy_vivo]     
        #En la actualizacion borro los proyectiles que murieron de la lista de proyectiles activos
        #NOTA: Uso de slicing por la mutabilidad de la lista (asignar normalmente no reeplaza datos sino que apunta a misma direccion de memoria)

class Rayo (Movimiento):             #Impacto de rayos a enemigos random
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga, rango):
        super().__init__(x, y, sprite, grupo, ataque_base, tiempo_recarga, rango)
        self.ultimo_ataque = 0
        self.image = pygame.Surface((0,0)) #Dejamos el sprite Vacio
        self.rayo_image = sprite
        self.rango = 600        #Alcance de 700 pixeles o casi toda la pantalla (excluye afuera de ella)
        self.timepo_rayo = 0

    def atacar(self, autor, objetivos):
        self.t_ahora = pygame.time.get_ticks()
        victimas_en_rango = []             
        if self.t_ahora - self.ultimo_ataque >= self.tiempo_recarga and len(objetivos)!=0:
            for enemigo in objetivos:                           
                if distancia_entre_puntos((autor.x,autor.y),(enemigo.x,enemigo.y))<self.rango:
                    victimas_en_rango.append(enemigo)             #Lista intermedia de enemigos que cumplen con un rango o se ven en pantalla

                if len(victimas_en_rango)!=0:
                    victima = victimas_en_rango[random.randint(0,len(victimas_en_rango)-1)]
                    victima.quitar_vida(self.ataque_base)  #Dañar enemigo aleatorio
                    self.mostrar_rayo(autor.buscar_pos(victima))
                    self.ultimo_ataque = self.t_ahora
                    self.timepo_rayo = self.t_ahora
        

    def mostrar_rayo(self,pos):
        self.image = self.rayo_image           #Mostrar sprite de rayo
        self.rect = self.image.get_rect(midbottom=pos)

    def borrar_rayo (self):
        self.image = pygame.Surface((0,0)) #Dejamos el sprite Vacio
        self.rect = self.image.get_rect(center=(self.x,self.y))

    def update(self):
        if self.t_ahora - self.timepo_rayo >= 100:
            self.borrar_rayo()
            
class Placaje (Movimiento):     #Daño de contacto de personaje del tipo 'normal' para los que son inmunes al rayo
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga, rango):
        super().__init__(x, y, sprite, grupo, ataque_base, tiempo_recarga, rango)
        self.ataque_base = ataque_base*0.5

    def atacar(self, autor, objetivos):
        super().atacar(autor, objetivos)       
        for enemigo in objetivos:           
            if autor.rect.colliderect(enemigo.rect):
                        enemigo.quitar_vida(self.ataque_base)

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
