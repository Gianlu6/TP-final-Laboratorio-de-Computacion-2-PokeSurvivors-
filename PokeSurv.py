import pygame       #Se instala con pip install pygame
import sys          #Para cerrar la ejecucion de codigo si se cierra el juego
import time

from constantes import *                           #Librerías propias
from Personaje import Personaje
from Enemigo import Enemigo
from Mundo import Mundo, MundoSprite        #Importarlo de esta manera evita un error de 'Modulo'

#Inicialización de pygame
pygame.init() 

RELOJ = pygame.time.Clock()                                     #Tiempo del juego

#Creación de ventana gráfica
pygame.display.set_caption("Pokemon Survivor")      #Nombre de ventana

#INICIALIZANDO SPRITES
prota_sprite_load = pygame.image.load("main_pikachu.png").convert_alpha()
prota_sprite = pygame.transform.scale(prota_sprite_load, (100, 100))
malo_sprite_load = pygame.image.load("malo.jpg").convert_alpha()
malo_sprite = pygame.transform.scale(malo_sprite_load, (100, 100))
proyectil_sprite_load = pygame.image.load("proyectil.png").convert_alpha()
proyectil_sprite = pygame.transform.scale(proyectil_sprite_load, (30, 30))

#Creación de la función principal
def main():
    mi_mundo = Mundo(WIDTH, HEIGHT)           #Instancia de clase Mundo que abarca la resolucion de la pantalla (puede ser mas grande)
    prota = Personaje(100, 50, 50, WIDTH//2, HEIGHT//2, prota_sprite)    #Instancia de personaje(Doble barra es división forzada a entero)
    malo1 = Enemigo(100, 50, 50, WIDTH//4, HEIGHT//4, malo_sprite)
    malo2 = Enemigo(100, 50, 50, WIDTH//6, HEIGHT//6, malo_sprite)

    enemigos = [malo1, malo2]

    while True:                                                     #BUCLE DEL JUEGO
        for event in pygame.event.get():                            # Si clickeas la x de cerrar ventana, termina el programa
           if event.type == pygame.QUIT: 
               pygame.quit()                                        # Se quita el juego
               sys.exit()                                           #Se mata la ejecución

        tecla = pygame.key.get_pressed()                            # Espera tecla del jugador
        if tecla[pygame.K_LEFT]:                                    # Analiza la tecla del jugador
            prota.moverse(-VELOCIDAD_PERSONAJE, 0)                                     # Teclear con las flechas mueve al personaje en eje 'x' e 'y'
        if tecla[pygame.K_RIGHT]:
            prota.moverse(VELOCIDAD_PERSONAJE, 0)
        if tecla[pygame.K_UP]:
            prota.moverse(0, -VELOCIDAD_PERSONAJE)                             #EN PYGAME EL EJE 'Y' HACIA ARRIBA ES NEGATIVO
        if tecla[pygame.K_DOWN]:
            prota.moverse(0, VELOCIDAD_PERSONAJE)


        mi_mundo.dibujar_mundo(VENTANA)
        mostrar_texto(f"{prota.vida}", FUENTE, NEGRO, 1000, 600)
        prota.dibujar()      
       
        for enemigo in enemigos:
            enemigo.avanzar(prota)#EL ORDEN IMPORTA, PRIMERO DIBUJAR EL MUNDO Y ARRIBA DE ESO EL/LOS PERSONAJE/S
            enemigo.dibujar()
            separar(malo1, malo2) #TEMPORAL HASTA QUE VEAMOS QUE ONDA
            separar(prota, enemigo)
                    
            #chequea colisiones con enemigos y te hace daño
            if prota.rect.colliderect(enemigo.rect):
                prota.vida -= 3
                
        #TEMPORAL. Si moris se cierra el juego
        if prota.vida <= 0:
            break
            
       
        pygame.display.flip()           #Actualiza la pantalla
        RELOJ.tick(60)                  #Limita el reloj a 60 fps o una velocidad mas "humana"


if __name__ =='__main__':               #Llamada al main() para ejecutar código principal
    main()
