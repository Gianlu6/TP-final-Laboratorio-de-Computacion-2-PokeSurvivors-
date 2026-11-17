import pygame
import random
from constantes import *


class MundoSprite:                              #Clase que genera elementos en el mundo
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tamanio = 40

    def dibujar_Sprite(self, pantalla):         #Método para dibujarlos como un rectanngulo azul
        pygame.draw.rect(pantalla, AZUL, 
                         (self.x, self.y, self.tamanio, self.tamanio))


class Mundo:                                #Clase mundo
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.elemento_fondo = [(MundoSprite(random.randint(0,ancho-40), 
                                        random.randint(0,alto-40))) for i in range (10)]
        #Exprecion generadora de 10 elementos Sprites en ubicacion random dentro del rango de la pantalla
        #Lista de clases mundoSprite con ubicaciones random dentro de el límite de la pantalla
    
    def dibujar_mundo (self, pantalla):                 
        pantalla.fill(VERDE)                     # Dibujar el mundo (color de fondo de relleno)
        for elemento in self.elemento_fondo:                # Cada elemento en la lista generada, es una instancia de clase con el método dibujar_Sprite 
            elemento.dibujar_Sprite(pantalla)               # Llamo al método de cada instancia de clase

class GrupoCamara (pygame.sprite.Group):        #Esta clase agrupa los sprites para redubijado masivo cuando se mueve la camara
    def __init__(self):
        super().__init__()
        self.display.surface = pygame.display.get_surface()

        #Offset de camara
        self.offset = pygame.math.Vector2()
        self.mitad_ancho = self.display_surface.get_size()[0] //2
        self.mitad.alto = self.display_surface.get_size()[1] //2


    def camara_centrada(self,target):
        self.offset.x = target.rect.center.x - self.mitad_ancho
        self.offset.y = target.rect.center.y - self.mitad_alto