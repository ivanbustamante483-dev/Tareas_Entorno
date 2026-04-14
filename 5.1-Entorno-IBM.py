import random
import time


class Pixel:
    def __init__(self, pixel_id: int, face: bool, intensidad: float):
        self.id = pixel_id
        self.face = face
        self.intensidad = intensidad

    def __eq__(self, other):
        if not isinstance(other, Pixel):
            return False
        return (
            self.id == other.id
            and self.face == other.face
            and self.intensidad == other.intensidad
        )

    def __hash__(self):
        return hash((self.id, self.face, self.intensidad))

    def __repr__(self):
        return f"Pixel(id={self.id}, face={self.face}, intensidad={self.intensidad})"


def generar_pixeles(cantidad: int = 10000):
    lista_pixeles = []

    # Elegimos una posición aleatoria para el único pixel especial
    posicion_especial = random.randint(0, cantidad - 1)

    for i in range(cantidad):
        if i == posicion_especial:
            pixel = Pixel(i, True, 1.0)
        else:
            face = random.choice([True, False])

            # Evitamos crear otro pixel con intensidad 1.0 y face True
            intensidad = round(random.uniform(0.0, 0.9999), 4)

            # Aunque salga face=True, como intensidad nunca será 1.0,
            # no podrá repetirse el pixel especial
            pixel = Pixel(i, face, intensidad)

        lista_pixeles.append(pixel)

    return lista_pixeles


def buscar_pixel_lista(lista):
    inicio = time.time()

    encontrados = [
        pixel for pixel in lista
        if pixel.face is True and pixel.intensidad == 1.0
    ]

    fin = time.time()
    tiempo = fin - inicio

    return encontrados, tiempo


def buscar_pixel_set(conjunto):
    inicio = time.time()

    encontrados = {
        pixel for pixel in conjunto
        if pixel.face is True and pixel.intensidad == 1.0
    }

    fin = time.time()
    tiempo = fin - inicio

    return encontrados, tiempo


def mostrar_resultado(nombre_estructura, encontrados, tiempo):
    print(f"=== {nombre_estructura} ===")
    print(f"Encontrado: {len(encontrados) > 0}")
    print(f"Tiempo: {tiempo:.10f} segundos")

    if len(encontrados) == 1:
        print("Único objeto")
    else:
        print("No se cumple que exista un único objeto")

    if tiempo > 0.0001:
        print("PEATÓN MUERTO")

    print()


def main():
    # Generar los 10.000 píxeles
    lista_pixeles = generar_pixeles(10000)

    # Guardarlos también en un set
    set_pixeles = set(lista_pixeles)

    # Buscar en lista
    encontrados_lista, tiempo_lista = buscar_pixel_lista(lista_pixeles)

    # Buscar en set
    encontrados_set, tiempo_set = buscar_pixel_set(set_pixeles)

    # Mostrar resultados
    mostrar_resultado("LISTA", encontrados_lista, tiempo_lista)
    mostrar_resultado("SET", encontrados_set, tiempo_set)


if __name__ == "__main__":
    main()