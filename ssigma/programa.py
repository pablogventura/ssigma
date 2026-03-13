# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.

import pickle

from .instrucciones import IfAlfabetico, IfNumerico, Goto


def cargar_programa(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def guardar_programa(programa, path):
    with open(path, "wb") as f:
        pickle.dump(programa, f, pickle.HIGHEST_PROTOCOL)


class Programa(object):
    """Programa P = I₁…Iₙ. Validación de labels en GOTO/IF."""
    def __init__(self, instrucciones=None):
        if instrucciones is None:
            instrucciones = []
        assert isinstance(instrucciones, list), "no es lista"
        self.ins = instrucciones
        for i in self.ins:
            if type(i) in (IfAlfabetico, IfNumerico, Goto):
                self.encontrar_label(i.destino)

    def encontrar_label(self, label):
        for idx, i in enumerate(self.ins):
            if i.label == label:
                return idx
        raise AssertionError("no existe el label %s" % label)

    def __str__(self):
        return "".join(i.__str__() + "\n" for i in self.ins)
