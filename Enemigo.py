import math
from Clases_Abs import SerVivo
import pygame
from constantes import *
from sprites import *
import random

ultimo_spawn = 0
enemigos = []
Inicio_De_Tanda = 0

class Enemigo(SerVivo):
    def __init__(self, vida_max, ataque, defensa, tipo, x, y, image, grupo, velocidad=2):
        super().__init__(vida_max, ataque, defensa, tipo, x, y, image, grupo, velocidad)
        self.intervalo = 500
        self.ultimo_chequeo = 0
        self.objetivo = (x, y)
        self.vida = vida_max        #Esto fue privatizado y convertido con @property en la clase SerVivo

        #Forzar la forma de la hitbox acorde a la imagen sprite recibido 
        #Como la colicion esta basada en el atributo self.rect este solo acepta formas rectangulares
        #Basadas en la resolucion total de la imagen, sin tener en cuenta su transparencia
        self.mask = pygame.mask.from_surface(self.image)    #Extraigo el alfa
        self.rect_lista = self.mask.get_bounding_rects()    #Transformo el alfa en cuadraditos chiquitos
        if self.rect_lista: #Si no esta vacio...
            self.rect = self.rect_lista[0].unionall(self.rect_lista[1:])    #Le asigno a self.rect esos rectangulos chicos unificados
            self.rect.center = (x,y)    

    def atacar(self,objetivo):
        if self.rect.colliderect(objetivo.rect):
            objetivo.quitar_vida(self.ataque)

    def avanzar(self, Personaje):
        ahora = pygame.time.get_ticks() #devuelve cuantos segundos pasaron desde pygame.init()
        
        #cada intervalo actualiza el objetivo
        if ahora - self.ultimo_chequeo >= self.intervalo:
            self.objetivo = self.buscar_pos(Personaje)
            self.ultimo_chequeo = ahora 
            
        #se mueve hacia el obj
        dx = self.objetivo[0] - self.x 
        dy = self.objetivo[1] - self.y
        distancia = math.hypot(dx, dy)
        
        #chequea si la distancia es mayor a la velocidad para ir asi no hay mov raros
        if distancia > self.velocidad:
            self.moverse(dx / distancia * self.velocidad, dy / distancia * self.velocidad)

    def mostrar_numeros_impacto(self,superficie,offset):    #Voy a llamar un dibjuado especial desde grupo camara para los numeritos de daño
        if self.vida < self.vida_max:
            barra_ancho= 50
            barra_alto = 6

            barra_x = self.rect.centerx - (barra_ancho // 2) - offset.x
            barra_y = self.rect.top - 12 - offset.y

            ratio = max(0,self.vida / self.vida_max)
            ancho_actual = int(barra_ancho*ratio)

            bg_barra = pygame.Rect(barra_x,barra_y,barra_ancho,barra_alto)
            vida_barra = pygame.Rect(barra_x,barra_y,ancho_actual,barra_alto)

            pygame.draw.rect(superficie, AZUL, bg_barra)
            pygame.draw.rect(superficie, VERDE, vida_barra)

            texto_offset_x = self.x - offset.x - (self.image.get_width()//2)
            texto_offset_y = self.y - offset.y + 10        
            mostrar_texto(f"{round(self.vida)}", FUENTE, NEGRO, texto_offset_x,texto_offset_y )            #Muestra texto de la vida



def spawneo_enemigos(personaje, grupo, especies_activas):
    global ultimo_spawn
    ahora = pygame.time.get_ticks()
    
    if len (enemigos) < 30 and ahora - ultimo_spawn >= 1000:
        ultimo_spawn = ahora

        #Spawn en un radio alrededor del personaje
        radio_minimo = (WIDTH//2)+50    #Menos de 50 pixeles del personaje no spawnean
        radio_maximo = (WIDTH//2)+250   #Mas de 250 pixeles del persojane no spawnean
        angulo= random.uniform(0, 360)  
        dist = random.uniform(radio_minimo,radio_maximo)

        # Vector con angulo y distancia random
        desplazamiento_spawn = pygame.math.Vector2(0,-1).rotate(angulo)*dist
        x = int(personaje.x + desplazamiento_spawn.x)       #Podes acceder a la pocicion de un vector llamando ".x", ".y"
        y = int(personaje.y + desplazamiento_spawn.y)   

        especie_elegida = random.choice(especies_activas)       #Random choise elige elemento al azar de un iterable
        enemigos.append(Enemigo(especie_elegida['vida'], especie_elegida['ataque'], especie_elegida['defensa'], especie_elegida['tipo'], x, y, especie_elegida['sprite_final'], grupo))

    for enemigo in enemigos:
        enemigo.avanzar(personaje)
        colision_empuje(enemigo,personaje)
    colision_todos(enemigos)