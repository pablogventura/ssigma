# -*- coding: utf-8 -*-
import unittest
import os
import tempfile
from ssigma import Parser, Programa, registro_por_defecto
from ssigma.exceptions import ParseError
from ssigma.instrucciones import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
    PrintNumerico, PrintPalabra, InputNumerico, InputPalabra,
    Agregar, VaciarPalabra, CopiaPalabra, IfAlfabetico,
)


class TestParser(unittest.TestCase):
    def setUp(self):
        self.p = Parser()

    def test_linea_vacia_retorna_none(self):
        self.assertIsNone(self.p.instruccion(""))
        self.assertIsNone(self.p.instruccion("   "))
        self.assertIsNone(self.p.instruccion(None))

    def test_sucesor(self):
        i = self.p.instruccion("N1 <- N1 + 1")
        self.assertIsInstance(i, Sucesor)
        self.assertEqual(i.var, 1)
        self.assertIsNone(i.label)

    def test_sucesor_con_label(self):
        i = self.p.instruccion("L10 N2 <- N2 + 1")
        self.assertEqual(i.label, 10)
        self.assertEqual(i.var, 2)

    def test_restapunto(self):
        i = self.p.instruccion("N3 <- N3 -·- 1")
        self.assertIsInstance(i, RestaPunto)
        self.assertEqual(i.var, 3)

    def test_cero(self):
        i = self.p.instruccion("N1 <- 0")
        self.assertIsInstance(i, Cero)
        self.assertEqual(i.var, 1)

    def test_copia_numerica(self):
        i = self.p.instruccion("N2 <- N1")
        self.assertIsInstance(i, CopiaNumerica)
        self.assertEqual(i.var, 2)
        self.assertEqual(i.var_src, 1)

    def test_if_numerico(self):
        i = self.p.instruccion("IF N1 != 0 GOTO L5")
        self.assertIsInstance(i, IfNumerico)
        self.assertEqual(i.var, 1)
        self.assertEqual(i.destino, 5)

    def test_goto(self):
        i = self.p.instruccion("GOTO L3")
        self.assertIsInstance(i, Goto)
        self.assertEqual(i.destino, 3)

    def test_skip(self):
        i = self.p.instruccion("SKIP")
        self.assertIsInstance(i, Skip)

    def test_print_numerico(self):
        i = self.p.instruccion("PRINT N2")
        self.assertIsInstance(i, PrintNumerico)
        self.assertEqual(i.var, 2)

    def test_print_palabra(self):
        i = self.p.instruccion("PRINT P1")
        self.assertIsInstance(i, PrintPalabra)
        self.assertEqual(i.var, 1)

    def test_input_numerico(self):
        i = self.p.instruccion("INPUT N3")
        self.assertIsInstance(i, InputNumerico)
        self.assertEqual(i.var, 3)

    def test_input_palabra(self):
        i = self.p.instruccion("INPUT P2")
        self.assertIsInstance(i, InputPalabra)
        self.assertEqual(i.var, 2)

    def test_vaciar_palabra(self):
        i = self.p.instruccion("P1 <- EPSILON")
        self.assertIsInstance(i, VaciarPalabra)
        self.assertEqual(i.var, 1)

    def test_copia_palabra(self):
        i = self.p.instruccion("P2 <- P1")
        self.assertIsInstance(i, CopiaPalabra)
        self.assertEqual(i.var, 2)
        self.assertEqual(i.var_src, 1)

    def test_if_alfabetico(self):
        i = self.p.instruccion("IF P1 BEGINS a GOTO L2")
        self.assertIsInstance(i, IfAlfabetico)
        self.assertEqual(i.var, 1)
        self.assertEqual(i.simbolo, "A")
        self.assertEqual(i.destino, 2)

    def test_agregar(self):
        i = self.p.instruccion("P1 <- P1 a")
        self.assertIsInstance(i, Agregar)
        self.assertEqual(i.var, 1)
        self.assertEqual(i.simbolo, "A")

    def test_programa_desde_archivo(self):
        ruta = os.path.join(os.path.dirname(__file__), "..", "examples", "devuelveunoconh.code")
        prog = self.p.programa_desde_archivo(ruta, verbose=False)
        self.assertIsInstance(prog, Programa)
        self.assertGreater(len(prog.ins), 0)

    def test_parse_error_al_cargar_archivo_con_linea_invalida(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".code", delete=False) as f:
            f.write("N1 <- 0\n")
            f.write("N1 <- N1 + 1\n")
            f.write("esto no es instruccion\n")
            ruta = f.name
        try:
            with self.assertRaises(ParseError) as ctx:
                self.p.programa_desde_archivo(ruta, verbose=False)
            e = ctx.exception
            self.assertEqual(e.num_linea, 3)
            self.assertIn("3", str(e))
            self.assertIn("instrucción no reconocida", str(e))
            self.assertIn("esto no es instruccion", str(e))
        finally:
            os.unlink(ruta)

    def test_macro_sin_registro_retorna_none(self):
        i = self.p.instruccion("SUMA(N1, N2, N3)")
        self.assertIsNone(i)

    def test_macro_con_registro_retorna_lista(self):
        reg = registro_por_defecto()
        p_macro = Parser(registro_macros=reg)
        i = p_macro.instruccion("SUMA(N1, N2, N3)")
        self.assertIsInstance(i, list)
        self.assertGreater(len(i), 1)
        prog = Programa(i)
        self.assertGreater(len(prog.ins), 1)
