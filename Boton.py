import pygame, sys
from constantes import *

fuente = pygame.font.SysFont("arialblack", 40)

class Boton():
    def __init__(self, x, y, imagen, escala):
        ancho = imagen.get_width()
        alto = imagen.get_height()
        self.imagen = pygame.transform.scale(imagen, (int(ancho * escala), int(alto * escala)))
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (x, y)
        self.cliqueado = False
        self.mask = pygame.mask.from_surface(self.imagen)
        
    def mouse_encima(self, pos):
        if not self.rect.collidepoint(pos):
            return False 
        local_x = pos[0] - self.rect.x
        local_y = pos[1] - self.rect.y 
        
        return bool(self.mask.get_at((local_x, local_y)))   
    
    def dibujar(self, superficie):
        accion = False
        #pos del mouse
        pos = pygame.mouse.get_pos()
        
        #si pasa arriba el mouse y condiciones
        if self.mouse_encima(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.cliqueado == False:
                self.cliqueado = True
                accion = True 
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.cliqueado = False
            
        #dibujar el boton
        superficie.blit(self.imagen, (self.rect.x, self.rect.y))
        
        return accion
