import pygame
import random
import constantes


class mundoSprite:                              #Clase que genera elementos en el mundo
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tamanio = 40

    def dibujar_Sprite(self, pantalla):         #Método para dibujarlos como un rectanngulo azul
        pygame.draw.rect(pantalla, constantes.AZUL, 
                          (self.x, self.y, self.tamanio, self.tamanio))


class Mundo:                                #Clase mundo
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.elemento_fondo = [(mundoSprite(random.randint(0,ancho-40), 
                                        random.randint(0,alto-40))) for i in range (10)]
        #Exprecion generadora de 10 elementos Sprites en ubicacion random dentro del rango de la pantalla
        #Lista de clases mundoSprite con ubicaciones random dentro de el límite de la pantalla
    
    def dibujar_mundo (self, pantalla):                 
        pantalla.fill(constantes.VERDE)                     # Dibujar el mundo (color de fondo de relleno)
        for elemento in self.elemento_fondo:                # Cada elemento en la lista generada, es una instancia de clase con el método dibujar_Sprite 
            elemento.dibujar_Sprite(pantalla)               # Llamo al método de cada instancia de clase

