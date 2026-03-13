# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.


class Instruccion(object):
    """Clase base para instrucciones del lenguaje S^Σ (Ins^Σ)."""
    __slots__ = ("var", "label", "es_numerica")

    def __init__(self, var, label=None):
        self.var = int(var)
        self.label = int(label) if label else None
        self.es_numerica = None

    def __str__(self):
        return "L%s\t" % self.label if self.label else "\t"
