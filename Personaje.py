from Ataque import *
from Clases_Abs import SerVivo
from Enemigo import *
from sprites import *

class Personaje(SerVivo):
    def __init__(self, vida_max, ataque, defensa, tipo, x, y, image, grupo, rango,velocidad):
        super().__init__(vida_max, ataque, defensa, tipo, x, y, image, grupo,velocidad)
        self.vida = vida_max        #Esto fue privatizado y convertido con @property en la clase SerVivo
        self.rango = rango
        self.grupo = grupo

        self.nivel = 1
        self.xp = 0
        self.xp_max = 100
        
        self.rect = self.rect.inflate(-55, -55)
        self.rect.center = (x,y)

        #Instancia de los ataques
        self.inventario = [ElectroTela(self.x, self.y, electroTela_sprite, grupo, self.ataque,500,self.rango),
                         Placaje(self.x, self.y, pygame.Surface((0,0)), grupo, self.ataque,500,0),
                         Rayo(x,y,rayoATQ_sprite,grupo,self.ataque*0.2,500,1), 
                         Chispitas(self.x, self.y,rayito_sprite,self.grupo,self.ataque,500,600,self.velocidad)]


    def atacar(self):
        for movimiento in self.inventario:
            movimiento.atacar(self,enemigos)

    def actualizar_posicion_armas(self):    #Refresca pocicion de ataques que siguen a personaje y se desfasan por separacion
        for movimiento in self.inventario:
            if type(movimiento) is ElectroTela:
                dx = (self.x + movimiento.offset_x) - movimiento.x
                dy = (self.y + movimiento.offset_y) - movimiento.y
                movimiento.moverse(dx, dy)

    def ganar_xp(self, cantidad):
        self.xp += cantidad
        if self.xp >= self.xp_max:
            self.xp -= self.xp_max
            self.nivel += 1
            self.vida_max += 20
            for movimiento in self.inventario:
                movimiento.ataque_base += 5

    def mostrar_numeros_impacto(self, superficie, offset):
        barra_ancho = 50
        barra_alto = 6

        barra_x = self.rect.centerx - (barra_ancho // 2) - offset.x
        barra_y = self.rect.top - 25 - offset.y

        ratio = self.xp / self.xp_max
        ancho_actual = int(barra_ancho * ratio)

        bg_barra = pygame.Rect(barra_x, barra_y, barra_ancho, barra_alto)
        xp_barra = pygame.Rect(barra_x, barra_y, ancho_actual, barra_alto)

        pygame.draw.rect(superficie, NEGRO, bg_barra)
        pygame.draw.rect(superficie, AMARILLO, xp_barra)
        mostrar_texto(f"Nv.{self.nivel}", FUENTE_DANIO, BLANCO, barra_x, barra_y - 20)
