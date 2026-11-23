from abc import ABC, abstractmethod
from constantes import *

class Entidad(pygame.sprite.Sprite, ABC):
    def __init__(self, vida, ataque, defensa, x, y, sprite, grupo):    # x, y -> Coordenadas de posición
        super().__init__(grupo)         #Pygame
        self.__vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.x = x
        self.y = y
        self.estoy_vivo = True

        #Atributos específicos de la clase tipo pygame Sprite:
        self.image = sprite
        self.rect = self.image.get_rect (center=(x,y))


    def moverse (self, dx, dy): #Recibe parámetros de cuanto hay que moverse
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)
        
    @abstractmethod
    def atacar(self, vida_enemigo, defensa_enemigo):
        pass
   
    def buscar_pos(self, Ent_Enemiga):
        return (Ent_Enemiga.x, Ent_Enemiga.y)



#Base de ataques?
#Rayo: Tiene mas daño que impactrueno
#Impactrueno: rayos caen aleatoreamente a los enemigos (anillo de relámpago de VS)
#Cola férrea, ataque normal para los de tierra (látigo de VS)
#Placaje: Ataque normal, daño de contacto
#Placaje eléctrico: Ataque eléctrico, daño de contacto (mas daño que rayo, deja estela de daño?)
#Electro tela/red: escudo electrico (ajo VS)
#Bola voltio
#Proyectiles?

#Enemigo. Ataques segun tipo (daño de contacto y proyectiles):
#Fuego y agua: proyectiles, fuego hace mas daño, agua lanza mas proyectiles
#Lucha, acero, roca: Daño por contacto, mínimo pero varios por segundo en lucha y acero hace mas daño pero el cooldown es mas largo
#Tierra: daño de contacto o area con terremotos



class Ataque (pygame.sprite.Sprite, ABC):
    def __init__(self, ataque, velocidad_ataque, area, cantidad, grupo):
        super().__init__(grupo)