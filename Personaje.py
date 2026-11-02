import pygame       #Para el método de mostrar el personaje en pantalla
import constantes


class miPokemon:
    def __init__(self, x,y):    # x, y -> Coordenadas de posición
        self.x = x
        self.y= y
        self.radio = 20         #Radio porque va a ser un cículo

    def dibujar_pj (self, pantalla):                        #Los métodos de dibujar reciben el pygamen objeto "ventana"/pantalla
        pygame.draw.circle (pantalla, constantes.ROJO, 
                          (self.x, self.y), self.radio)
    # Creamos un círculo con color rojo, posición y tamaño tanto eje x como eje y.

    def moverse (self, dx, dy): #Recibe parámetros de cuanto hay que moverse
        self.x += dx
        self.y += dy
