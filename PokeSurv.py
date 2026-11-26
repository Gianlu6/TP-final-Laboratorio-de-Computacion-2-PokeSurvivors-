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
menu_start = pygame.image.load("menu_start.png").convert_alpha()
menu_quit = pygame.image.load("menu_quit.png").convert_alpha()

#crear botones
boton_start = Boton(450, 260, menu_start, 5)
boton_quit = Boton(365, 60, menu_quit, 5)

#Creación de la función principal
def main():
    global juego_pausado
    while True:
        if juego_pausado == True:
            if boton_start.dibujar(VENTANA):#menu
                juego_pausado = False
            
            elif boton_quit.dibujar(VENTANA):
                pygame.quit()
                sys.exit()
        
        #BUCLE DEL JUEGO
        for event in pygame.event.get():                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    juego_pausado = not juego_pausado
                    
            # Si clickeas la x de cerrar ventana, termina el programa
            if event.type == pygame.QUIT: 
                pygame.quit()                                        # Se quita el juego
                sys.exit()                #Se mata la ejecución

        #Input de teclas
        if not juego_pausado:
            tecla = pygame.key.get_pressed()                            # Espera tecla del jugador
            if tecla[pygame.K_LEFT]:                                    # Analiza la tecla del jugador
                prota.moverse(-prota.velocidad, 0)                      # Teclear con las flechas mueve al personaje en eje 'x' e 'y'
            if tecla[pygame.K_RIGHT]:
                prota.moverse(prota.velocidad, 0)
            if tecla[pygame.K_UP]:
                prota.moverse(0, -prota.velocidad)                             #EN PYGAME EL EJE 'Y' HACIA ARRIBA ES NEGATIVO
            if tecla[pygame.K_DOWN]:
                prota.moverse(0, prota.velocidad)
            
            #Funcion que crea y agrega enemigos a la lista hasta un limite
            spawneo_enemigos(prota,camara_grupo)

            #chequea colisiones con enemigos y te hace daño
            for enemigo in enemigos:
                enemigo.atacar(prota)

            prota.atacar(enemigos)
        
            prota.actualizar_posicion_armas()

            camara_grupo.update()           #Dibujo masivo de sprites 
            
            camara_grupo.dibujar_fondo()                       #Dibujo de fondo pasto infinito    
            camara_grupo.camara_centrada(prota)                #El camara_grupo mueve los sprites simulando un movimiento de camara

            # Limpiar enemigos muertos de las listas
            enemigos[:] = [e for e in enemigos if e.estoy_vivo]      

            #TEMPORAL. Si moris se cierra el juego
            if prota.vida <= 0:
                break
        
        barra_prota.dibujar(VENTANA, prota.vida, prota.vida_max)
        mostrar_texto(f"{prota.vida}/{prota.vida_max}", FUENTE_POKEMON2, AMARILLO, 200, 610)            #Muestra texto de la vida
        mostrar_texto(f"{prota.vida}/{prota.vida_max}", FUENTE_POKEMON1, NEGRO, 200, 610)            #Muestra texto de la vida
        pygame.display.flip()           #Actualiza la pantalla
        RELOJ.tick(60)                  #Limita el reloj a 60 fps o una velocidad mas "humana

if __name__ =='__main__':               #Llamada al main() para ejecutar código principal
    #Inicialización de pygame
    pygame.init() 

    RELOJ = pygame.time.Clock()                                     #Tiempo del juego

    #Creación de ventana gráfica
    pygame.display.set_caption("Pokemon Survivor")      #Nombre de ventana el objeto "ventana" es la constante PANTALLA

    #Set camara
    camara_grupo = GrupoCamara("recursos\pasto.jpg")        #GRUPO DE CAMARA: para que se mueva la "camara" (no existe en realida movemos y dibujamos masivamente el mundo con la transformacion inversa del personaje)

    prota = Personaje(100, 55, 40, 'electric', WIDTH//2, HEIGHT//2, prota_sprite, camara_grupo, 1,VELOCIDAD_PERSONAJE)    #Instancia de personaje(Doble barra es división forzada a entero)
    barra_prota = BarraVida(100, 600, 300, 50, prota.vida_max)
    arboles = generar_arboles(camara_grupo, 50, 3000, 3000, "recursos\Oak_Tree.png", 3)

    main()
