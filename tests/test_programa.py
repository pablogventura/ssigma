# -*- coding: utf-8 -*-
import unittest
import tempfile
import os
from ssigma import Programa, cargar_programa, guardar_programa
from ssigma.instrucciones import Skip, Goto, Sucesor
from ssigma.exceptions import LabelNotFoundError


class TestPrograma(unittest.TestCase):
    def test_programa_vacio_no_permitido_por_def(self):
        p = Programa([])
        self.assertEqual(len(p.ins), 0)

    def test_programa_una_instruccion(self):
        p = Programa([Skip()])
        self.assertEqual(len(p.ins), 1)

    def test_encontrar_label(self):
        goto = Goto(5)
        skip1 = Skip()
        skip2 = Skip(label=5)
        p = Programa([skip1, skip2])
        self.assertEqual(p.encontrar_label(5), 1)

    def test_label_no_existente_raise(self):
        goto = Goto(99)
        with self.assertRaises(LabelNotFoundError) as ctx:
            Programa([goto])
        self.assertEqual(ctx.exception.label, 99)

    def test_guardar_y_cargar(self):
        prog = Programa([Sucesor(1), Skip(label=1)])
        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
            path = f.name
        try:
            guardar_programa(prog, path)
            cargado = cargar_programa(path)
            self.assertEqual(len(cargado.ins), 2)
            self.assertEqual(cargado.ins[0].var, 1)
            self.assertEqual(cargado.ins[1].label, 1)
        finally:
            os.unlink(path)
