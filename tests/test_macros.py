# -*- coding: utf-8 -*-
import unittest
from ssigma import Macro, RegistroMacros, Programa, Ejecucion, registro_por_defecto
from ssigma.macros import macro_suma, MacroError
from ssigma.instrucciones import CopiaNumerica


class TestMacro(unittest.TestCase):
    def test_macro_simple_expande(self):
        cuerpo = [
            {"tipo": "CopiaNumerica", "var_dest": "V1", "var_src": "V2"},
        ]
        m = Macro("COPIA", ["V1", "V2"], cuerpo)
        ins = m.expandir({"V1": 1, "V2": 2})
        self.assertEqual(len(ins), 1)
        self.assertIsInstance(ins[0], CopiaNumerica)
        self.assertEqual(ins[0].var, 1)
        self.assertEqual(ins[0].var_src, 2)

    def test_macro_suma_expande(self):
        m = macro_suma()
        ins = m.expandir({"V1": 1, "V2": 2, "V3": 3})
        self.assertGreater(len(ins), 5)
        self.assertEqual(ins[0].var, 1000)
        self.assertEqual(ins[0].var_src, 2)

    def test_sustitucion_incompleta_raise(self):
        m = macro_suma()
        with self.assertRaises(MacroError):
            m.expandir({"V1": 1, "V2": 2})

    def test_registro_obtener(self):
        reg = registro_por_defecto()
        m = reg.obtener("SUMA")
        self.assertIsNotNone(m)
        self.assertEqual(m.nombre, "SUMA")
        self.assertIsNone(reg.obtener("NOEXISTE"))

    def test_expandir_llamada_suma(self):
        reg = registro_por_defecto()
        ins = reg.expandir_llamada("SUMA", [1, 2, 3])
        self.assertGreater(len(ins), 1)
        prog = Programa(ins)
        e = Ejecucion(prog)
        e.debug = False
        e.numericas[2] = 4
        e.numericas[3] = 5
        e.ejecutar()
        self.assertEqual(e.numericas[1], 9)

    def test_expandir_llamada_macro_inexistente(self):
        reg = RegistroMacros()
        with self.assertRaises(MacroError):
            reg.expandir_llamada("NOEXISTE", [1, 2])

    def test_expandir_llamada_args_incorrectos(self):
        reg = registro_por_defecto()
        with self.assertRaises(MacroError):
            reg.expandir_llamada("SUMA", [1, 2])
