class Proyectil:
    def __init__(self, daño, rango, velocidad, sprite, x, y):
        self.daño = daño
        self.rango = rango
        self.velocidad = velocidad
        self.sprite = sprite
        self.x = x
        self.y = y
        self.rect = self.sprite.get_rect(center=(x, y))

    def moverse(self, posicion_enemiga):
        pass