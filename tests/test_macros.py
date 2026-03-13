# -*- coding: utf-8 -*-
import unittest
import os
from ssigma import Macro, RegistroMacros, Programa, Ejecucion, Parser, registro_por_defecto
from ssigma.macros import macro_suma, MacroError
from ssigma.instrucciones import CopiaNumerica
from ssigma.parser.macro_def_parser import cargar_archivo_macros, parsear_linea_cuerpo


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

    def test_parsear_linea_cuerpo(self):
        lab, d = parsear_linea_cuerpo("V4 <- V2")
        self.assertIsNone(lab)
        self.assertEqual(d, {"tipo": "CopiaNumerica", "var_dest": "V4", "var_src": "V2"})
        lab, d = parsear_linea_cuerpo("A1: IF V5 != 0 GOTO A2")
        self.assertEqual(lab, "A1")
        self.assertEqual(d.get("tipo"), "IfNumerico")
        self.assertEqual(d.get("var"), "V5")
        self.assertEqual(d.get("destino"), "A2")

    def test_cargar_archivo_macros_y_include(self):
        base = os.path.join(os.path.dirname(__file__), "..", "examples")
        reg = cargar_archivo_macros(os.path.join(base, "mi_suma.macros"))
        self.assertIsNotNone(reg.obtener("SUMA"))
        ins = reg.expandir_llamada("SUMA", [1, 2, 3])
        prog = Programa(ins)
        e = Ejecucion(prog)
        e.debug = False
        e.numericas[2], e.numericas[3] = 6, 3
        e.ejecutar()
        self.assertEqual(e.numericas[1], 9)
        p = Parser()
        prog2 = p.programa_desde_archivo(os.path.join(base, "prog_con_include.code"), verbose=False)
        e2 = Ejecucion(prog2)
        e2.debug = False
        e2.numericas[2], e2.numericas[3] = 2, 3
        e2.ejecutar()
        self.assertEqual(e2.numericas[1], 5)

    def test_resta_mult_pred_doble_max_min(self):
        from ssigma import Ejecucion
        reg = registro_por_defecto()
        e = Ejecucion(Programa([]))
        e.debug = False
        for nombre, args, setup, esperado in [
            ("RESTA", [1, 10, 4], lambda ex: (ex.numericas.__setitem__(10, 10), ex.numericas.__setitem__(4, 4)), 6),
            ("MULT", [1, 2, 3], lambda ex: (ex.numericas.__setitem__(2, 3), ex.numericas.__setitem__(3, 4)), 12),
            ("PRED", [1, 2], lambda ex: ex.numericas.__setitem__(2, 5), 4),
            ("DOBLE", [1, 2], lambda ex: ex.numericas.__setitem__(2, 7), 14),
            ("MAX", [1, 2, 3], lambda ex: (ex.numericas.__setitem__(2, 3), ex.numericas.__setitem__(3, 8)), 8),
            ("MIN", [1, 2, 3], lambda ex: (ex.numericas.__setitem__(2, 5), ex.numericas.__setitem__(3, 2)), 2),
        ]:
            ins = reg.expandir_llamada(nombre, args)
            prog = Programa(ins)
            ex = Ejecucion(prog)
            ex.debug = False
            setup(ex)
            ex.ejecutar()
            self.assertEqual(ex.numericas[1], esperado, "macro %s" % nombre)
