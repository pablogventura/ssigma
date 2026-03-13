# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# Programa P = I₁…Iₙ y persistencia (pickle).

import pickle

from .instrucciones import INSTRUCCIONES_CON_DESTINO
from .exceptions import LabelNotFoundError

ENCODING = "utf-8"


def cargar_programa(path):
    """Carga un Programa desde un archivo pickle."""
    with open(path, "rb") as f:
        return pickle.load(f)


def guardar_programa(programa, path):
    """Guarda un Programa en un archivo pickle."""
    with open(path, "wb") as f:
        pickle.dump(programa, f, pickle.HIGHEST_PROTOCOL)


class Programa(object):
    """Programa P = I₁…Iₙ. Valida que todos los labels referenciados existan."""
    def __init__(self, instrucciones=None):
        if instrucciones is None:
            instrucciones = []
        if not isinstance(instrucciones, list):
            raise TypeError("instrucciones debe ser una lista")
        self.ins = list(instrucciones)
        for idx, i in enumerate(self.ins):
            if type(i) in INSTRUCCIONES_CON_DESTINO:
                self.encontrar_label(i.destino, desde_instruccion=idx)

    def encontrar_label(self, label, desde_instruccion=None):
        """Índice (0-based) de la primera instrucción con el label dado."""
        for idx, i in enumerate(self.ins):
            if i.label == label:
                return idx
        raise LabelNotFoundError(label, desde_instruccion=desde_instruccion)

    def __str__(self):
        return "".join(i.__str__() + "\n" for i in self.ins)
