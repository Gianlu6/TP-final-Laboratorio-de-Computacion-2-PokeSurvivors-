import pygame
import random
from constantes import *


class MundoSprite(pygame.sprite.Sprite):                              #Clase que genera elementos en el mundo
    def __init__(self, x, y, grupo):
        super().__init__(grupo)
        #self.x = x
        #self.y = y
        self.tamanio = 40

        #Atributos obligatorios para el pygame.sprite.group
        self.image = pygame.Surface((self.tamanio, self.tamanio))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect(topleft=(x,y))

   
    def dibujar_Sprite(self, pantalla):         #Método para dibujarlos como un rectanngulo azul
        pygame.draw.rect(pantalla, AZUL, 
                         (self.x, self.y, self.tamanio, self.tamanio))


class Mundo:                                #Clase mundo (en desuso)
    def __init__(self, ancho, alto,grupo):
        self.grupo = grupo
        self.ancho = ancho
        self.alto = alto
        self.elemento_fondo = [MundoSprite(random.randint(0,ancho-40), 
                                        random.randint(0,alto-40),self.grupo) for i in range (10)]
        #Exprecion generadora de 10 elementos Sprites en ubicacion random dentro del rango de la pantalla
        #Lista de clases mundoSprite con ubicaciones random dentro de el límite de la pantalla
    
    def dibujar_mundo (self, pantalla):                 
        pantalla.fill(VERDE)                     # Dibujar el mundo (color de fondo de relleno)
        for elemento in self.elemento_fondo:                # Cada elemento en la lista generada, es una instancia de clase con el método dibujar_Sprite 
            elemento.dibujar_Sprite(pantalla)               # Llamo al método de cada instancia de clase


class GrupoCamara (pygame.sprite.Group):        #Esta clase agrupa los sprites para redubijado masivo cuando se mueve la camara
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #Offset de camara
        self.offset = pygame.math.Vector2()
        self.mitad_ancho = self.display_surface.get_size()[0] //2
        self.mitad_alto = self.display_surface.get_size()[1] //2


    def camara_centrada(self,target):                                              #Método que aplica una transformacion inversa al mundo en base a un target: el personaje
        self.offset.x = target.rect.centerx - self.mitad_ancho
        self.offset.y = target.rect.centery - self.mitad_alto

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):         #El sorted + lambda se usa ordenar y dibujar los sprites en linea del mas alto en "y" al mas bajo (profundidad de atras hacia adelante)
            off_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, off_pos)