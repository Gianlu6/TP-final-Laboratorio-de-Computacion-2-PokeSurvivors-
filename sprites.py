import pygame

#INICIALIZANDO SPRITES
prota_sprite_load = pygame.image.load("sprites/main_pikachu.png").convert_alpha()
prota_sprite = pygame.transform.scale(prota_sprite_load, (100, 100))
malo_sprite_load = pygame.image.load("sprites/malo.jpg").convert_alpha()
malo_sprite = pygame.transform.scale(malo_sprite_load, (50, 50))

electroTela_sprite_load = pygame.image.load("recursos/ElectroTela.png").convert_alpha()
electroTela_sprite = pygame.transform.scale(electroTela_sprite_load, (200, 200))

rayoATQ_sprite_load = pygame.image.load("recursos/RayoImpacto.png").convert_alpha()
rayoATQ_sprite = pygame.transform.scale(rayoATQ_sprite_load, (100, 1000))

rayito_sprite_load = pygame.image.load("recursos/Proyectil_Rayo.png").convert_alpha()
rayito_sprite = pygame.transform.scale(rayito_sprite_load, (30, 30))
