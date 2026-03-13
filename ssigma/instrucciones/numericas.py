# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# Instrucciones numéricas y de control (Nk, GOTO, SKIP).

from .base import Instruccion


class Sucesor(Instruccion):
    """Nk := Nk + 1"""
    def __init__(self, var, label=None):
        super(Sucesor, self).__init__(var, label)
        self.es_numerica = True

    def __str__(self):
        return super(Sucesor, self).__str__() + "N%s <- N%s + 1" % (self.var, self.var)


class RestaPunto(Instruccion):
    """Nk := Nk −· 1 (predecesor)"""
    def __init__(self, var, label=None):
        super(RestaPunto, self).__init__(var, label)
        self.es_numerica = True

    def __str__(self):
        return super(RestaPunto, self).__str__() + "N%s <- N%s -·- 1" % (self.var, self.var)


class Cero(Instruccion):
    """Nk := 0"""
    def __init__(self, var, label=None):
        super(Cero, self).__init__(var, label)
        self.es_numerica = True

    def __str__(self):
        return super(Cero, self).__str__() + "N%s <- 0" % self.var


class CopiaNumerica(Instruccion):
    """Nk := Nn"""
    __slots__ = ("var", "label", "es_numerica", "var_src")

    def __init__(self, var_dest, var_src, label=None):
        super(CopiaNumerica, self).__init__(var_dest, label)
        self.var_src = int(var_src)
        self.es_numerica = True

    def __str__(self):
        return super(CopiaNumerica, self).__str__() + "N%s <- N%s" % (self.var, self.var_src)


class IfNumerico(Instruccion):
    """IF Nk != 0 GOTO Lm"""
    __slots__ = ("var", "label", "es_numerica", "destino")

    def __init__(self, var, destino, label=None):
        super(IfNumerico, self).__init__(var, label)
        self.destino = int(destino)
        self.es_numerica = True

    def __str__(self):
        return super(IfNumerico, self).__str__() + "IF N%s != 0 GOTO L%s" % (self.var, self.destino)


class Goto(Instruccion):
    """GOTO Lm"""
    __slots__ = ("var", "label", "es_numerica", "destino")

    def __init__(self, destino, label=None):
        super(Goto, self).__init__(0, label)
        self.destino = int(destino)
        self.es_numerica = True

    def __str__(self):
        return super(Goto, self).__str__() + "GOTO L%s" % self.destino


class Skip(Instruccion):
    """SKIP"""
    def __init__(self, label=None):
        super(Skip, self).__init__(0, label)
        self.es_numerica = True

    def __str__(self):
        return super(Skip, self).__str__() + "SKIP"
