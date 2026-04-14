import random
import time

CANTIDAD_FINCAS = 100000
MIN_KG = 50
MAX_KG = 500
INCREMENTO = 1.10


# -----------------------------------
# 1. LISTA TRADICIONAL
# -----------------------------------
inicio = time.time()

abonos_lista = []
for _ in range(CANTIDAD_FINCAS):
    abonos_lista.append(random.randint(MIN_KG, MAX_KG))

total_lista = 0
for kg in abonos_lista:
    total_lista += kg * INCREMENTO

fin = time.time()
tiempo_lista = fin - inicio


# -----------------------------------
# 2. LISTA POR COMPRENSIÓN
# -----------------------------------
inicio = time.time()

abonos_comprension = [random.randint(MIN_KG, MAX_KG) for _ in range(CANTIDAD_FINCAS)]
total_comprension = sum([kg * INCREMENTO for kg in abonos_comprension])

fin = time.time()
tiempo_comprension = fin - inicio


# -----------------------------------
# 3. GENERADOR
# -----------------------------------
inicio = time.time()

generador_abonos = (random.randint(MIN_KG, MAX_KG) * INCREMENTO for _ in range(CANTIDAD_FINCAS))
total_generador = sum(generador_abonos)

fin = time.time()
tiempo_generador = fin - inicio


# -----------------------------------
# RESULTADOS
# -----------------------------------
print("=== LISTA TRADICIONAL ===")
print(f"Total: {total_lista:.2f} kg")
print(f"Tiempo: {tiempo_lista:.6f} segundos\n")

print("=== LIST COMPREHENSION ===")
print(f"Total: {total_comprension:.2f} kg")
print(f"Tiempo: {tiempo_comprension:.6f} segundos\n")

print("=== GENERADOR ===")
print(f"Total: {total_generador:.2f} kg")
print(f"Tiempo: {tiempo_generador:.6f} segundos\n")


# -----------------------------------
# COMPARACIÓN FINAL
# -----------------------------------
tiempos = {
    "Lista tradicional": tiempo_lista,
    "List comprehension": tiempo_comprension,
    "Generador": tiempo_generador
}

mas_rapido = min(tiempos, key=tiempos.get)

print("=== CONCLUSIÓN ===")
print(f"El método más rápido ha sido: {mas_rapido}")