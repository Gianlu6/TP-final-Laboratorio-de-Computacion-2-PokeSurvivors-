import pygame
from Llamada_Api import *

#INICIALIZANDO SPRITES

#prota_sprite_load = pygame.image.load(obtenerPikachu()).convert_alpha()        #PROXIMAMENTE: obtencion de datos de la API
prota_sprite_load = pygame.image.load("main_pikachu.png").convert_alpha()
prota_sprite = pygame.transform.scale(prota_sprite_load, (100, 100))
malo_sprite_load = pygame.image.load("malo.jpg").convert_alpha()
malo_sprite = pygame.transform.scale(malo_sprite_load, (50, 50))

rayo_sprite_load = pygame.image.load("rayo.png").convert_alpha()
rayo_sprite = pygame.transform.scale(rayo_sprite_load, (100, 100))

electroTela_sprite_load = pygame.image.load("recursos\ElectroTela.png").convert_alpha()
electroTela_sprite = pygame.transform.scale(electroTela_sprite_load, (200, 200))

rayoATQ_sprite_load = pygame.image.load("recursos\RayoImpacto.png").convert_alpha()
rayoATQ_sprite = pygame.transform.scale(rayoATQ_sprite_load, (200, 200))