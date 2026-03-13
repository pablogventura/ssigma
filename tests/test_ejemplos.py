# -*- coding: utf-8 -*-
"""Tests que cargan y ejecutan los programas de examples/*.code."""
import unittest
import os
from ssigma import Parser, Programa, Ejecucion, registro_por_defecto


def _ruta(*rel):
    return os.path.join(os.path.dirname(__file__), "..", "examples", *rel)


class TestEjemplos(unittest.TestCase):
    def _prog_desde_archivo(self, nombre, con_macros=False):
        p = Parser(registro_por_defecto()) if con_macros else Parser()
        return p.programa_desde_archivo(_ruta(nombre), verbose=False)

    def test_devuelveunoconh_parsea_y_ejecuta(self):
        prog = self._prog_desde_archivo("devuelveunoconh.code")
        e = Ejecucion(prog)
        e.debug = False
        f = e.orquilla_numerica(0, 1)
        result = f("g")
        self.assertEqual(result, 0)

    def test_solo_numericos_n1_queda_en_dos(self):
        prog = self._prog_desde_archivo("solo_numericos.code")
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 2)

    def test_restapunto_n1_queda_en_uno(self):
        prog = self._prog_desde_archivo("restapunto.code")
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 1)

    def test_copia_y_salto_salta_y_n3_no_incrementa(self):
        prog = self._prog_desde_archivo("copia_y_salto.code")
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 2)
        self.assertEqual(e.numericas[2], 2)
        self.assertEqual(e.numericas[3], 0)

    def test_palabras_p1_p2_y_salto_alfabetico(self):
        prog = self._prog_desde_archivo("palabras.code")
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.alfabeticas[1], "AB")
        self.assertEqual(e.alfabeticas[2], "AB")
        self.assertEqual(e.numericas[1], 0)

    def test_suma_macro_parsea_y_resultado_correcto(self):
        prog = self._prog_desde_archivo("suma_macro.code", con_macros=True)
        e = Ejecucion(prog)
        e.debug = False
        e.numericas[2] = 10
        e.numericas[3] = 7
        e.ejecutar()
        self.assertEqual(e.numericas[1], 17)

    def test_resta_macro(self):
        prog = self._prog_desde_archivo("resta_macro.code", con_macros=True)
        e = Ejecucion(prog)
        e.debug = False
        e.numericas[2] = 10
        e.numericas[3] = 4
        e.ejecutar()
        self.assertEqual(e.numericas[1], 6)

    def test_mult_macro(self):
        prog = self._prog_desde_archivo("mult_macro.code", con_macros=True)
        e = Ejecucion(prog)
        e.debug = False
        e.numericas[2] = 3
        e.numericas[3] = 4
        e.ejecutar()
        self.assertEqual(e.numericas[1], 12)
