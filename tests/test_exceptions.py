# -*- coding: utf-8 -*-
import unittest
from ssigma.exceptions import SSigmaError, ParseError, LabelNotFoundError


class TestExceptions(unittest.TestCase):
    def test_ssigma_error_hereda_exception(self):
        e = SSigmaError("mensaje")
        self.assertIsInstance(e, Exception)
        self.assertIn("mensaje", str(e))

    def test_parse_error_tiene_linea(self):
        e = ParseError("sintaxis", linea="N1 N2")
        self.assertEqual(e.linea, "N1 N2")
        self.assertIn("sintaxis", str(e))

    def test_label_not_found(self):
        e = LabelNotFoundError(99)
        self.assertEqual(e.label, 99)
        self.assertIn("99", str(e))
