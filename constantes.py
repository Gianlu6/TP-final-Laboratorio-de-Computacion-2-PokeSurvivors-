#Resolución
import pygame
import math
import random
from itertools import combinations


pygame.font.init()

WIDTH, HEIGHT = 1080, 720    
VELOCIDAD_PERSONAJE = 3.50


#Colores Básico (Tupla de valores RGB 8 bits, 0-255)
AZUL = (0,0,255)
ROJO = (255,0,0)
VERDE_OSCURO = (69, 139, 0)
VERDE = (0,255,0)
BLANCO = (255,255,255)
NEGRO = (0,0,0)
AMARILLO = (255,255,0)

VENTANA = pygame.display.set_mode((WIDTH, HEIGHT))
FUENTE = pygame.font.SysFont("Arial", 30)
FUENTE_POKEMON1 = pygame.font.Font("recursos\Pokemon Hollow.ttf",30)
FUENTE_POKEMON2 = pygame.font.Font("recursos\Pokemon Solid.ttf",30)



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

    
#con combinations, creas todas las combinaciones posibles de dos unidades y llamas separar con cada una
def separar_todos(entidades):
    for a, b in combinations(entidades, 2):
        separar(a, b)

#Distancia entre dos posiciones. Recibe dos tuplas de poscicion x,y y devuelve distancia 
def distancia_entre_puntos(a,b):
    dif_x = a[0] - b[0]
    dif_y = a[1] - b[1]
    return math.hypot(dif_x, dif_y)

#Recibe varios parametros y retorna el calculo de danio a aplicar a la vida. Recibe referencia de las entidades
def calculo_danio(emisor,destinatario,ataque_movimiento,tipo_movimiento):
    mult_tipo=1
    if tipo_movimiento == 'electric':       #Si Pikachu ataca
        if destinatario.tipo=='ground':
            mult_tipo = 0
        elif destinatario.tipo=='water' or destinatario.tipo=='flying':
            mult_tipo = 2
        elif destinatario.tipo=='dragon' or destinatario.tipo=='electric' or destinatario.tipo=='grass':
            mult_tipo = 0.5
    if destinatario.tipo == 'electric':     #Si atacan a Pikachu
        if emisor.tipo == 'ground':
            mult_tipo = 2
        elif emisor.tipo == 'electric' or emisor.tipo == 'flying' or emisor.tipo == 'steel':
            mult_tipo = 0.5
    cuenta = ataque_movimiento*(emisor.ataque/destinatario.defensa)*mult_tipo*random.uniform(0.95,1.05)
    return cuenta

#La multiplicacion de daño que hace Pikachu segun tipo:
# x0 si el enemigo es Tierra (Inmune)
# x2 si es Agua o Volador (debil a la electricidad)
# x0.5 a Dragon, Eléctrico o planta
# x1 al resto de los tipos

#La multiplicacion del ataque del enemigo hacia Pikachu
# x2 de daño si lo ataca un tipo Tierra
# x0.5 electrico, volador, acero
# x1 el resto