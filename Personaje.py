from Clases_Abs import Entidad

class Personaje(Entidad):
    def __init__(self, vida, ataque, defensa, x, y, sprite):
        super().__init__(vida, ataque, defensa, x, y, sprite)
        
    def atacar(self, Enemigo):
       pass
    
    
        
