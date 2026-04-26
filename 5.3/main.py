"""
main.py - Aplicación principal
================================
Comparación de optimización y documentación en Python.

Aplicación con interfaz gráfica Tkinter que compara dos versiones
del mismo problema (optimizada vs. no optimizada) usando datos
en tiempo real de la posición de la ISS.

Autor: Alumno DAW
Fecha: Abril 2026
"""

import tkinter as tk
from tkinter import scrolledtext, font as tkfont
import threading
import time
import cProfile
import io
import pstats
from datetime import datetime

import utils


# ═══════════════════════════════════════════════════════════════
#  CONSTANTES DE ESTILO
# ═══════════════════════════════════════════════════════════════

COLOR_FONDO = "#1e1e2e"
COLOR_PANEL = "#2a2a3d"
COLOR_BORDE = "#3b3b55"
COLOR_TEXTO = "#e0e0e0"
COLOR_TITULO = "#cba6f7"
COLOR_EXITO = "#a6e3a1"
COLOR_ERROR = "#f38ba8"
COLOR_AVISO = "#f9e2af"
COLOR_BOTON = "#45475a"
COLOR_BOTON_HOVER = "#585b70"
COLOR_HELP = "#89b4fa"

INTERVALO_ACTUALIZACION = 8  # segundos entre actualizaciones


# ═══════════════════════════════════════════════════════════════
#  FUNCIONES DE INTERFAZ - VENTANA HELP
# ═══════════════════════════════════════════════════════════════

def mostrar_ventana_help(titulo_version):
    """
    Abre una ventana emergente con la documentación de las funciones.

    Recoge los docstrings de todas las funciones públicas del módulo
    utils.py y los muestra en una ventana independiente con scroll.

    Parámetros:
        titulo_version (str): Texto del título de la ventana,
            por ejemplo 'Help - Versión No Optimizada'.

    Retorna:
        None.
    """
    ventana = tk.Toplevel()
    ventana.title(titulo_version)
    ventana.geometry("700x550")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(True, True)

    # Título
    lbl = tk.Label(
        ventana, text=f"📖 {titulo_version}",
        font=("Consolas", 14, "bold"),
        bg=COLOR_FONDO, fg=COLOR_HELP,
        pady=10
    )
    lbl.pack(fill=tk.X)

    # Área de texto con scroll
    area = scrolledtext.ScrolledText(
        ventana, wrap=tk.WORD,
        font=("Consolas", 10),
        bg=COLOR_PANEL, fg=COLOR_TEXTO,
        insertbackground=COLOR_TEXTO,
        relief=tk.FLAT, padx=10, pady=10
    )
    area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    # Rellenar con los docstrings
    docstrings = utils.obtener_docstrings_modulo()
    for nombre, doc in docstrings:
        area.insert(tk.END, f"{'─' * 50}\n", "separador")
        area.insert(tk.END, f"▶ {nombre}()\n", "nombre_func")
        area.insert(tk.END, f"{doc}\n\n", "docstring")

    # Etiquetas de estilo
    area.tag_config("separador", foreground="#585b70")
    area.tag_config("nombre_func", foreground=COLOR_TITULO, font=("Consolas", 11, "bold"))
    area.tag_config("docstring", foreground=COLOR_TEXTO)
    area.configure(state=tk.DISABLED)

    # Botón cerrar
    btn = tk.Button(
        ventana, text="Cerrar", command=ventana.destroy,
        bg=COLOR_BOTON, fg=COLOR_TEXTO,
        activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_TEXTO,
        relief=tk.FLAT, padx=20, pady=5,
        font=("Consolas", 10, "bold"), cursor="hand2"
    )
    btn.pack(pady=(0, 10))


# ═══════════════════════════════════════════════════════════════
#  FUNCIONES DE PROFILING
# ═══════════════════════════════════════════════════════════════

def ejecutar_con_profiling(funcion, *args):
    """
    Ejecuta una función midiendo su tiempo y recogiendo datos de cProfile.

    Usa cProfile para analizar el rendimiento de la función proporcionada
    y devuelve tanto el resultado como las estadísticas de profiling.

    Parámetros:
        funcion (callable): Función a ejecutar y perfilar.
        *args: Argumentos posicionales que se pasan a la función.

    Retorna:
        tuple: (resultado, tiempo_ms, texto_profiling)
            - resultado: El valor retornado por la función.
            - tiempo_ms (float): Tiempo de ejecución en milisegundos.
            - texto_profiling (str): Estadísticas de cProfile formateadas.
    """
    profiler = cProfile.Profile()
    inicio = time.perf_counter()
    profiler.enable()
    resultado = funcion(*args)
    profiler.disable()
    fin = time.perf_counter()

    tiempo_ms = (fin - inicio) * 1000

    # Capturar salida de cProfile
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative")
    stats.print_stats(10)  # Top 10 llamadas
    texto_profiling = stream.getvalue()

    return resultado, tiempo_ms, texto_profiling


# ═══════════════════════════════════════════════════════════════
#  CLASE PRINCIPAL DE LA APLICACIÓN
# ═══════════════════════════════════════════════════════════════

class AplicacionComparativa:
    """
    Ventana principal de la aplicación comparativa.

    Crea una interfaz Tkinter dividida en dos paneles que muestran
    la versión no optimizada (izquierda) y optimizada (derecha)
    del procesamiento de datos de la ISS.

    Atributos:
        raiz (tk.Tk): Ventana raíz de Tkinter.
        ejecutando (bool): Controla el bucle de actualización.
        paneles (dict): Diccionario con los widgets de cada panel.
    """

    def __init__(self):
        """
        Inicializa la ventana principal y todos los widgets.

        Parámetros:
            Ninguno.

        Retorna:
            None.
        """
        self.raiz = tk.Tk()
        self.raiz.title("🛰️ Comparación de Optimización en Python — ISS Tracker")
        self.raiz.geometry("1280x780")
        self.raiz.configure(bg=COLOR_FONDO)
        self.raiz.minsize(1000, 600)

        self.ejecutando = True
        self.paneles = {}

        self._crear_titulo()
        self._crear_paneles()
        self._crear_barra_inferior()

        # Cerrar limpiamente
        self.raiz.protocol("WM_DELETE_WINDOW", self._cerrar)

        # Primera actualización
        self.raiz.after(500, self._iniciar_actualizacion)

    def _crear_titulo(self):
        """Crea el título superior de la aplicación."""
        marco_titulo = tk.Frame(self.raiz, bg=COLOR_FONDO, pady=8)
        marco_titulo.pack(fill=tk.X)

        lbl = tk.Label(
            marco_titulo,
            text="🛰️  Comparación de Optimización — Datos de la ISS en Tiempo Real",
            font=("Consolas", 15, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TITULO
        )
        lbl.pack()

    def _crear_panel(self, padre, titulo, color_acento, clave):
        """
        Crea un panel completo (datos + profiling + botón Help).

        Parámetros:
            padre (tk.Widget): Widget contenedor.
            titulo (str): Título del panel.
            color_acento (str): Color hexadecimal para el acento del panel.
            clave (str): Clave para almacenar los widgets ('no_opt' u 'opt').

        Retorna:
            None.
        """
        marco = tk.Frame(padre, bg=COLOR_PANEL, relief=tk.FLAT, bd=0)
        marco.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=4)

        # Línea de acento superior
        linea = tk.Frame(marco, bg=color_acento, height=3)
        linea.pack(fill=tk.X)

        # Título del panel
        lbl_titulo = tk.Label(
            marco, text=titulo,
            font=("Consolas", 12, "bold"),
            bg=COLOR_PANEL, fg=color_acento,
            pady=6
        )
        lbl_titulo.pack(fill=tk.X)

        # Indicador de estado
        marco_estado = tk.Frame(marco, bg=COLOR_PANEL)
        marco_estado.pack(fill=tk.X, padx=10)

        indicador = tk.Label(
            marco_estado, text="  ●  ",
            font=("Consolas", 14),
            bg=COLOR_PANEL, fg=COLOR_AVISO
        )
        indicador.pack(side=tk.LEFT)

        lbl_estado = tk.Label(
            marco_estado, text="Esperando primera lectura...",
            font=("Consolas", 9),
            bg=COLOR_PANEL, fg=COLOR_TEXTO, anchor=tk.W
        )
        lbl_estado.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Tiempo de ejecución
        lbl_tiempo = tk.Label(
            marco, text="Tiempo: —",
            font=("Consolas", 10, "bold"),
            bg=COLOR_PANEL, fg=COLOR_AVISO,
            anchor=tk.W, padx=10
        )
        lbl_tiempo.pack(fill=tk.X)

        # Hora de actualización
        lbl_hora = tk.Label(
            marco, text="Última actualización: —",
            font=("Consolas", 9),
            bg=COLOR_PANEL, fg="#7f849c",
            anchor=tk.W, padx=10
        )
        lbl_hora.pack(fill=tk.X)

        # Área de datos
        area_datos = scrolledtext.ScrolledText(
            marco, wrap=tk.WORD, height=10,
            font=("Consolas", 9),
            bg="#1e1e2e", fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief=tk.FLAT, padx=8, pady=6
        )
        area_datos.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Separador
        sep = tk.Label(
            marco, text="── cProfile ──",
            font=("Consolas", 9), bg=COLOR_PANEL, fg="#585b70"
        )
        sep.pack(pady=(4, 0))

        # Área de profiling
        area_profile = scrolledtext.ScrolledText(
            marco, wrap=tk.WORD, height=6,
            font=("Consolas", 8),
            bg="#181825", fg="#9399b2",
            insertbackground=COLOR_TEXTO,
            relief=tk.FLAT, padx=8, pady=4
        )
        area_profile.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 4))

        # Botón Help
        btn_help = tk.Button(
            marco, text="❓ Help",
            font=("Consolas", 10, "bold"),
            bg=COLOR_BOTON, fg=COLOR_HELP,
            activebackground=COLOR_BOTON_HOVER, activeforeground=COLOR_HELP,
            relief=tk.FLAT, padx=16, pady=4, cursor="hand2",
            command=lambda: mostrar_ventana_help(f"Help — {titulo}")
        )
        btn_help.pack(pady=(2, 8))

        # Guardar referencias
        self.paneles[clave] = {
            "indicador": indicador,
            "lbl_estado": lbl_estado,
            "lbl_tiempo": lbl_tiempo,
            "lbl_hora": lbl_hora,
            "area_datos": area_datos,
            "area_profile": area_profile,
        }

    def _crear_paneles(self):
        """Crea los dos paneles (no optimizado y optimizado)."""
        contenedor = tk.Frame(self.raiz, bg=COLOR_FONDO)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=6)

        self._crear_panel(
            contenedor,
            "⚠️ Versión NO Optimizada",
            COLOR_ERROR,
            "no_opt"
        )
        self._crear_panel(
            contenedor,
            "✅ Versión Optimizada",
            COLOR_EXITO,
            "opt"
        )

    def _crear_barra_inferior(self):
        """Crea la barra de estado inferior."""
        barra = tk.Frame(self.raiz, bg=COLOR_BORDE, height=28)
        barra.pack(fill=tk.X, side=tk.BOTTOM)

        self.lbl_barra = tk.Label(
            barra,
            text=f"Actualización automática cada {INTERVALO_ACTUALIZACION}s  •  API: Open Notify  •  Pulsa ❓ Help para ver la documentación",
            font=("Consolas", 8),
            bg=COLOR_BORDE, fg="#a6adc8",
            padx=10, pady=3
        )
        self.lbl_barra.pack(fill=tk.X)

    # ───────────────────────────────────────────────────────────
    #  ACTUALIZACIÓN DE DATOS
    # ───────────────────────────────────────────────────────────

    def _iniciar_actualizacion(self):
        """Lanza la primera actualización en un hilo."""
        hilo = threading.Thread(target=self._bucle_actualizacion, daemon=True)
        hilo.start()

    def _bucle_actualizacion(self):
        """
        Bucle que obtiene datos y actualiza ambos paneles periódicamente.

        Se ejecuta en un hilo secundario para no bloquear la interfaz.
        Cada ciclo obtiene los datos de la API, los procesa con ambas
        versiones y actualiza la GUI a través de raiz.after().

        Parámetros:
            Ninguno.

        Retorna:
            None (se ejecuta indefinidamente hasta cerrar la app).
        """
        while self.ejecutando:
            try:
                # Obtener datos de la API
                posicion = utils.obtener_posicion_iss()
                astronautas = utils.obtener_astronautas()

                if posicion["exito"] and astronautas["exito"]:
                    # Versión NO optimizada con profiling
                    res_no_opt, t_no_opt, prof_no_opt = ejecutar_con_profiling(
                        utils.procesar_datos_no_optimizado, posicion, astronautas
                    )
                    # Versión optimizada con profiling
                    res_opt, t_opt, prof_opt = ejecutar_con_profiling(
                        utils.procesar_datos_optimizado, posicion, astronautas
                    )

                    hora = utils.formatear_hora()

                    # Actualizar GUI desde el hilo principal
                    self.raiz.after(0, self._actualizar_panel,
                                   "no_opt", res_no_opt, t_no_opt, prof_no_opt, hora, True)
                    self.raiz.after(0, self._actualizar_panel,
                                   "opt", res_opt, t_opt, prof_opt, hora, True)
                else:
                    error = posicion["error"] or astronautas["error"]
                    self.raiz.after(0, self._mostrar_error, error)

            except Exception as e:
                self.raiz.after(0, self._mostrar_error, str(e))

            time.sleep(INTERVALO_ACTUALIZACION)

    def _actualizar_panel(self, clave, resultado, tiempo_ms, profiling, hora, exito):
        """
        Actualiza los widgets de un panel con datos nuevos.

        Parámetros:
            clave (str): 'no_opt' u 'opt'.
            resultado (dict): Datos procesados.
            tiempo_ms (float): Tiempo de ejecución en ms.
            profiling (str): Salida de cProfile.
            hora (str): Hora formateada.
            exito (bool): Si la lectura fue exitosa.

        Retorna:
            None.
        """
        panel = self.paneles[clave]

        # Indicador visual
        panel["indicador"].config(fg=COLOR_EXITO if exito else COLOR_ERROR)
        panel["lbl_estado"].config(
            text="Datos actualizados correctamente" if exito else "Error en la lectura"
        )

        # Tiempo
        panel["lbl_tiempo"].config(text=f"Tiempo de ejecución: {tiempo_ms:.3f} ms")

        # Hora
        panel["lbl_hora"].config(text=f"Última actualización: {hora}")

        # Datos
        area = panel["area_datos"]
        area.configure(state=tk.NORMAL)
        area.delete("1.0", tk.END)
        area.insert(tk.END, resultado["resumen"])
        area.configure(state=tk.DISABLED)

        # Profiling
        area_p = panel["area_profile"]
        area_p.configure(state=tk.NORMAL)
        area_p.delete("1.0", tk.END)
        area_p.insert(tk.END, profiling)
        area_p.configure(state=tk.DISABLED)

    def _mostrar_error(self, mensaje):
        """
        Muestra un error en ambos paneles.

        Parámetros:
            mensaje (str): Texto del error.

        Retorna:
            None.
        """
        for clave in ("no_opt", "opt"):
            panel = self.paneles[clave]
            panel["indicador"].config(fg=COLOR_ERROR)
            panel["lbl_estado"].config(text=f"Error: {mensaje[:60]}")

    def _cerrar(self):
        """Detiene el bucle de actualización y cierra la aplicación."""
        self.ejecutando = False
        self.raiz.destroy()

    def ejecutar(self):
        """
        Inicia el bucle principal de la aplicación Tkinter.

        Parámetros:
            Ninguno.

        Retorna:
            None.
        """
        self.raiz.mainloop()


# ═══════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = AplicacionComparativa()
    app.ejecutar()
