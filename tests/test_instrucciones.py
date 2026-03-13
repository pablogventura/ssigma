# -*- coding: utf-8 -*-
import unittest
from ssigma.instrucciones import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
    Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico,
)


class TestInstruccionesNumericas(unittest.TestCase):
    def test_sucesor(self):
        i = Sucesor(3)
        self.assertEqual(i.var, 3)
        self.assertIsNone(i.label)
        self.assertTrue(i.es_numerica)
        self.assertIn("N3 <- N3 + 1", str(i))

    def test_sucesor_con_label(self):
        i = Sucesor(1, label=10)
        self.assertEqual(i.label, 10)
        self.assertIn("L10", str(i))

    def test_restapunto(self):
        i = RestaPunto(2)
        self.assertEqual(i.var, 2)
        self.assertIn("N2 <- N2 -·- 1", str(i))

    def test_cero(self):
        i = Cero(5)
        self.assertEqual(i.var, 5)
        self.assertIn("N5 <- 0", str(i))

    def test_copia_numerica(self):
        i = CopiaNumerica(1, 2)
        self.assertEqual(i.var, 1)
        self.assertEqual(i.var_src, 2)
        self.assertIn("N1 <- N2", str(i))

    def test_if_numerico(self):
        i = IfNumerico(1, 5)
        self.assertEqual(i.var, 1)
        self.assertEqual(i.destino, 5)
        self.assertIn("IF N1 != 0 GOTO L5", str(i))

    def test_goto(self):
        i = Goto(7)
        self.assertEqual(i.destino, 7)
        self.assertEqual(i.var, 0)
        self.assertIn("GOTO L7", str(i))

    def test_skip(self):
        i = Skip()
        self.assertEqual(i.var, 0)
        self.assertIn("SKIP", str(i))


class TestInstruccionesPalabras(unittest.TestCase):
    def test_agregar(self):
        i = Agregar(1, "a")
        self.assertEqual(i.var, 1)
        self.assertEqual(i.simbolo, "a")
        self.assertFalse(i.es_numerica)
        self.assertIn("P1 <- P1a", str(i))

    def test_quitar(self):
        i = Quitar(2)
        self.assertEqual(i.var, 2)
        self.assertIn("P2 <- ^P2", str(i))

    def test_vaciar_palabra(self):
        i = VaciarPalabra(1)
        self.assertIn("epsilon", str(i))

    def test_copia_palabra(self):
        i = CopiaPalabra(2, 1)
        self.assertEqual(i.var, 2)
        self.assertEqual(i.var_src, 1)
        self.assertIn("P2 <- P1", str(i))

    def test_if_alfabetico(self):
        i = IfAlfabetico(1, "x", 3)
        self.assertEqual(i.var, 1)
        self.assertEqual(i.simbolo, "x")
        self.assertEqual(i.destino, 3)
        self.assertIn("BEGINS x", str(i))
