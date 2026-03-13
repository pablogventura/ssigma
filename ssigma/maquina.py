# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# Máquina de ejecución: estado (i, s⃗, σ⃗) y transición S_P.

from .programa import Programa
from .infinitupla import Infinitupla
from .ejecutor import ejecutar_paso


class Ejecucion(object):
    """Máquina de ejecución S_P. Estado: linea (índice), numericas (s⃗), alfabeticas (σ⃗)."""
    def __init__(self, programa):
        if not isinstance(programa, Programa):
            raise TypeError("programa debe ser una instancia de Programa")
        self.programa = programa
        self.numericas = Infinitupla(True)
        self.alfabeticas = Infinitupla(False)
        self.linea = 0
        self.termino = False
        self.debug = True
        self.num_pasos = 0

    def reset(self):
        self.numericas = Infinitupla(True)
        self.alfabeticas = Infinitupla(False)
        self.linea = 0
        self.termino = False
        self.num_pasos = 0

    def orquilla_numerica(self, n_numericos, n_alfabeticos):
        """Devuelve una función (n₁,…,nₙ, p₁,…,pₘ) → N1 al terminar (Ψ_P^{n,m,#})."""
        params = ["n%s" % (i + 1) for i in range(n_numericos)]
        params += ["p%s" % (i + 1) for i in range(n_alfabeticos)]
        codigo = "def result(" + ", ".join(params) + "):\n"
        for i in range(n_numericos):
            codigo += "  self.numericas[%s] = n%s\n" % (i + 1, i + 1)
        for i in range(n_alfabeticos):
            codigo += "  self.alfabeticas[%s] = p%s\n" % (i + 1, i + 1)
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
        """Un paso de transición: ejecuta la instrucción actual o marca terminación."""
        if 0 <= self.linea < len(self.programa.ins):
            self.num_pasos += 1
            inst = self.programa.ins[self.linea]
            if self.debug:
                if inst.var != 0:
                    if inst.es_numerica:
                        print("%s:\t%s\t N%s=%s" % (
                            self.linea, inst, inst.var, self.numericas[inst.var]))
                    else:
                        print("%s:\t%s\t P%s=%s" % (
                            self.linea, inst, inst.var, self.alfabeticas[inst.var]))
                else:
                    print("%s:\t%s" % (self.linea, inst))
            ejecutar_paso(inst, self)
        else:
            self.termino = True

    def __str__(self):
        return "Variables Numericas: %s\nVariables Alfabeticas: %s\nlinea: %s" % (
            self.numericas, self.alfabeticas, self.linea)
