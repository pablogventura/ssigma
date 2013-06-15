#!/usr/bin/env python
# -*- coding: utf8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.

class Instruccion(object):
    """
    Clase abstracta con lo general de una instruccion
    """
    def __init__(self, var, label=None):
        self.var = int(var)
        if label:
            self.label = int(label)
        else:
            self.label = label

        self.es_numerica = None # numerica o alfabetica
    
    def __str__(self):
        result = ""
        if self.label:
            result += "L%s\t" % self.label
        else:
            result += "\t"
        return result


class Sucesor(Instruccion):
    def __init__(self, var, label=None):
        super(Sucesor, self).__init__(var, label)
        self.es_numerica = True
    
    def __str__(self):
        result = super(Sucesor, self).__str__()
        result += "N%s <- N%s + 1" % (self.var, self.var)
        return result

class RestaPunto(Instruccion):
    def __init__(self, var, label=None):
        super(RestaPunto, self).__init__(var, label)
        self.es_numerica = True
    
    def __str__(self):
        result = super(RestaPunto, self).__str__()
        result += "N%s <- N%s -·- 1" % (self.var, self.var)
        return result
            
class IfNumerico(Instruccion):
    def __init__(self, var, destino, label=None):
        super(IfNumerico, self).__init__(var, label)
        self.destino = int(destino)
        self.es_numerica = True
    
    def __str__(self):
        result = super(IfNumerico, self).__str__()
        result += "IF N%s != 0 GOTO L%s" % (self.var, self.destino)
        return result


class Agregar(Instruccion):
    def __init__(self, var, simbolo, label=None):
        super(Agregar, self).__init__(var, label)
        self.simbolo = str(simbolo)
        self.es_numerica = False
        
    def __str__(self):
        result = super(Agregar, self).__str__()
        result += "P%s <- P%s%s" % (self.var, self.var, self.simbolo)
        return result

class Quitar(Instruccion):
    def __init__(self, var, label=None):
        super(Quitar, self).__init__(var, label)
        self.es_numerica = False
    
    def __str__(self):
        result = super(Quitar, self).__str__()
        result += "P%s <- ^P%s" % (self.var, self.var)
        return result
            
class IfAlfabetico(Instruccion):
    def __init__(self, var, simbolo, destino, label=None):
        super(IfAlfabetico, self).__init__(var, label)
        self.destino = int(destino)
        self.simbolo = str(simbolo)
        self.es_numerica = False
    
    def __str__(self):
        result = super(IfAlfabetico, self).__str__()
        result += "IF P%s BEGINS %s GOTO L%s" % (self.var, self.simbolo, self.destino)
        return result

