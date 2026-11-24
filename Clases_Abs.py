from abc import ABC, abstractmethod
from constantes import *

class Entidad(pygame.sprite.Sprite, ABC):
    def __init__(self,x,y,sprite, grupo):
        super().__init__(grupo)
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

    #Getter de posicion
    def posicion(self):
        return (self.x,self.y)
    
    
    # def __init__(self, vida, ataque, defensa, x, y, sprite, grupo):    # x, y -> Coordenadas de posición
    #     super().__init__(grupo)         #Pygame
    #     self.__vida = vida
    #     self.ataque = ataque
    #     self.defensa = defensa
    #     self.x = x
    #     self.y = y
    #     self.estoy_vivo = True

    #     #Atributos específicos de la clase tipo pygame Sprite:
    #     self.image = sprite
    #     self.rect = self.image.get_rect (center=(x,y))
        

    # def moverse (self, dx, dy): #Recibe parámetros de cuanto hay que moverse
    #     self.x += dx
    #     self.y += dy
    #     self.rect.center = (self.x, self.y)
        
        
    # @abstractmethod
    # def atacar(self, vida_enemigo, defensa_enemigo):
    #     pass
   
    # def buscar_pos(self, Ent_Enemiga):
    #     return (Ent_Enemiga.x, Ent_Enemiga.y)

class SerVivo(Entidad):
    def __init__(self, vida_max, ataque, defensa, x, y, sprite, grupo):    # x, y -> Coordenadas de posición
            super().__init__(x,y,sprite,grupo)         
            self.vida_max = vida_max
            self.ataque = ataque
            self.defensa = defensa
            self.x = x
            self.y = y
            self.estoy_vivo = True

    
        
        
    @abstractmethod
    def atacar(self, vida_enemigo, defensa_enemigo):
        pass
    
    def buscar_pos(self, Ent_Enemiga):
        return (Ent_Enemiga.x, Ent_Enemiga.y)

#Entidad -> Movimiento/ataque/arma -> Impactrueno
class Movimiento(Entidad):
    def __init__(self, x, y, sprite, grupo, ataque_base, tiempo_recarga):
        super().__init__(x, y, sprite, grupo)
        self.ataque_base = ataque_base
        self.tiempo_recarga = tiempo_recarga

#Cada ciclo reloj se lo llama y ataca pasado su tiempo de recarga
    @abstractmethod
    def atacar(self):
        pass