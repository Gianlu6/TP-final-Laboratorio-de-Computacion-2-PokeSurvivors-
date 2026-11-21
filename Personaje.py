from Clases_Abs import Entidad

class Personaje(Entidad):
    def __init__(self, vida, ataque, defensa, x, y, image, grupo):
        super().__init__(vida, ataque, defensa, x, y, image, grupo)
        
    def atacar(self, Enemigo):
       pass
    
    
        
