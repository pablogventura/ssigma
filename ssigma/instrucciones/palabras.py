# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# Instrucciones sobre variables de palabra (Pk).

from .base import Instruccion


class Agregar(Instruccion):
    """Pk := Pk.a"""
    __slots__ = ("var", "label", "es_numerica", "simbolo")

    def __init__(self, var, simbolo, label=None):
        super(Agregar, self).__init__(var, label)
        self.simbolo = str(simbolo)
        self.es_numerica = False

    def __str__(self):
        return super(Agregar, self).__str__() + "P%s <- P%s%s" % (self.var, self.var, self.simbolo)


class Quitar(Instruccion):
    """Pk := ^↷Pk (quitar primer símbolo)"""
    def __init__(self, var, label=None):
        super(Quitar, self).__init__(var, label)
        self.es_numerica = False

    def __str__(self):
        return super(Quitar, self).__str__() + "P%s <- ^P%s" % (self.var, self.var)


class VaciarPalabra(Instruccion):
    """Pk := ε"""
    def __init__(self, var, label=None):
        super(VaciarPalabra, self).__init__(var, label)
        self.es_numerica = False

    def __str__(self):
        return super(VaciarPalabra, self).__str__() + "P%s <- epsilon" % self.var


class CopiaPalabra(Instruccion):
    """Pk := Pn"""
    __slots__ = ("var", "label", "es_numerica", "var_src")

    def __init__(self, var_dest, var_src, label=None):
        super(CopiaPalabra, self).__init__(var_dest, label)
        self.var_src = int(var_src)
        self.es_numerica = False

    def __str__(self):
        return super(CopiaPalabra, self).__str__() + "P%s <- P%s" % (self.var, self.var_src)


class IfAlfabetico(Instruccion):
    """IF Pk BEGINS a GOTO Lm"""
    __slots__ = ("var", "label", "es_numerica", "destino", "simbolo")

    def __init__(self, var, simbolo, destino, label=None):
        super(IfAlfabetico, self).__init__(var, label)
        self.destino = int(destino)
        self.simbolo = str(simbolo)
        self.es_numerica = False

    def __str__(self):
        return super(IfAlfabetico, self).__str__() + "IF P%s BEGINS %s GOTO L%s" % (
            self.var, self.simbolo, self.destino)
