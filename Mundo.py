import pygame
import random
from constantes import *

class Arbol(pygame.sprite.Sprite):
    def __init__(self, x, y, grupo, imagen):
        super().__init__(grupo)
        self.x = x
        self.y = y
        self.image = imagen
        self.rect = self.image.get_rect(midbottom=(x, y))
        
def generar_arboles(grupo, cantidad, ancho_mundo, alto_mundo, ruta_imagen, escala=1, separacion=80, ):
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        if escala != 1:
            imagen = pygame.transform.scale_by(imagen, escala)
        arboles = []
        intentos = 0
        while len(arboles) < cantidad and intentos < cantidad * 20:
            intentos += 1
            x = random.randint(0, ancho_mundo)
            y = random.randint(0, alto_mundo)
            if all(abs(x - a.rect.centerx) > separacion or abs(y - a.rect.centery) > separacion
                    for a in arboles):
                arboles.append(Arbol(x, y, grupo, imagen))
                
        return arboles
        

class GrupoCamara (pygame.sprite.Group):        #Esta clase agrupa los sprites para redubijado masivo cuando se mueve la camara
    def __init__(self, ruta_fondo=None):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #Offset de camara
        self.offset = pygame.math.Vector2()
        self.mitad_ancho = self.display_surface.get_size()[0] //2
        self.mitad_alto = self.display_surface.get_size()[1] //2

        #fondo
        self.fondo = None
        if ruta_fondo:
            self.set_fondo(ruta_fondo)

    def set_fondo(self, ruta_fondo): #carga la imagen de suelo
        self.fondo = pygame.image.load(ruta_fondo).convert()
        self.fondo_ancho, self.fondo_alto = self.fondo.get_size()

    def dibujar_fondo(self):
        if self.fondo is None:
            return
        
        pantalla_ancho, pantalla_alto = self.display_surface.get_size()
        inicio_x = -(int(self.offset.x) % self.fondo_ancho)
        inicio_y = -(int(self.offset.y) % self.fondo_alto)
        
        for x in range(inicio_x, pantalla_ancho, self.fondo_ancho):
            for y in range(inicio_y, pantalla_alto, self.fondo_alto):
                self.display_surface.blit(self.fondo, (x, y))

    def camara_centrada(self,target):                                              #Método que aplica una transformacion inversa al mundo en base a un target: el personaje
        self.offset.x = target.rect.centerx - self.mitad_ancho
        self.offset.y = target.rect.centery - self.mitad_alto

        for sprite in sorted(self.sprites(), key=lambda s: (getattr(s,'z',1), s.rect.centery)):         
        #El sorted + lambda se usa ordenar y dibujar los sprites con 2 criterios: 
        #El primero prioridad z, siendo 1 en SerVivo y 0 en Movimientos o sprites de ataque,
        # y el segundo criterio es por linea del mas alto en "y" al mas bajo (profundidad de atras hacia adelante)
            rect_visual = sprite.image.get_rect(center=sprite.rect.center)          #Si a un sprite se le ajusta la hitbox con un rect.inflate, etc la colicion es forzada a estar anclada en el centro  
            off_pos = rect_visual.topleft - self.offset
            self.display_surface.blit(sprite.image, off_pos)

            #Dibujar vida enemigos y letritas con metodo separado
            if hasattr(sprite,"mostrar_numeros_impacto"):
                sprite.mostrar_numeros_impacto(self.display_surface, self.offset)