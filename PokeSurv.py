import pygame       #Se instala con pip install pygame
import sys          #Para cerrar la ejecucion de codigo si se cierra el juego

from constantes import *                           #Librerías propias
from Personaje import Personaje
from Enemigo import *
from Mundo import *        #Importarlo de esta manera evita un error de 'Modulo'
from Ataque import *
from BarraVida import *
from sprites import *
from Boton import *

#variables de juego
juego_pausado = False

#cargar imagen de menu
menu_start = pygame.image.load("sprites/menu_start.png").convert_alpha()
menu_quit = pygame.image.load("sprites/menu_quit.png").convert_alpha()

#crear botones
boton_start = Boton(425, 260, menu_start, 5)
boton_quit = Boton(425, 360, menu_quit, 5)

arbol_img = cargar_imagen_arbol("recursos/Oak_Tree.png")

def menu_principal():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if boton_start.rect.collidepoint(event.pos):
                    return
                elif boton_quit.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        camara_grupo.dibujar_fondo()
        boton_start.dibujar(VENTANA)            # solo dibuja
        boton_quit.dibujar(VENTANA)
        pygame.display.flip()
        RELOJ.tick(60)


def nueva_partida():
    global camara_grupo, prota, barra_prota, arboles, juego_pausado
    
    juego_pausado = False
    enemigos.clear()
    camara_grupo = GrupoCamara("recursos/pasto.jpg")
    prota = Personaje(100, 55, 40, 'electric', WIDTH//2, HEIGHT//2,
                      prota_sprite, camara_grupo, 1, VELOCIDAD_PERSONAJE)
    barra_prota = BarraVida(100, 600, 300, 50, prota.vida_max)
            
def jugar():
    global juego_pausado
    Inicio_De_Tanda = pygame.time.get_ticks()       #Tiempo de inicio de juego excluyendo el tiempo en menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                juego_pausado = not juego_pausado

            if juego_pausado and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if boton_start.rect.collidepoint(event.pos):
                    juego_pausado = False
                elif boton_quit.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        if not juego_pausado:
            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_LEFT]:
                prota.moverse(-prota.velocidad, 0)
                prota.is_derecha = True
            if tecla[pygame.K_RIGHT]:
                prota.moverse(prota.velocidad, 0)
                prota.is_derecha = False
            if tecla[pygame.K_UP]:
                prota.moverse(0, -prota.velocidad)
            if tecla[pygame.K_DOWN]:
                prota.moverse(0, prota.velocidad)

            spawneo_enemigos(prota, camara_grupo)
            
            actualizar_arboles(prota, camara_grupo, arbol_img)
            arboles = arboles_cercanos(prota)
            
            for enemigo in enemigos:
                enemigo.atacar(prota)
                for arbol in arboles:
                    colision_solida(enemigo, arbol)
                
            for arbol in arboles:
                colision_solida(prota, arbol) 
            
            prota.atacar(enemigos)
            prota.actualizar_posicion_armas()
            camara_grupo.update()

            enemigos[:] = [e for e in enemigos if e.estoy_vivo]

            if prota.vida <= 0:
                return                      # murió: vuelve a main()

        camara_grupo.dibujar_fondo()
        camara_grupo.camara_centrada(prota)
        barra_prota.dibujar(VENTANA, prota.vida, prota.vida_max)
        mostrar_texto(f"{prota.vida}/{prota.vida_max}", FUENTE_POKEMON2, AMARILLO, 200, 610)
        mostrar_texto(f"{prota.vida}/{prota.vida_max}", FUENTE_POKEMON1, NEGRO, 200, 610)

        if juego_pausado:
            boton_start.dibujar(VENTANA)
            boton_quit.dibujar(VENTANA)

        pygame.display.flip()
        RELOJ.tick(60)

#Creación de la función principal
def main():
    while True:
        menu_principal()
        nueva_partida()
        jugar()
    
if __name__ =='__main__':               #Llamada al main() para ejecutar código principal
    pygame.init()
    RELOJ = pygame.time.Clock()
    pygame.display.set_caption("Pokemon Survivor")

    camara_grupo = GrupoCamara("recursos/pasto.jpg")   # para que exista en el primer menú
    main()