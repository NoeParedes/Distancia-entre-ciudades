import unittest
from main import Ciudad, ObtenerCoordenadasAPI, calcular_distancia

class PruebasDistanciaCiudades(unittest.TestCase):

    def test_caso_exito(self):
        """
        Prueba el caso de éxito donde se calculan correctamente las distancias entre dos ciudades existentes.
        """
        ciudad1 = Ciudad("Mexico", "Mexico City")
        ciudad2 = Ciudad("Japan", "Tokyo")

        obtener_coordenadas = ObtenerCoordenadasAPI()
        coord1 = obtener_coordenadas.obtener_coordenadas(ciudad1)
        coord2 = obtener_coordenadas.obtener_coordenadas(ciudad2)

        if coord1 and coord2:
            distancia = calcular_distancia(coord1, coord2)
            self.assertGreater(distancia, 9000)  # Verificar que la distancia sea mayor a 9000 km

    def test_ciudad_no_existente(self):
        """
        Prueba el caso extremo donde una de las ciudades no existe.
        """
        ciudad1 = Ciudad("Mexico", "Mexico City")
        ciudad2 = Ciudad("Pais Inexistente", "Ciudad Inexistente")

        obtener_coordenadas = ObtenerCoordenadasAPI()
        coord1 = obtener_coordenadas.obtener_coordenadas(ciudad1)
        coord2 = obtener_coordenadas.obtener_coordenadas(ciudad2)

        self.assertIsNone(coord2)

    def test_misma_ciudad(self):
        """
        Prueba el caso extremo donde se ingresan la misma ciudad dos veces.
        """
        ciudad1 = Ciudad("Mexico", "Mexico City")
        ciudad2 = Ciudad("Mexico", "Mexico City")

        obtener_coordenadas = ObtenerCoordenadasAPI()
        coord1 = obtener_coordenadas.obtener_coordenadas(ciudad1)
        coord2 = obtener_coordenadas.obtener_coordenadas(ciudad2)

        if coord1 and coord2:
            distancia = calcular_distancia(coord1, coord2)
            self.assertEqual(distancia, 0.0)

if __name__ == '__main__':
    unittest.main()