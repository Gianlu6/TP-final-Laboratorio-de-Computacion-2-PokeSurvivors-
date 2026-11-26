import pygame
from abc import ABC, abstractmethod
from constantes import *
from BarraVida import *


class Entidad(pygame.sprite.Sprite, ABC):
    def __init__(self,x,y,sprite, grupo):  #z es un atributo de prioridad de renderizado, teniendo Los seres vivos mas prioritdad que las armas
        super().__init__(grupo)
        self.x = x
        self.y = y
        #Atributos específicos de la clase tipo pygame Sprite:
        self.image = sprite
        self.rect = self.image.get_rect (center=(x,y))
        self.z = 1
        self.estoy_vivo = True

    def moverse (self, dx, dy): #Recibe parámetros de cuanto hay que moverse
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)

    #Getter de posicion
    def posicion(self):
        return (self.x,self.y)
    

class SerVivo(Entidad):
    def __init__(self, vida_max, ataque, defensa, tipo, x, y, sprite, grupo,velocidad):    # x, y -> Coordenadas de posición
            super().__init__(x,y,sprite,grupo)         
            self.vida_max = vida_max
            self.__vida = vida_max 
            self.ataque = ataque
            self.defensa = defensa
            self.__tipo = tipo
            self.grupo = grupo
            
            self.velocidad = velocidad
            self.image_original = self.image
            self.tiempo_danio = 0               # -> Tiempo que pasó desde que se hizo daño (MILISEGUNDOS)
            self.invulnerabilidad = 250           # -> Tiempo el cual no deberia recibir daño aunque se acierte el ataque (MILISEGUNDOS)

    #Property es un decorador intergrado que convierte un metodo getter de un atributo privado
    #en un atributo de solo lectura (o un método sin paréntesis con el mismo nombre que el atributo privado)
        
    #El getter de vida se llama asi:
    #prota.vida 
    @property                   
    def vida(self):
        return self.__vida

    #El decorador .setter toma el nombre del atributo privado y cuando lo llamas 
    # para editarlo como un atributo normal, en realidad pasa por el método setter validador

    #El setter de vida se llama asi:
    # prota.vida = valor          
    @vida.setter                  # <-- Setter tanto de curacion como de danio                
    def vida(self, valor):
        if valor >= 0 and valor <= self.vida_max:
            self.__vida = valor


    def quitar_vida(self, danio):
        if pygame.time.get_ticks() - self.tiempo_danio >= self.invulnerabilidad:
            if danio >= self.vida:
                self.vida = 0
                self.estoy_vivo = False
                self.kill()
            else:
                self.vida -= danio
                self.recibir_danio()

            #Aparicion de texto de danio
            pos_texto_danio = (self.rect.centerx, self.rect.top - 15)
            numerin=NumeroDanio(pos_texto_danio,danio, self.grupo)

    def curar_vida(self,curacion):
        if curacion+self.vida >= self.vida_max:
            self.vida = self.vida_max
        else:
            self.vida+=curacion

    def recibir_danio(self):                                    #Metodo que pone en rojo el sprite cuando recibe danio
        mascara = pygame.mask.from_surface(self.image)
        self.image = mascara.to_surface(setcolor=ROJO, unsetcolor=(0, 0, 0, 0))
        self.tiempo_danio = pygame.time.get_ticks()
        

    def update(self):                                                               #Metodo que se llama en grupo_camara en el bucle para actualizar sprites. 
        # Pasados ciertos segundos vuelve la imagen de rojo daño a la original
        if pygame.time.get_ticks() - self.tiempo_danio >= self.invulnerabilidad:
            self.image = self.image_original
            self.tiempo_danio = 0


    @property       #Tipo solo puede leerse
    def tipo(self):
        return self.__tipo


        
        
    @abstractmethod             
    def atacar(self, vida_enemigo, defensa_enemigo):
        pass
    
    def buscar_pos(self, Ent_Enemiga):              #Obtiene pocicion del enemigo
        return (Ent_Enemiga.x, Ent_Enemiga.y)

    

#Entidad -> Movimiento/ataque/arma -> Impactrueno
class Movimiento(Entidad):
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga,rango):
        super().__init__(x, y, sprite, grupo)
        self.ataque_base = ataque_base
        self.tiempo_recarga = tiempo_recarga
        self.offset_x = 0       #Por defecto en 0 pero si hay un Movimiento/Ataque que siga al personaje, se desplaza para que no tape al personaje
        self.offset_y = 0
        self.z = 0
        self.rango = rango

    @abstractmethod                     #Cada ataque ES distinto 
    def atacar(self,autor,objetivos):
        pass