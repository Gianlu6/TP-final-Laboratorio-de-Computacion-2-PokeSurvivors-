#Resolución
import pygame
import math

pygame.font.init()

WIDTH, HEIGHT = 1080, 720    
VELOCIDAD_PERSONAJE = 3.50

#Colores Básico (Tupla de valores RGB 8 bits, 0-255)
AZUL = (0,0,255)
ROJO = (255,0,0)
VERDE = (0,255,0)
BLANCO = (255,255,255)
NEGRO = (0,0,0)
AMARILLO = (255,255,0)

VENTANA = pygame.display.set_mode((WIDTH, HEIGHT))
FUENTE = pygame.font.SysFont("Arial", 30)

def mostrar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    VENTANA.blit(img, (x, y))
    
def separar(entidad_a, entidad_b):   
    if not entidad_a.rect.colliderect(entidad_b.rect):
        return #si no hay colision no hace nada
    
    #donde se superpone cada eje
    overlap_x = min(entidad_a.rect.right, entidad_b.rect.right) - max(entidad_a.rect.left, entidad_b.rect.left)
    overlap_y = min(entidad_a.rect.bottom, entidad_b.rect.bottom) - max(entidad_a.rect.top, entidad_b.rect.top)
    
    # se corrige el eje donde la posicion es menor
    if overlap_x < overlap_y:
        empuje = overlap_x / 2
        if entidad_a.rect.centerx < entidad_b.rect.centerx:
            entidad_a.x -= empuje
            entidad_b.x += empuje
            
        else:
            entidad_a.x += empuje
            entidad_b.x -= empuje 
            
    else:
        empuje = overlap_y / 2
        if entidad_a.rect.centery < entidad_b.rect.centery:
            entidad_a.y -= empuje
            entidad_b.y += empuje
            
        else:
            entidad_a.y += empuje
            entidad_b.y -= empuje 
            
    entidad_a.rect.center = (entidad_a.x, entidad_a.y)
    entidad_b.rect.center = (entidad_b.x, entidad_b.y)