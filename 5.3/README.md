# 🛰️ Comparación de Optimización y Documentación en Python

Aplicación de escritorio con interfaz gráfica (Tkinter) que compara dos versiones del mismo problema:
una **no optimizada** y una **optimizada**, usando datos en tiempo real de la Estación Espacial Internacional.

---

## 🎯 Objetivo

Demostrar de forma visual y medible cómo las decisiones de programación afectan al rendimiento,
utilizando herramientas como `cProfile` para análisis de rendimiento y `docstrings` para documentación.

---

## 📋 Funcionalidades

| Funcionalidad | Descripción |
|---|---|
| **Datos en tiempo real** | Posición de la ISS y lista de astronautas vía API |
| **Dos versiones** | Panel izquierdo (no optimizada) vs. panel derecho (optimizada) |
| **Indicador de estado** | Color verde (OK), rojo (error), amarillo (esperando) |
| **Tiempo de ejecución** | Medición en milisegundos en cada panel |
| **Profiling con cProfile** | Estadísticas de rendimiento debajo de cada panel |
| **Botón Help** | Muestra los docstrings de todas las funciones |
| **Actualización automática** | Los datos se refrescan cada 8 segundos |

---

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
python main.py
```

### 3. Generar documentación PDF

```bash
python docs/generar_pdf.py
```

### 4. Ver documentación HTML

Abrir `docs/documentacion_web.html` en cualquier navegador.

---

## 📁 Estructura del Proyecto

```
5.3/
├── main.py                       # Aplicación principal (Tkinter)
├── utils.py                      # Funciones de API y procesamiento
├── requirements.txt              # Dependencias del proyecto
├── README.md                     # Este archivo
└── docs/
    ├── documentacion_web.html    # Documentación HTML
    ├── generar_pdf.py            # Script generador de PDF
    └── documentacion_proyecto.pdf # PDF generado (tras ejecutar el script)
```

---

## ⚙️ Requisitos

- **Python** 3.8 o superior
- **Tkinter** (incluido con Python en la mayoría de instalaciones)
- **Conexión a Internet** (para acceder a la API de Open Notify)
- Dependencias listadas en `requirements.txt`:
  - `requests` — peticiones HTTP
  - `fpdf2` — generación de PDF

---

## 🔗 API utilizada

- [Open Notify - ISS Position](http://api.open-notify.org/iss-now.json) — Posición actual de la ISS
- [Open Notify - Astronauts](http://api.open-notify.org/astros.json) — Astronautas en el espacio

---

## 📊 Comparación rápida

| Aspecto | No Optimizada | Optimizada |
|---|---|---|
| Elementos únicos | Bucle anidado O(n²) | `set()` O(n) |
| Estadísticas | Bucles manuales | `sum()`, `min()`, `max()` |
| Longitud de cadena | Recorrido carácter a carácter | `len()` |
| Construcción de texto | Concatenación con `+` | f-strings |

---

## 📄 Licencia

Proyecto académico — DAW — Abril 2026
