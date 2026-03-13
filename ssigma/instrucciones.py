# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.

class Instruccion(object):
    """Clase base para instrucciones del lenguaje S^Σ."""
    def __init__(self, var, label=None):
        self.var = int(var)
        self.label = int(label) if label else None
        self.es_numerica = None

    def __str__(self):
        result = "L%s\t" % self.label if self.label else "\t"
        return result


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
    def __init__(self, var_dest, var_src, label=None):
        super(CopiaNumerica, self).__init__(var_dest, label)
        self.var_src = int(var_src)
        self.es_numerica = True

    def __str__(self):
        return super(CopiaNumerica, self).__str__() + "N%s <- N%s" % (self.var, self.var_src)


class IfNumerico(Instruccion):
    """IF Nk != 0 GOTO Lm"""
    def __init__(self, var, destino, label=None):
        super(IfNumerico, self).__init__(var, label)
        self.destino = int(destino)
        self.es_numerica = True

    def __str__(self):
        return super(IfNumerico, self).__str__() + "IF N%s != 0 GOTO L%s" % (self.var, self.destino)


class Goto(Instruccion):
    """GOTO Lm"""
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


class Agregar(Instruccion):
    """Pk := Pk.a"""
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
    def __init__(self, var_dest, var_src, label=None):
        super(CopiaPalabra, self).__init__(var_dest, label)
        self.var_src = int(var_src)
        self.es_numerica = False

    def __str__(self):
        return super(CopiaPalabra, self).__str__() + "P%s <- P%s" % (self.var, self.var_src)


class IfAlfabetico(Instruccion):
    """IF Pk BEGINS a GOTO Lm"""
    def __init__(self, var, simbolo, destino, label=None):
        super(IfAlfabetico, self).__init__(var, label)
        self.destino = int(destino)
        self.simbolo = str(simbolo)
        self.es_numerica = False

    def __str__(self):
        return super(IfAlfabetico, self).__str__() + "IF P%s BEGINS %s GOTO L%s" % (
            self.var, self.simbolo, self.destino)
