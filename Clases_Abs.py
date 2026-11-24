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
            self.__vida = vida_max
            self.ataque = ataque
            self.defensa = defensa
            self.x = x
            self.y = y
            self.estoy_vivo = True

    #Property es un decorador intergrado que convierte un metodo getter de un atributo privado
    #en un atributo de solo lectura (o un método sin paréntesis con el mismo nombre que el atributo privado)
    
    #El getter de vida se llama asi:
        #prota.vida 
    @property                   
    def vida(self):
        return self.__vida

    #El decorador .setter toma el nombre del atributo privado y cuando lo llamas 
    # para editarlo como un atributo normal, en realidad pasa por el método setter validador

    #El setter de vida se llama asi:
    # prota.vida = danio
    @vida.setter                                  
    def vida(self, danio):
        if danio >= self.__vida:
            self.__vida = 0
        else:
            self.__vida -= danio
        
        
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
#Bola voltio: Protectil? Varita de fuego? El ataque sube en base a la velocidad
#Mega-punch, headbutt: Normales
#Volt Switch: Eléctrico. Pega y cambia, poco daño
#Proyectiles?

#Modificadores pasivos para evolucion

#Enemigo. Ataques segun tipo (daño de contacto y proyectiles):
#Fuego y agua: proyectiles, fuego hace mas daño, agua lanza mas proyectiles
#Lucha, acero, roca: Daño por contacto, mínimo pero varios por segundo en lucha y acero hace mas daño pero el cooldown es mas largo
#Tierra: daño de contacto o area con terremotos

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