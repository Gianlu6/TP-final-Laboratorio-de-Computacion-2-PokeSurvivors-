import pygame       #Se instala con pip install pygame
import sys          #Para cerrar la ejecucion de codigo si se cierra el juego
import time

from constantes import *                           #Librerías propias
from Personaje import Personaje
from Enemigo import Enemigo
from Mundo import *        #Importarlo de esta manera evita un error de 'Modulo'
from Llamada_Api import obtenerPikachu

#Inicialización de pygame
pygame.init() 

RELOJ = pygame.time.Clock()                                     #Tiempo del juego

#Creación de ventana gráfica
pygame.display.set_caption("Pokemon Survivor")      #Nombre de ventana el objeto "ventana" es la constante PANTALLA

#Set camara
camara_grupo = GrupoCamara()        #GRUPO DE CAMARA: para que se mueva la "camara" (no existe en realida movemos y dibujamos masivamente el mundo con la transformacion inversa del personaje)


#INICIALIZANDO SPRITES
#prota_sprite_load = pygame.image.load(obtenerPikachu()).convert_alpha()        #PROXIMAMENTE: obtencion de datos de la API
prota_sprite_load = pygame.image.load("main_pikachu.png").convert_alpha()
prota_sprite = pygame.transform.scale(prota_sprite_load, (100, 100))
malo_sprite_load = pygame.image.load("malo.jpg").convert_alpha()
malo_sprite = pygame.transform.scale(malo_sprite_load, (100, 100))
proyectil_sprite_load = pygame.image.load("proyectil.png").convert_alpha()
proyectil_sprite = pygame.transform.scale(proyectil_sprite_load, (30, 30))

mi_mundo = Mundo(WIDTH, HEIGHT,camara_grupo)           #Instancia de clase Mundo que abarca la resolucion de la pantalla (puede ser mas grande)
prota = Personaje(100, 50, 50, WIDTH//2, HEIGHT//2, prota_sprite, camara_grupo)    #Instancia de personaje(Doble barra es división forzada a entero)
malo1 = Enemigo(100, 50, 50, WIDTH//4, HEIGHT//4, malo_sprite,camara_grupo)
malo2 = Enemigo(100, 50, 50, WIDTH//6, HEIGHT//6, malo_sprite,camara_grupo)

enemigos = [malo1, malo2]



#Creación de la función principal
def main():
    while True:                                                     #BUCLE DEL JUEGO
        for event in pygame.event.get():                            # Si clickeas la x de cerrar ventana, termina el programa
           if event.type == pygame.QUIT: 
               pygame.quit()                                        # Se quita el juego
               sys.exit()                #Se mata la ejecución

        #Input de teclas
        tecla = pygame.key.get_pressed()                            # Espera tecla del jugador
        if tecla[pygame.K_LEFT]:                                    # Analiza la tecla del jugador
            prota.moverse(-VELOCIDAD_PERSONAJE, 0)                  # Teclear con las flechas mueve al personaje en eje 'x' e 'y'
        if tecla[pygame.K_RIGHT]:
            prota.moverse(VELOCIDAD_PERSONAJE, 0)
        if tecla[pygame.K_UP]:
            prota.moverse(0, -VELOCIDAD_PERSONAJE)                             #EN PYGAME EL EJE 'Y' HACIA ARRIBA ES NEGATIVO
        if tecla[pygame.K_DOWN]:
            prota.moverse(0, VELOCIDAD_PERSONAJE)
      
       
        for enemigo in enemigos:
            enemigo.avanzar(prota) #EL ORDEN IMPORTA, PRIMERO DIBUJAR EL MUNDO Y ARRIBA DE ESO EL/LOS PERSONAJE/S
    
            separar(malo1, malo2) #TEMPORAL HASTA QUE VEAMOS QUE ONDA
            separar(prota, enemigo)
                    
            #chequea colisiones con enemigos y te hace daño
            if prota.rect.colliderect(enemigo.rect):
                prota.vida -= 3
                
        #TEMPORAL. Si moris se cierra el juego
        if prota.vida <= 0:
            break

          
        camara_grupo.update()
        
        VENTANA.fill((VERDE))                       #Color de Fondo 
        camara_grupo.camara_centrada(prota)         #Grupo

        mostrar_texto(f"{prota.vida}", FUENTE, NEGRO, 1000, 600)            #Muestra texto de la vida
               

        pygame.display.flip()           #Actualiza la pantalla
        RELOJ.tick(60)                  #Limita el reloj a 60 fps o una velocidad mas "humana"


if __name__ =='__main__':               #Llamada al main() para ejecutar código principal
    main()
