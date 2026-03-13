# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.

from .programa import Programa
from .infinitupla import Infinitupla
from .instrucciones import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
    Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico,
)


class Ejecucion(object):
    """Máquina de ejecución: S_P(i, s⃗, σ⃗). Estado (linea, numericas, alfabeticas)."""
    def __init__(self, programa):
        assert isinstance(programa, Programa)
        self.programa = programa
        self.numericas = Infinitupla(True)
        self.alfabeticas = Infinitupla(False)
        self.linea = 0
        self.termino = False
        self.debug = True

    def reset(self):
        self.numericas = Infinitupla(True)
        self.alfabeticas = Infinitupla(False)
        self.linea = 0
        self.termino = False

    def orquilla_numerica(self, numericos, alfabeticos):
        """Devuelve una función (n1,…, p1,…) → N1 al terminar (Ψ_P^{n,m,#})."""
        params = ["n%s" % (i+1) for i in range(numericos)]
        params += ["p%s" % (i+1) for i in range(alfabeticos)]
        codigo = "def result(" + ", ".join(params) + "):\n"
        for i in range(numericos):
            codigo += "  self.numericas[%s] = n%s\n" % (i+1, i+1)
        for i in range(alfabeticos):
            codigo += "  self.alfabeticas[%s] = p%s\n" % (i+1, i+1)
        codigo += "  self.ejecutar()\n  r = self.numericas[1]\n  self.reset()\n  return r\n"
        loc = {}
        exec(codigo, {"self": self}, loc)
        return loc["result"]

    def ejecutar(self, pasos=None):
        if pasos is not None:
            for _ in range(pasos):
                self.paso()
        else:
            while not self.termino:
                self.paso()

    def paso(self):
        """Un paso de transición S_P."""
        if 0 <= self.linea < len(self.programa.ins):
            linea = self.programa.ins[self.linea]
            if self.debug:
                if linea.es_numerica:
                    print("%s:\t%s\t N%s=%s" % (
                        self.linea, linea, linea.var, self.numericas[linea.var]))
                else:
                    print("%s:\t%s\t P%s=%s" % (
                        self.linea, linea, linea.var, self.alfabeticas[linea.var]))

            if linea.es_numerica:
                if type(linea) == Sucesor:
                    self.numericas[linea.var] += 1
                    self.linea += 1
                elif type(linea) == RestaPunto:
                    self.numericas[linea.var] = max(0, self.numericas[linea.var] - 1)
                    self.linea += 1
                elif type(linea) == Cero:
                    self.numericas[linea.var] = 0
                    self.linea += 1
                elif type(linea) == CopiaNumerica:
                    self.numericas[linea.var] = self.numericas[linea.var_src]
                    self.linea += 1
                elif type(linea) == IfNumerico:
                    if self.numericas[linea.var] != 0:
                        self.linea = self.programa.encontrar_label(linea.destino)
                    else:
                        self.linea += 1
                elif type(linea) == Goto:
                    self.linea = self.programa.encontrar_label(linea.destino)
                elif type(linea) == Skip:
                    self.linea += 1
            else:
                if type(linea) == Agregar:
                    self.alfabeticas[linea.var] += linea.simbolo
                    self.linea += 1
                elif type(linea) == Quitar:
                    self.alfabeticas[linea.var] = self.alfabeticas[linea.var][1:]
                    self.linea += 1
                elif type(linea) == VaciarPalabra:
                    self.alfabeticas[linea.var] = ""
                    self.linea += 1
                elif type(linea) == CopiaPalabra:
                    self.alfabeticas[linea.var] = self.alfabeticas[linea.var_src]
                    self.linea += 1
                elif type(linea) == IfAlfabetico:
                    if self.alfabeticas[linea.var].startswith(linea.simbolo):
                        self.linea = self.programa.encontrar_label(linea.destino)
                    else:
                        self.linea += 1
        else:
            self.termino = True

    def __str__(self):
        return ("Variables Numericas: %s\nVariables Alfabeticas: %s\nlinea: %s" % (
            self.numericas, self.alfabeticas, self.linea))
