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