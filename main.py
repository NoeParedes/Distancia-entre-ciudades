import csv
import requests
import math
from abc import ABC, abstractmethod
from requests.exceptions import RequestException, HTTPError, JSONDecodeError

# Definir la clase Coordenada
class Coordenada:
    def __init__(self, latitud, longitud):
        self.latitud = latitud
        self.longitud = longitud

# Definir la clase Ciudad
class Ciudad:
    def __init__(self, nombre_pais, nombre_ciudad):
        self.nombre_pais = nombre_pais
        self.nombre_ciudad = nombre_ciudad

class ObtenerCoordenadasInterface(ABC):
    @abstractmethod
    def obtener_coordenadas(self, ciudad):
        pass

# Implementación usando CSV
class ObtenerCoordenadasCSV(ObtenerCoordenadasInterface):
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def obtener_coordenadas(self, ciudad):
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['city'].lower() == ciudad.nombre_ciudad.lower() and row['country'].lower() == ciudad.nombre_pais.lower():
                    return Coordenada(float(row['lat']), float(row['lng']))
        return None

# Implementación usando API
class ObtenerCoordenadasAPI(ObtenerCoordenadasInterface):
    def obtener_coordenadas(self, ciudad):
        try:
            response = requests.get(f'https://nominatim.openstreetmap.org/search?q={ciudad.nombre_ciudad},{ciudad.nombre_pais}&format=json')
            response.raise_for_status()  # Lanzar una excepción si la respuesta no es exitosa
            data = response.json()
            if data:
                return Coordenada(float(data[0]['lat']), float(data[0]['lon']))
        except RequestException as e:
            print(f"Error al obtener coordenadas: {e}")
        except (IndexError, KeyError, ValueError, JSONDecodeError) as e:
            print(f"Error en los datos de la API: {e}")
        return None

# Implementación Mock

def calcular_distancia(coord1, coord2):
    R = 6371  #radio de la Tierra en kilómetros
    lat1, lon1 = math.radians(coord1.latitud), math.radians(coord1.longitud)
    lat2, lon2 = math.radians(coord2.latitud), math.radians(coord2.longitud)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distancia = R * c
    return distancia

def ciudades_mas_cercanas(ciudad1, ciudad2, ciudad3):
    # Obtener coordenadas de las ciudades usando CSV
    obtener_coordenadas_csv = ObtenerCoordenadasCSV('worldcities.csv')
    coord1_csv = obtener_coordenadas_csv.obtener_coordenadas(ciudad1)
    coord2_csv = obtener_coordenadas_csv.obtener_coordenadas(ciudad2)
    coord3_csv = obtener_coordenadas_csv.obtener_coordenadas(ciudad3)

    # Obtener coordenadas de las ciudades usando API
    obtener_coordenadas_api = ObtenerCoordenadasAPI()
    coord1_api = obtener_coordenadas_api.obtener_coordenadas(ciudad1)
    coord2_api = obtener_coordenadas_api.obtener_coordenadas(ciudad2)
    coord3_api = obtener_coordenadas_api.obtener_coordenadas(ciudad3)

    # Calcular distancias entre las ciudades
    if coord1_csv and coord2_csv and coord3_csv:
        distancia_csv = [
            calcular_distancia(coord1_csv, coord2_csv),
            calcular_distancia(coord1_csv, coord3_csv),
            calcular_distancia(coord2_csv, coord3_csv)
        ]
    else:
        print("No se pudieron obtener las coordenadas de una o varias ciudades desde el CSV.")
        return None, None

    if coord1_api and coord2_api and coord3_api:
        distancia_api = [
            calcular_distancia(coord1_api, coord2_api),
            calcular_distancia(coord1_api, coord3_api),
            calcular_distancia(coord2_api, coord3_api)
        ]
    else:
        print("No se pudieron obtener las coordenadas de una o varias ciudades desde la API.")
        return None, None

    # Determinar cuáles dos ciudades están más cerca
    min_dist_csv = min(distancia_csv)
    min_dist_api = min(distancia_api)
    if min_dist_csv <= min_dist_api:
        if distancia_csv.index(min_dist_csv) == 0:
            return ciudad1, ciudad2
        elif distancia_csv.index(min_dist_csv) == 1:
            return ciudad1, ciudad3
        else:
            return ciudad2, ciudad3
    else:
        if distancia_api.index(min_dist_api) == 0:
            return ciudad1, ciudad2
        elif distancia_api.index(min_dist_api) == 1:
            return ciudad1, ciudad3
        else:
            return ciudad2, ciudad3

def main():
    # Definir las ciudades
    ciudad1 = Ciudad("Peru", "Lima")
    ciudad2 = Ciudad("Colombia", "Bogotá")
    ciudad3 = Ciudad("Argentina", "Buenos Aires")

    # Determinar las dos ciudades más cercanas
    ciudad_cercana1, ciudad_cercana2 = ciudades_mas_cercanas(ciudad1, ciudad2, ciudad3)

    if ciudad_cercana1 and ciudad_cercana2:
        print(f"Las dos ciudades más cercanas son {ciudad_cercana1.nombre_ciudad}, {ciudad_cercana1.nombre_pais} y {ciudad_cercana2.nombre_ciudad}, {ciudad_cercana2.nombre_pais}")
    else:
        print("No se pudieron determinar las dos ciudades más cercanas.")

if __name__ == "__main__":
    main()
