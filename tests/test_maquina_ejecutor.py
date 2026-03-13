# -*- coding: utf-8 -*-
import unittest
from ssigma import Programa, Ejecucion
from ssigma.instrucciones import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
    Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico,
)


class TestEjecutorNumerico(unittest.TestCase):
    def test_sucesor(self):
        prog = Programa([Sucesor(1)])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 1)

    def test_restapunto_no_baja_de_cero(self):
        prog = Programa([RestaPunto(1)])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 0)

    def test_restapunto_decrece(self):
        prog = Programa([Sucesor(1), Sucesor(1), RestaPunto(1)])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 1)

    def test_cero(self):
        prog = Programa([Sucesor(1), Sucesor(1), Cero(1)])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 0)

    def test_copia_numerica(self):
        prog = Programa([Sucesor(2), CopiaNumerica(1, 2)])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 1)
        self.assertEqual(e.numericas[2], 1)

    def test_if_numerico_salta_si_no_cero(self):
        # N1<-1; IF N1!=0 GOTO L2; N2<-1; L2 SKIP (label 2 en índice 3)
        prog = Programa([
            Sucesor(1),
            IfNumerico(1, 2),
            Sucesor(2),
            Skip(label=2),
        ])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 1)
        self.assertEqual(e.numericas[2], 0)

    def test_if_numerico_no_salta_si_cero(self):
        # N1<-0; IF N1!=0 GOTO L2; N2<-1; L2 SKIP
        prog = Programa([
            Cero(1),
            IfNumerico(1, 2),
            Sucesor(2),
            Skip(label=2),
        ])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[2], 1)

    def test_goto(self):
        # GOTO L2; N1<-1; L2 SKIP
        prog = Programa([Goto(2), Sucesor(1), Skip(label=2)])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 0)

    def test_skip(self):
        prog = Programa([Skip(), Sucesor(1)])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 1)


class TestEjecutorPalabras(unittest.TestCase):
    def test_agregar_quitar(self):
        prog = Programa([Agregar(1, "a"), Agregar(1, "b"), Quitar(1)])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.alfabeticas[1], "b")

    def test_vaciar_palabra(self):
        prog = Programa([Agregar(1, "x"), VaciarPalabra(1)])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.alfabeticas[1], "")

    def test_copia_palabra(self):
        prog = Programa([Agregar(1, "a"), CopiaPalabra(2, 1)])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.alfabeticas[1], "a")
        self.assertEqual(e.alfabeticas[2], "a")

    def test_if_alfabetico_begins(self):
        # P1<-P1a; IF P1 BEGINS a GOTO L2; N1<-1; L2 SKIP
        prog = Programa([
            Agregar(1, "a"),
            IfAlfabetico(1, "a", 2),
            Sucesor(1),
            Skip(label=2),
        ])
        e = Ejecucion(prog)
        e.debug = False
        e.ejecutar()
        self.assertEqual(e.numericas[1], 0)


class TestOrquilla(unittest.TestCase):
    def test_orquilla_numerica_cero_uno(self):
        # Programa que deja N1 = 1
        prog = Programa([Sucesor(1)])
        e = Ejecucion(prog)
        e.debug = False
        f = e.orquilla_numerica(0, 0)
        self.assertEqual(f(), 1)

    def test_orquilla_con_params(self):
        prog = Programa([CopiaNumerica(1, 2), Sucesor(1)])
        e = Ejecucion(prog)
        e.debug = False
        f = e.orquilla_numerica(2, 0)
        self.assertEqual(f(3, 5), 6)
