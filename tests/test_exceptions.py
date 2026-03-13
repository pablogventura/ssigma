# -*- coding: utf-8 -*-
import unittest
from ssigma.exceptions import SSigmaError, ParseError, LabelNotFoundError, ExecutionError


class TestExceptions(unittest.TestCase):
    def test_ssigma_error_hereda_exception(self):
        e = SSigmaError("mensaje")
        self.assertIsInstance(e, Exception)
        self.assertIn("mensaje", str(e))

    def test_parse_error_con_contexto(self):
        e = ParseError("instrucción no reconocida", num_linea=5, archivo="x.code", fragmento="N2 <- 1")
        self.assertEqual(e.num_linea, 5)
        self.assertEqual(e.archivo, "x.code")
        self.assertEqual(e.fragmento, "N2 <- 1")
        self.assertIn("línea 5", str(e))
        self.assertIn("x.code", str(e))
        self.assertIn("instrucción no reconocida", str(e))

    def test_label_not_found(self):
        e = LabelNotFoundError(99)
        self.assertEqual(e.label, 99)
        self.assertIn("99", str(e))

    def test_label_not_found_desde_instruccion(self):
        e = LabelNotFoundError(10, desde_instruccion=3)
        self.assertIn("10", str(e))
        self.assertIn("instrucción 4", str(e))

    def test_execution_error_con_contexto(self):
        e = ExecutionError("No existe el label L5.", num_instruccion=2, num_paso=10, instruccion="GOTO L5")
        self.assertEqual(e.num_instruccion, 2)
        self.assertEqual(e.num_paso, 10)
        self.assertIn("Instrucción", str(e))
        self.assertIn("3", str(e))
        self.assertIn("L5", str(e))
