# -*- coding: utf-8 -*-
import unittest
from ssigma.infinitupla import Infinitupla


class TestInfinitupla(unittest.TestCase):
    def test_indexacion_desde_uno(self):
        n = Infinitupla(True)
        self.assertEqual(n[1], 0)
        n[1] = 5
        self.assertEqual(n[1], 5)
        n[2] = 10
        self.assertEqual(n[2], 10)

    def test_indice_cero_prohibido(self):
        n = Infinitupla(True)
        with self.assertRaises(AssertionError):
            _ = n[0]
        with self.assertRaises(AssertionError):
            n[0] = 1

    def test_default_numerica(self):
        n = Infinitupla(True)
        self.assertEqual(n[100], 0)

    def test_default_alfabetica(self):
        a = Infinitupla(False)
        self.assertEqual(a[100], "")

    def test_crece_automaticamente(self):
        n = Infinitupla(True)
        n[5] = 99
        self.assertEqual(n[5], 99)
        self.assertEqual(n[1], 0)
        self.assertEqual(n[3], 0)
