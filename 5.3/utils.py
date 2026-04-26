"""
utils.py - Módulo de funciones auxiliares
=========================================
Contiene las funciones de obtención de datos desde la API de la ISS
y el procesamiento de esos datos en dos versiones:
  - no_optimizada: intencionadamente ineficiente
  - optimizada: eficiente y limpia
"""

import time
import requests
import math
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
#  OBTENCIÓN DE DATOS DESDE LA API
# ═══════════════════════════════════════════════════════════════

def obtener_posicion_iss():
    """
    Obtiene la posición actual de la Estación Espacial Internacional.

    Realiza una petición GET a la API pública 'Open Notify' que devuelve
    la latitud y longitud actuales de la ISS en tiempo real.

    Parámetros:
        Ninguno.

    Retorna:
        dict: Diccionario con las claves:
            - 'latitud'   (float): Latitud actual de la ISS.
            - 'longitud'  (float): Longitud actual de la ISS.
            - 'timestamp' (int):   Marca de tiempo UNIX de la lectura.
            - 'exito'     (bool):  True si la petición fue exitosa.
            - 'error'     (str):   Mensaje de error si falló la petición.

    Ejemplo de uso:
        >>> datos = obtener_posicion_iss()
        >>> print(datos['latitud'], datos['longitud'])
    """
    url = "http://api.open-notify.org/iss-now.json"
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()
        return {
            "latitud": float(datos["iss_position"]["latitude"]),
            "longitud": float(datos["iss_position"]["longitude"]),
            "timestamp": datos["timestamp"],
            "exito": True,
            "error": ""
        }
    except requests.RequestException as e:
        return {
            "latitud": 0.0,
            "longitud": 0.0,
            "timestamp": 0,
            "exito": False,
            "error": str(e)
        }


def obtener_astronautas():
    """
    Obtiene la lista de astronautas actualmente en el espacio.

    Realiza una petición GET a la API pública 'Open Notify' que devuelve
    los nombres y naves de los astronautas en misión.

    Parámetros:
        Ninguno.

    Retorna:
        dict: Diccionario con las claves:
            - 'cantidad'    (int):  Número total de astronautas.
            - 'astronautas' (list): Lista de dicts con 'nombre' y 'nave'.
            - 'exito'       (bool): True si la petición fue exitosa.
            - 'error'       (str):  Mensaje de error si falló la petición.

    Ejemplo de uso:
        >>> datos = obtener_astronautas()
        >>> for a in datos['astronautas']:
        ...     print(a['nombre'], '-', a['nave'])
    """
    url = "http://api.open-notify.org/astros.json"
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()
        astronautas = [
            {"nombre": p["name"], "nave": p["craft"]}
            for p in datos["people"]
        ]
        return {
            "cantidad": datos["number"],
            "astronautas": astronautas,
            "exito": True,
            "error": ""
        }
    except requests.RequestException as e:
        return {
            "cantidad": 0,
            "astronautas": [],
            "exito": False,
            "error": str(e)
        }


# ═══════════════════════════════════════════════════════════════
#  VERSIÓN NO OPTIMIZADA - Procesamiento ineficiente
# ═══════════════════════════════════════════════════════════════

def procesar_datos_no_optimizado(posicion, astronautas):
    """
    Procesa los datos de la ISS de forma INTENCIONADAMENTE INEFICIENTE.

    Esta función realiza el mismo trabajo que su versión optimizada,
    pero utiliza prácticas de programación pobres a propósito:
      - Bucles innecesarios para buscar valores.
      - Listas temporales redundantes.
      - Cálculos repetidos dentro de bucles.
      - Concatenación de cadenas ineficiente.

    Parámetros:
        posicion (dict): Diccionario devuelto por obtener_posicion_iss().
        astronautas (dict): Diccionario devuelto por obtener_astronautas().

    Retorna:
        dict: Diccionario con las claves:
            - 'resumen'        (str):   Texto formateado con toda la información.
            - 'hemisferio_lat' (str):   'Norte' o 'Sur'.
            - 'hemisferio_lon' (str):   'Este' u 'Oeste'.
            - 'distancia_origen' (float): Distancia al punto (0,0).
            - 'nombres_astronautas' (list): Lista de nombres.
            - 'naves_unicas'  (list): Lista de naves sin duplicados.
            - 'nombre_mas_largo' (str): El nombre de astronauta más largo.
            - 'estadisticas'  (dict): Estadísticas calculadas.
    """
    latitud = posicion["latitud"]
    longitud = posicion["longitud"]
    lista_astronautas = astronautas["astronautas"]

    # --- Determinar hemisferio con lógica redundante ---
    hemisferio_lat = ""
    hemisferio_lon = ""
    for i in range(1):  # Bucle innecesario de una sola iteración
        if latitud >= 0:
            hemisferio_lat = "Norte"
        if latitud < 0:
            hemisferio_lat = "Sur"
        if longitud >= 0:
            hemisferio_lon = "Este"
        if longitud < 0:
            hemisferio_lon = "Oeste"

    # --- Calcular distancia al origen de forma repetitiva ---
    distancia = 0.0
    for i in range(5):  # Repite el cálculo 5 veces innecesariamente
        distancia = math.sqrt(latitud * latitud + longitud * longitud)

    # --- Extraer nombres con bucle manual ---
    nombres = []
    for i in range(len(lista_astronautas)):
        nombre = lista_astronautas[i]["nombre"]
        nombres.append(nombre)

    # --- Buscar naves únicas con bucle anidado ---
    naves_unicas = []
    for astro in lista_astronautas:
        nave = astro["nave"]
        encontrada = False
        for n in naves_unicas:
            if n == nave:
                encontrada = True
        if not encontrada:
            naves_unicas.append(nave)

    # --- Buscar el nombre más largo con variable temporal ---
    nombre_mas_largo = ""
    longitud_max = 0
    for nombre in nombres:
        longitud_nombre = 0
        for caracter in nombre:  # Contar caracteres manualmente
            longitud_nombre += 1
        if longitud_nombre > longitud_max:
            longitud_max = longitud_nombre
            nombre_mas_largo = nombre

    # --- Calcular estadísticas de longitudes de nombres ---
    longitudes = []
    for nombre in nombres:
        contador = 0
        for c in nombre:
            contador += 1
        longitudes.append(contador)

    # Calcular suma manualmente
    suma_longitudes = 0
    for lon in longitudes:
        suma_longitudes = suma_longitudes + lon

    # Calcular media manualmente
    media_longitudes = 0
    if len(longitudes) > 0:
        media_longitudes = suma_longitudes / len(longitudes)

    # Calcular mínimo manualmente
    minimo = 999999
    for lon in longitudes:
        if lon < minimo:
            minimo = lon

    # Calcular máximo manualmente
    maximo = 0
    for lon in longitudes:
        if lon > maximo:
            maximo = lon

    estadisticas = {
        "total_astronautas": len(nombres),
        "total_naves": len(naves_unicas),
        "media_longitud_nombre": round(media_longitudes, 2),
        "nombre_mas_corto": minimo,
        "nombre_mas_largo_len": maximo,
    }

    # --- Construir resumen con concatenación ineficiente ---
    resumen = ""
    resumen = resumen + "═══ POSICIÓN DE LA ISS ═══\n"
    resumen = resumen + "Latitud:  " + str(round(latitud, 4)) + "°\n"
    resumen = resumen + "Longitud: " + str(round(longitud, 4)) + "°\n"
    resumen = resumen + "Hemisferio: " + hemisferio_lat + " / " + hemisferio_lon + "\n"
    resumen = resumen + "Distancia al origen: " + str(round(distancia, 2)) + "°\n"
    resumen = resumen + "\n═══ ASTRONAUTAS EN EL ESPACIO ═══\n"
    resumen = resumen + "Total: " + str(astronautas["cantidad"]) + "\n"
    for nombre in nombres:
        resumen = resumen + "  • " + nombre + "\n"
    resumen = resumen + "\nNaves: " + ", ".join(naves_unicas) + "\n"
    resumen = resumen + "Nombre más largo: " + nombre_mas_largo + "\n"
    resumen = resumen + "\n═══ ESTADÍSTICAS ═══\n"
    resumen = resumen + "Media longitud nombres: " + str(estadisticas["media_longitud_nombre"]) + "\n"
    resumen = resumen + "Nombre más corto (chars): " + str(estadisticas["nombre_mas_corto"]) + "\n"
    resumen = resumen + "Nombre más largo (chars): " + str(estadisticas["nombre_mas_largo_len"]) + "\n"

    return {
        "resumen": resumen,
        "hemisferio_lat": hemisferio_lat,
        "hemisferio_lon": hemisferio_lon,
        "distancia_origen": distancia,
        "nombres_astronautas": nombres,
        "naves_unicas": naves_unicas,
        "nombre_mas_largo": nombre_mas_largo,
        "estadisticas": estadisticas,
    }


# ═══════════════════════════════════════════════════════════════
#  VERSIÓN OPTIMIZADA - Procesamiento eficiente
# ═══════════════════════════════════════════════════════════════

def procesar_datos_optimizado(posicion, astronautas):
    """
    Procesa los datos de la ISS de forma EFICIENTE y LIMPIA.

    Aplica buenas prácticas de programación:
      - Operador ternario para decisiones simples.
      - Comprensiones de lista (list comprehensions).
      - Funciones integradas: max(), min(), sum(), len(), set().
      - f-strings para construir cadenas.
      - Un solo recorrido cuando es posible.

    Parámetros:
        posicion (dict): Diccionario devuelto por obtener_posicion_iss().
        astronautas (dict): Diccionario devuelto por obtener_astronautas().

    Retorna:
        dict: Diccionario con las mismas claves que la versión no optimizada:
            - 'resumen', 'hemisferio_lat', 'hemisferio_lon',
              'distancia_origen', 'nombres_astronautas', 'naves_unicas',
              'nombre_mas_largo', 'estadisticas'.
    """
    lat = posicion["latitud"]
    lon = posicion["longitud"]
    lista = astronautas["astronautas"]

    # Hemisferio con operador ternario
    hemisferio_lat = "Norte" if lat >= 0 else "Sur"
    hemisferio_lon = "Este" if lon >= 0 else "Oeste"

    # Distancia al origen — un solo cálculo
    distancia = math.hypot(lat, lon)

    # Nombres con list comprehension
    nombres = [a["nombre"] for a in lista]

    # Naves únicas con set
    naves_unicas = list({a["nave"] for a in lista})

    # Nombre más largo con max() y key
    nombre_mas_largo = max(nombres, key=len) if nombres else ""

    # Estadísticas con funciones integradas
    longitudes = [len(n) for n in nombres]
    estadisticas = {
        "total_astronautas": len(nombres),
        "total_naves": len(naves_unicas),
        "media_longitud_nombre": round(sum(longitudes) / len(longitudes), 2) if longitudes else 0,
        "nombre_mas_corto": min(longitudes) if longitudes else 0,
        "nombre_mas_largo_len": max(longitudes) if longitudes else 0,
    }

    # Resumen con f-strings y join
    lista_nombres = "\n".join(f"  • {n}" for n in nombres)
    resumen = (
        f"═══ POSICIÓN DE LA ISS ═══\n"
        f"Latitud:  {round(lat, 4)}°\n"
        f"Longitud: {round(lon, 4)}°\n"
        f"Hemisferio: {hemisferio_lat} / {hemisferio_lon}\n"
        f"Distancia al origen: {round(distancia, 2)}°\n"
        f"\n═══ ASTRONAUTAS EN EL ESPACIO ═══\n"
        f"Total: {astronautas['cantidad']}\n"
        f"{lista_nombres}\n"
        f"\nNaves: {', '.join(naves_unicas)}\n"
        f"Nombre más largo: {nombre_mas_largo}\n"
        f"\n═══ ESTADÍSTICAS ═══\n"
        f"Media longitud nombres: {estadisticas['media_longitud_nombre']}\n"
        f"Nombre más corto (chars): {estadisticas['nombre_mas_corto']}\n"
        f"Nombre más largo (chars): {estadisticas['nombre_mas_largo_len']}\n"
    )

    return {
        "resumen": resumen,
        "hemisferio_lat": hemisferio_lat,
        "hemisferio_lon": hemisferio_lon,
        "distancia_origen": distancia,
        "nombres_astronautas": nombres,
        "naves_unicas": naves_unicas,
        "nombre_mas_largo": nombre_mas_largo,
        "estadisticas": estadisticas,
    }


# ═══════════════════════════════════════════════════════════════
#  UTILIDADES AUXILIARES
# ═══════════════════════════════════════════════════════════════

def formatear_hora(timestamp_unix=None):
    """
    Convierte un timestamp UNIX a una cadena legible HH:MM:SS.

    Si no se proporciona timestamp, usa la hora actual del sistema.

    Parámetros:
        timestamp_unix (int, optional): Marca de tiempo UNIX.
            Si es None, se usa la hora actual.

    Retorna:
        str: Hora formateada como 'HH:MM:SS'.

    Ejemplo:
        >>> formatear_hora(1713700000)
        '18:26:40'
        >>> formatear_hora()
        '19:30:15'  # (hora actual)
    """
    if timestamp_unix:
        return datetime.fromtimestamp(timestamp_unix).strftime("%H:%M:%S")
    return datetime.now().strftime("%H:%M:%S")


def obtener_docstrings_modulo():
    """
    Recopila los docstrings de todas las funciones públicas de este módulo.

    Recorre el módulo actual y extrae el nombre y docstring de cada función
    que no empiece por '_'.

    Parámetros:
        Ninguno.

    Retorna:
        list[tuple]: Lista de tuplas (nombre_funcion, docstring).
            Si la función no tiene docstring, se indica 'Sin documentación'.
    """
    import sys
    import inspect
    modulo = sys.modules[__name__]
    resultado = []
    for nombre, obj in inspect.getmembers(modulo, inspect.isfunction):
        if not nombre.startswith("_"):
            doc = inspect.getdoc(obj) or "Sin documentación."
            resultado.append((nombre, doc))
    return resultado
