import tkinter as tk
from tkinter import messagebox
import pytest
import io
import contextlib
import sys

# Importar las funciones del módulo de operaciones
from operaciones import suma, resta, multiplicacion, division

class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Académica 6.1")
        self.root.geometry("400x600")
        self.root.configure(bg="#2c3e50")

        self.operacion_actual = ""
        self.primer_numero = None
        self.operador = None

        # Estilos
        self.font_display = ("Consolas", 24, "bold")
        self.font_buttons = ("Segoe UI", 14)
        self.font_tests = ("Consolas", 10)

        # Pantalla de visualización
        self.display = tk.Entry(root, font=self.font_display, justify='right', bd=10, insertwidth=4, bg="#ecf0f1", fg="#2c3e50")
        self.display.pack(fill=tk.BOTH, padx=10, pady=20)

        # Contenedor de botones
        self.btn_frame = tk.Frame(root, bg="#2c3e50")
        self.btn_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # Definición de botones
        botones = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]

        for (text, row, col) in botones:
            btn = tk.Button(self.btn_frame, text=text, width=5, height=2, font=self.font_buttons,
                            command=lambda t=text: self.on_button_click(t),
                            bg="#34495e", fg="white", activebackground="#1abc9c", bd=0)
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        for i in range(4):
            self.btn_frame.grid_columnconfigure(i, weight=1)
        for i in range(1, 5):
            self.btn_frame.grid_rowconfigure(i, weight=1)

        # Botón de Pruebas
        self.test_btn = tk.Button(root, text="Pruebas", font=("Segoe UI", 12, "bold"), 
                                  bg="#e67e22", fg="white", command=self.ejecutar_pruebas, bd=0, pady=10)
        self.test_btn.pack(fill=tk.BOTH, padx=12, pady=10)

        # Area de resultados de pruebas
        self.test_output = tk.Text(root, height=8, font=self.font_tests, bg="#34495e", fg="#ecf0f1", state=tk.DISABLED)
        self.test_output.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

    def on_button_click(self, char):
        if char == 'C':
            self.display.delete(0, tk.END)
            self.primer_numero = None
            self.operador = None
        elif char in '0123456789':
            self.display.insert(tk.END, char)
        elif char in '+-*/':
            try:
                self.primer_numero = float(self.display.get())
                self.operador = char
                self.display.delete(0, tk.END)
            except ValueError:
                pass
        elif char == '=':
            if self.operador and self.primer_numero is not None:
                try:
                    segundo_numero = float(self.display.get())
                    if self.operador == '+': resultado = suma(self.primer_numero, segundo_numero)
                    elif self.operador == '-': resultado = resta(self.primer_numero, segundo_numero)
                    elif self.operador == '*': resultado = multiplicacion(self.primer_numero, segundo_numero)
                    elif self.operador == '/': resultado = division(self.primer_numero, segundo_numero)
                    
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, str(resultado))
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                    self.display.delete(0, tk.END)
                except Exception as e:
                    messagebox.showerror("Error", "Operación inválida")
                    self.display.delete(0, tk.END)

    def ejecutar_pruebas(self):
        """Ejecuta las pruebas unitarias y muestra el resultado en la UI."""
        self.test_output.config(state=tk.NORMAL)
        self.test_output.delete('1.0', tk.END)
        
        # Definición de las pruebas mínimas obligatorias del PDF
        pruebas = [
            ("suma correcta", lambda: suma(2, 3) == 5),
            ("resta correcta", lambda: resta(5, 2) == 3),
            ("multiplicación correcta", lambda: multiplicacion(3, 4) == 12),
            ("división correcta", lambda: division(10, 2) == 5),
            ("división por cero", self.test_div_cero_valido)
        ]

        correctas = 0
        total = len(pruebas)

        for nombre, func in pruebas:
            try:
                if func():
                    self.test_output.insert(tk.END, f"✔ {nombre}\n", "success")
                    correctas += 1
                else:
                    self.test_output.insert(tk.END, f"❌ {nombre}\n", "fail")
            except Exception:
                self.test_output.insert(tk.END, f"❌ {nombre}\n", "fail")

        self.test_output.tag_config("success", foreground="#2ecc71")
        self.test_output.tag_config("fail", foreground="#e74c3c")
        
        # El PDF pide mostrar el resultado final
        resultado_final = f"\nResultado: {correctas}/{total} pruebas correctas"
        self.test_output.insert(tk.END, resultado_final)
        
        # Opcional: Colorear el resultado final según el éxito
        if correctas == total:
            self.test_output.insert(tk.END, " (ÉXITO TOTAL)", "success")
        
        self.test_output.config(state=tk.DISABLED)

    def test_div_cero_valido(self):
        """Verifica que la división por cero lance ValueError (control del error)."""
        try:
            division(10, 0)
            return False # No lanzó error, la prueba falla
        except ValueError:
            return True # Lanzó ValueError, la prueba es correcta

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()
