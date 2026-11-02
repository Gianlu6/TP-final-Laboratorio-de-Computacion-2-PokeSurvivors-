import pygame       #Se instala con pip install pygame
import sys          #Para cerrar la ejecucion de codigo si se cierra el juego

import constantes                           #Librerías propias
from Personaje import miPokemon
from Mundo import Mundo, mundoSprite        #Importarlo de esta manera evita un error de 'Modulo'

#Inicialización de pygame
pygame.init() 


#Creación de ventana gráfica
ventana = pygame.display.set_mode((constantes.WIDTH,  constantes.HEIGHT))
pygame.display.set_caption("Pokemon Survivor")      #Nombre de ventana

#Creación de la función principal
def main():
    reloj = pygame.time.Clock()                                     #Tiempo del juego
    mi_Mundo = Mundo(constantes.WIDTH, constantes.HEIGHT)           #Instancia de clase Mundo que abarca la resolucion de la pantalla (puede ser mas grande)
    prota = miPokemon(constantes.WIDTH//2, constantes.HEIGHT//2)    #Instancia de personaje(Doble barra es división forzada a entero)


    while True:                                                     #BUCLE DEL JUEGO
        for event in pygame.event.get():                            # Si clickeas la x de cerrar ventana, termina el programa
           if event.type == pygame.QUIT: 
               pygame.quit()                                        # Se quita el juego
               sys.exit()                                           #Se mata la ejecución

        tecla = pygame.key.get_pressed()                            # Espera tecla del jugador
        if tecla[pygame.K_LEFT]:                                    # Analiza la tecla del jugador
            prota.moverse(-5,0)                                     # Teclear con las flechas mueve al personaje en eje 'x' e 'y'
        if tecla[pygame.K_RIGHT]:
                    prota.moverse(5,0)
        if tecla[pygame.K_UP]:
                    prota.moverse(0,-5)                             #EN PYGAME EL EJE 'Y' HACIA ARRIBA ES NEGATIVO
        if tecla[pygame.K_DOWN]:
            prota.moverse(0,5)


        mi_Mundo.dibujar_mundo(ventana)                             #Llamo a los métodos de las clases para dibujar en pantalla
        prota.dibujar_pj(ventana)                                   #EL ORDEN IMPORTA, PRIMERO DIBUJAR EL MUNDO Y ARRIBA DE ESO EL/LOS PERSONAJE/S

        pygame.display.flip()           #Actualiza la pantalla
        reloj.tick(60)                  #Limita el reloj a 60 fps o una velocidad mas "humana"


if __name__ =='__main__':               #Llamada al main() para ejecutar código principal
    main()
