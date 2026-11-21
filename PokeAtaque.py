import math
import pygame
from PokeSurv import rayo_sprite

# ---------- PROYECTILES ----------
class Proyectil:
    """Base: vuela en línea recta hacia un punto."""
    def __init__(self, velocidad, sprite, x, y, objetivo, daño):
        self.velocidad = velocidad
        self.sprite = sprite
        self.x, self.y = x, y
        self.objetivo = objetivo
        self.daño = daño
        self.activo = True
        self.rect = sprite.get_rect(center=(x, y))

    def moverse(self):
        dx = self.objetivo[0] - self.x
        dy = self.objetivo[1] - self.y
        dist = math.hypot(dx, dy)
        if dist <= self.velocidad:
            self.x, self.y = self.objetivo
            self.activo = False
        else:
            self.x += dx / dist * self.velocidad
            self.y += dy / dist * self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, self.rect)


class Rayo(Proyectil):
    pass


# ---------- ATAQUES ----------
class PokeAtaque:
    nombre = "Ataque"
    multiplicador = 1.0
    velocidad = 8
    clase_proyectil = Proyectil
    sprite = None  # se carga una vez

    def lanzar(self, personaje, posicion_enemigo):
        return self.clase_proyectil(
            velocidad=self.velocidad,
            sprite=self.sprite,
            x=personaje.x,
            y=personaje.y,
            objetivo=posicion_enemigo,
            daño=personaje.daño * self.multiplicador,
        )


class Lanzarayos(PokeAtaque):
    nombre = "Lanzarayos"
    multiplicador = 0.0
    velocidad = 4
    clase_proyectil = Rayo
    sprite = rayo_sprite

