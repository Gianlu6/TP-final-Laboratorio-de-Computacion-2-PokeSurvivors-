import pygame       #Se instala con pip install pygame
import sys          #Para cerrar la ejecucion de codigo si se cierra el juego
import threading
import queue

from constantes import *                           #Librerías propias
from Personaje import Personaje
from Enemigo import *
from Mundo import *        #Importarlo de esta manera evita un error de 'Modulo'
from Ataque import *
from BarraVida import *
from sprites import *
from Boton import *
from Llamada_Api import *

#variables de juego
juego_pausado = False

#cargar imagen de menu
menu_start = pygame.image.load("sprites/menu_start.png").convert_alpha()
menu_quit = pygame.image.load("sprites/menu_quit.png").convert_alpha()

#crear botones
boton_start = Boton(425, 260, menu_start, 5)
boton_quit = Boton(425, 360, menu_quit, 5)

arbol_img = cargar_imagen_arbol("recursos/Oak_Tree.png")

#Creacion de variables para usar hilos
cola_main = queue.Queue()                   #Cola donde se dejan las url y se extraen los datos obtenidos
evento_terminador = threading.Event()       #Evento para finalizar el hilo daemon

#Spawn de 5 por defecto para que no este vacio al principio (Criterio de eleccion: los mas debiles y con ventaja para Pikachu)
spawn_inicial = [{'nombre': 'magikarp', 'ataque': 10, 'defensa': 55, 'vida': 20, 'velocidad': 80, 'tipo': ['water'], 'altura': 9, 'sprite_url': 'recursos/magikarp.png'}, 
                {'nombre': 'horsea', 'ataque': 40, 'defensa': 70, 'vida': 30, 'velocidad': 60, 'tipo': ['water'], 'altura': 4, 'sprite_url': 'recursos/horsea.png'}, 
                {'nombre': 'tentacool', 'ataque': 40, 'defensa': 35, 'vida': 40, 'velocidad': 70, 'tipo': ['water', 'poison'], 'altura': 9, 'sprite_url': 'recursos/tentacool.png'}, 
                {'nombre': 'pidgey', 'ataque': 45, 'defensa': 40, 'vida': 40, 'velocidad': 56, 'tipo': ['normal', 'flying'], 'altura': 3, 'sprite_url': 'recursos/pidgey.png'}, 
                {'nombre': 'zubat', 'ataque': 45, 'defensa': 35, 'vida': 40, 'velocidad': 55, 'tipo': ['poison', 'flying'], 'altura': 8, 'sprite_url': 'recursos/zubat.png'}]
spawn_activo = []

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
    global camara_grupo, prota, barra_prota, juego_pausado
    
    juego_pausado = False
    reiniciar_arboles()
    enemigos.clear()
    camara_grupo = GrupoCamara("recursos/pasto.jpg")
    prota = Personaje(1000, 55, 40, 'electric', WIDTH//2, HEIGHT//2,
                      prota_sprite, camara_grupo, 1, VELOCIDAD_PERSONAJE)
    barra_prota = BarraVida(100, 600, 300, 50, prota.vida_max)
            
def jugar():
    global juego_pausado
    global spawn_activo
    
    #Se inician el hilo secundario
    hilo1 = threading.Thread(target=hilo_oleada,args=(cola_main,evento_terminador),daemon=True)
    hilo1.start()
    pokemones_actuales = []
    ejecutando = True

    #Cargar los pokemones iniciales:
    spawn_activo[:] = [p.copy() for p in spawn_inicial]
    for pokemon in spawn_activo:
        if "sprite_final" not in pokemon:
            img_cruda = pygame.image.load(pokemon["sprite_url"]).convert_alpha() 
            normalizar_escala = 30*((pokemon['altura']*10)**COEFICIENTE_ESCALA)      
            pokemon["sprite_final"]= pygame.transform.scale(img_cruda, (normalizar_escala, normalizar_escala))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
                evento_terminador.set() 
                pygame.quit()
                sys.exit()


            # Espera teclas para pausar con barra espaciadora
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                juego_pausado = not juego_pausado

            
            if juego_pausado and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if boton_start.rect.collidepoint(event.pos):
                    juego_pausado = False
                elif boton_quit.rect.collidepoint(event.pos):
                    evento_terminador.set() 
                    pygame.quit()
                    sys.exit()

        if not juego_pausado:
            #Espera de las teclas para moverse
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

            actualizar_arboles(prota, camara_grupo, arbol_img)


            #Cambio de oleada
            try:
                oleada_recibida = cola_main.get_nowait()        #Parecido al comando .get() pero en vez de bloquearse cuando esta vacia lanza una exepcion (PROBAR QUE PASA CON GET SOLO)
                for pokemon in oleada_recibida:
                    if "sprite_final" not in pokemon:

                        pokemon["sprite_final"] = pokemon["sprite"].convert_alpha()   #Recien aca se recorta la imagen porque era una operacion Thread-safe 

                        #Normalizador de escalas para que la diferencia de tamaños entre pokemones no sea zarpada. 
                        # 30 (escala Prota) por la altura en cm (La api la guarda en dm) y un "exponente de comprecion" o raiz que 
                        # achique los valores grandes y agrande los chicos. Cuanto mas chico sea el valor menos diferencia de escala va a ver
                    
                        escala_normalizada = 30*((pokemon['altura']*10)**COEFICIENTE_ESCALA)      
                        pokemon["sprite_final"]= pygame.transform.scale(pokemon["sprite"], (escala_normalizada, escala_normalizada))
                spawn_activo = oleada_recibida          #Los datos depositados en oleada_recibida pasan a la lista que usa el spawn constantemente
    
            except queue.Empty:
                
                pass    #Ignorar si no hay oleada nueva
    
            if spawn_activo:
                spawneo_enemigos(prota, camara_grupo,spawn_activo)
            
            arboles = arboles_cercanos(prota)
            
            for enemigo in enemigos:
                enemigo.atacar(prota)
                for arbol in arboles:
                    colision_solida(enemigo, arbol)
                
            for arbol in arboles:
                colision_solida(prota, arbol) 
            
            prota.atacar()
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