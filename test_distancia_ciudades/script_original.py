import csv
import requests
import math
from abc import ABC, abstractmethod

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
        print(f"No se encontraron coordenadas para {ciudad.nombre_ciudad}, {ciudad.nombre_pais}\n")
        return None

# Implementación usando API
class ObtenerCoordenadasAPI(ObtenerCoordenadasInterface):
    def obtener_coordenadas(self, ciudad):
        response = requests.get(f'https://nominatim.openstreetmap.org/search?q={ciudad.nombre_ciudad},{ciudad.nombre_pais}&format=json')
        data = response.json()
        if data:
            return Coordenada(float(data[0]['lat']), float(data[0]['lon']))
        print(f"No se encontraron coordenadas para {ciudad.nombre_ciudad}, {ciudad.nombre_pais}")
        return None

def calcular_distancia(coord1, coord2):
    if coord1.latitud == coord2.latitud and coord1.longitud == coord2.longitud:
        print("\nSe ingresó la misma ciudad dos veces.\n")
        return 0.0

    R = 6371  # radio de la Tierra en kilómetros
    lat1, lon1 = math.radians(coord1.latitud), math.radians(coord1.longitud)
    lat2, lon2 = math.radians(coord2.latitud), math.radians(coord2.longitud)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia

def main():
    # Definir las ciudades
    ciudad1 = Ciudad("Mexico", "Mexico City")
    ciudad2 = Ciudad("Japan", "Tokyo")

    # Seleccionar la implementación de coordenadas
    obtener_coordenadas = ObtenerCoordenadasAPI()

    # Obtener las coordenadas de ambas ciudades
    coord1 = obtener_coordenadas.obtener_coordenadas(ciudad1)
    coord2 = obtener_coordenadas.obtener_coordenadas(ciudad2)

    # Calcular la distancia
    distancia = calcular_distancia(coord1, coord2)
    if distancia is not None:
        print(f'La distancia entre {ciudad1.nombre_ciudad}, {ciudad1.nombre_pais} y {ciudad2.nombre_ciudad}, {ciudad2.nombre_pais} es {distancia:.2f} km\n')

main()