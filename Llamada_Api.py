import requests
import io
import time
import random
import threading
import queue
import pygame

#Los datos de pokemon descargados en la API se guardan en un diccionario para ahorrar tiempo de carga cuando toca de nuevo el pokemon o se reinicia la partida
Cache_pokemons = {} 

def obtener_pokemon(id):
    id_sorteo = id
    if id_sorteo in Cache_pokemons:     #Si el pokemon que toca ya toco antes se llama al cache para retornar rapido el diccionario
        return Cache_pokemons[id_sorteo]
    try:
        req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id_sorteo}", timeout=5)
        req.raise_for_status()
        dicc = req.json()

        poke_dato = {'nombre':dicc['name'],'ataque':dicc['stats'][1]['base_stat'],'defensa':dicc['stats'][2]['base_stat'],
                     'vida':dicc['stats'][0]['base_stat'],'velocidad':dicc['stats'][5]['base_stat'],'tipo':dicc['types'],
                     'altura':dicc['height'], 'sprite_url':dicc['sprites']['front_default']}

        #Extraer imagen sprite de la URL y cargarla en memoria
        img_req = requests.get(poke_dato['sprite_url'], timeout=5)
        img_req.raise_for_status()
        imagen_byte = io.BytesIO(img_req.content)

        poke_imagen = pygame.image.load(imagen_byte)

        poke_dato['sprite'] = poke_imagen
        #Como el metodo .convert_alpha() NO es thread safe entonces se aplicara mas adelante
        #NOTA: Pygame gráfico en general NO es thread safe

        return poke_dato
    
    except Exception as e:  #Exepsion ya sea de timeout o de HTTP response status
        print(f"Error tipo {e}")
        return None


def hilo_oleada(cola_datos, evento_terminacion):
    while not evento_terminacion.is_set():  #Mientras no se dispare el evento de terminacion de hilos
        ids_tanda = [random.randint(1,151) for i in range (5)]      # Sorteo de 5 IDs
        nueva_tanda = []

        for p in ids_tanda:
            if evento_terminacion.is_set(): #Mientras no se dispare el evento de terminacion de hilos
                return
            datos = obtener_pokemon(p)  #Llamo a la funcion que trae datos de la API
            if datos:   #Si datos no esta vacio, mete el resultado en la lista
                nueva_tanda.append(datos)

        if nueva_tanda:     #Si hay algo en la lista nueva_tanda
            cola_datos.put(nueva_tanda)

        for i in range(120):        #Este seria el "delay de 1 minuto" por oleada
            if evento_terminacion.is_set():
                return
            time.sleep(0.5)