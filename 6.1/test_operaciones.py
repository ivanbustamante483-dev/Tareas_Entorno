# test_operaciones.py
# Pruebas unitarias con pytest para las funciones de la calculadora

import pytest
from operaciones import suma, resta, multiplicacion, division


# ─── Tests de suma ────────────────────────────────────────────
class TestSuma:
    def test_suma_positivos(self):
        assert suma(2, 3) == 5

    def test_suma_negativos(self):
        assert suma(-1, -1) == -2

    def test_suma_con_cero(self):
        assert suma(0, 5) == 5

    def test_suma_decimales(self):
        assert suma(1.5, 2.5) == 4.0


# ─── Tests de resta ───────────────────────────────────────────
class TestResta:
    def test_resta_basica(self):
        assert resta(5, 2) == 3

    def test_resta_resultado_negativo(self):
        assert resta(2, 5) == -3

    def test_resta_con_cero(self):
        assert resta(5, 0) == 5


# ─── Tests de multiplicación ─────────────────────────────────
class TestMultiplicacion:
    def test_multiplicacion_basica(self):
        assert multiplicacion(3, 4) == 12

    def test_multiplicacion_por_cero(self):
        assert multiplicacion(5, 0) == 0

    def test_multiplicacion_negativos(self):
        assert multiplicacion(-2, -3) == 6


# ─── Tests de división ───────────────────────────────────────
class TestDivision:
    def test_division_basica(self):
        assert division(10, 2) == 5

    def test_division_decimal(self):
        assert division(7, 2) == 3.5

    def test_division_por_cero(self):
        with pytest.raises(ValueError, match="No se puede dividir por cero"):
            division(10, 0)
