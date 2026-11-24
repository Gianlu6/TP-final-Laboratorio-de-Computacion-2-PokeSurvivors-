import pygame       #Se instala con pip install pygame
import sys          #Para cerrar la ejecucion de codigo si se cierra el juego

from constantes import *                           #Librerías propias
from Personaje import Personaje
from Enemigo import *
from Mundo import *        #Importarlo de esta manera evita un error de 'Modulo'
from Ataque import *
from BarraVida import *
from sprites import *

#Inicialización de pygame
pygame.init() 

RELOJ = pygame.time.Clock()                                     #Tiempo del juego

#Creación de ventana gráfica
pygame.display.set_caption("Pokemon Survivor")      #Nombre de ventana el objeto "ventana" es la constante PANTALLA

#Set camara
camara_grupo = GrupoCamara()        #GRUPO DE CAMARA: para que se mueva la "camara" (no existe en realida movemos y dibujamos masivamente el mundo con la transformacion inversa del personaje)



mi_mundo = Mundo(WIDTH, HEIGHT,camara_grupo)                                            #Instancia de clase Mundo que abarca la resolucion de la pantalla (puede ser mas grande)
prota = Personaje(100, 50, 50, WIDTH//2, HEIGHT//2, prota_sprite, camara_grupo, 300)    #Instancia de personaje(Doble barra es división forzada a entero)
barra_prota = BarraVida(100, 600, 300, 50, prota.vida)
proyectiles = []


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
        
        #Funcion que crea y agrega enemigos a la lista hasta un limite
        spawneo_enemigos(prota,camara_grupo)

        #chequea colisiones con enemigos y te hace daño
        for enemigo in enemigos:
            if prota.rect.colliderect(enemigo.rect):
                prota.vida = 1


        disparo = prota.atacar(enemigos)
        if disparo is not None:
            proyectiles.append(disparo)

        for p in proyectiles:
            p.avanzar()
            if distancia_entre_puntos(p.posicion(), prota.posicion()) > p.rango: #Los proyectiles mueren pasado su rango
                
                p.estoy_vivo = False
                p.kill()        #Kill las saca del sprite group para que no se renderice mas
                continue
            for enemigo in enemigos:
                if p.estoy_vivo and p.rect.colliderect(enemigo.rect):
                    enemigo.vida = p.atacar(enemigo.vida, enemigo.defensa)
                    p.estoy_vivo = False
                    p.kill()                #Tambien mueren los proyectiles cuando impactan a un enemigo
                if enemigo.vida <=0:
                    enemigo.estoy_vivo = False
                    enemigo.kill()
    
    

        camara_grupo.update()
        
        VENTANA.fill((VERDE_OSCURO))                       #Color de Fondo 
        camara_grupo.camara_centrada(prota)                #Grupo

        # Limpiar proyectiles y enemigos muertos de las listas
        proyectiles[:] = [p for p in proyectiles if p.estoy_vivo]
        enemigos[:] = [e for e in enemigos if e.estoy_vivo]      


        #TEMPORAL. Si moris se cierra el juego
        if prota.vida <= 0:
            break

        barra_prota.dibujar(VENTANA, prota.vida)
        mostrar_texto(f"{prota.vida}/{prota.vida_max}", FUENTE_POKEMON2, AMARILLO, 200, 610)            #Muestra texto de la vida
        mostrar_texto(f"{prota.vida}/{prota.vida_max}", FUENTE_POKEMON1, NEGRO, 200, 610)            #Muestra texto de la vida
        pygame.display.flip()           #Actualiza la pantalla
        RELOJ.tick(60)                  #Limita el reloj a 60 fps o una velocidad mas "humana"

if __name__ =='__main__':               #Llamada al main() para ejecutar código principal
    main()
