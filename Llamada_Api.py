import requests
import io
import time


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


def generador_pokemones(inicio,fin):
    for id in range(inicio, fin+1):
        yield f"https://pokeapi.co/api/v2/pokemon/{id}"


def obtener_pokemon(url):
    while True:
        try:
            req = requests.get(url,timeout=3)
            req.raise_for_status()
            break
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:           #Codigo error 'Too Many Request', llamar a la API con demaciados trabajadores en poco tiempo
                time.sleep(1)
                continue
        except requests.Timeout:
            print("Tiempo de espera agotado")
            time.sleep(1)
            continue

    pokeAPI = req.json()
    poke_datos = {'nombre':pokeAPI['name'],'sprite_url':pokeAPI['sprites']['front_default'],'altura':pokeAPI['height']//10}
    return poke_datos

def cargar_API_sprite (pokedicc):
    poke_imagen=requests.get(pokedicc['sprite_url'])
    pokeImage_memoria = io.BytesIO(poke_imagen.content)
    return pokeImage_memoria
