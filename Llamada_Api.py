import requests
import io


#Aca se traen los datos de la PokeAPI y se preparan para que las demas funciones y clases los usen
def obtenerPikachu ():
    encuesta= requests.get('https://pokeapi.co/api/v2/pokemon/25')
    if encuesta.status_code == 200:
        pikaDatos = encuesta.json()
        pikaSprite_URL = pikaDatos['sprites']['front_default']


        #Para mostrar imagen con pygame.load se descarga en memoria
        pikaImagen_r = requests.get(pikaSprite_URL)
        pikaImg_memoria = io.BytesIO(pikaImagen_r.content)
        return pikaImg_memoria
        
    else:
        print("No se pudo cargar API de PIKACHU")

#HAY QUE USAR HILOOOS PORQUE LA API ES PROCESOBLOQUEANTE
#Cargar API
#obtenerSprite (id) devuelve url
#obtener pokemon
