# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.

import re
from .instrucciones import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
    Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico,
)
from .programa import Programa


class Parser(object):
    """Parser del lenguaje S^Σ. Una línea → una instrucción o None (fin)."""
    def programa_desde_archivo(self, path):
        result = []
        with open(path, "r", encoding="utf-8") as f:
            while True:
                nueva = self.instruccion(f.readline())
                if nueva is not None:
                    print(nueva)
                    result.append(nueva)
                else:
                    break
        print("-----FIN PARSEO-----")
        return Programa(result)

    def programa(self):
        result = []
        while True:
            nueva = self.instruccion(input("Linea %s:\n" % len(result)))
            if nueva is not None:
                print(nueva)
                result.append(nueva)
            else:
                break
        return Programa(result)

    def instruccion(self, linea):
        if linea is None:
            return None
        linea = linea.upper().strip()
        if not linea:
            return None
        label, resto = self.parse_label(linea)
        for parseo in [
            self.parse_goto, self.parse_skip,
            self.parse_sucesor, self.parse_restapunto, self.parse_cero,
            self.parse_copianumerica, self.parse_ifnumerico,
            self.parse_agregar, self.parse_quitar,
            self.parse_vaciarpalabra, self.parse_copiapalabra,
            self.parse_ifalfabetico,
        ]:
            inst = parseo(resto)
            if inst is not None:
                inst.label = label
                return inst
        return None

    def parse_label(self, linea):
        m = re.match(r"^[ ]*L(?P<label>[0-9]+)[ ]*(?P<resto>.*)$", linea)
        if m:
            return int(m.group("label")), m.group("resto").strip()
        return None, linea

    def parse_goto(self, linea):
        m = re.match(r"^[ ]*GOTO[ ]*L(?P<destino>[0-9]+)[ ]*$", linea)
        return Goto(m.group("destino")) if m else None

    def parse_skip(self, linea):
        m = re.match(r"^[ ]*SKIP[ ]*$", linea)
        return Skip() if m else None

    def parse_sucesor(self, linea):
        m = re.match(r"^[ ]*N(?P<var1>[0-9]+)[ ]*<-[ ]*N(?P<var2>[0-9]+)[ ]*\+[ ]*1[ ]*$", linea)
        return Sucesor(m.group("var1")) if m and m.group("var1") == m.group("var2") else None

    def parse_restapunto(self, linea):
        m = re.match(r"^[ ]*N(?P<var1>[0-9]+)[ ]*<-[ ]*N(?P<var2>[0-9]+)[ ]*-·-[ ]*1[ ]*$", linea)
        return RestaPunto(m.group("var1")) if m and m.group("var1") == m.group("var2") else None

    def parse_cero(self, linea):
        m = re.match(r"^[ ]*N(?P<var>[0-9]+)[ ]*<-[ ]*0[ ]*$", linea)
        return Cero(m.group("var")) if m else None

    def parse_copianumerica(self, linea):
        m = re.match(r"^[ ]*N(?P<var1>[0-9]+)[ ]*<-[ ]*N(?P<var2>[0-9]+)[ ]*$", linea)
        return CopiaNumerica(m.group("var1"), m.group("var2")) if m else None

    def parse_ifnumerico(self, linea):
        m = re.match(r"^[ ]*IF[ ]*N(?P<var>[0-9]+)[ ]*!=[ ]*0[ ]*GOTO[ ]*L(?P<destino>[0-9]+)[ ]*$", linea)
        return IfNumerico(m.group("var"), m.group("destino")) if m else None

    def parse_agregar(self, linea):
        m = re.match(r"^[ ]*P(?P<var1>[0-9]+)[ ]*<-[ ]*P(?P<var2>[0-9]+)(?P<simbolo>[^ ]*)[ ]*$", linea)
        if m and m.group("var1") == m.group("var2") and len(m.group("simbolo")) == 1:
            return Agregar(m.group("var1"), m.group("simbolo"))
        return None

    def parse_quitar(self, linea):
        m = re.match(r"^[ ]*P(?P<var1>[0-9]+)[ ]*<-[ ]*\^P(?P<var2>[0-9]+)[ ]*$", linea)
        return Quitar(m.group("var1")) if m and m.group("var1") == m.group("var2") else None

    def parse_vaciarpalabra(self, linea):
        m = re.match(r"^[ ]*P(?P<var>[0-9]+)[ ]*<-[ ]*EPSILON[ ]*$", linea)
        return VaciarPalabra(m.group("var")) if m else None

    def parse_copiapalabra(self, linea):
        m = re.match(r"^[ ]*P(?P<var1>[0-9]+)[ ]*<-[ ]*P(?P<var2>[0-9]+)[ ]*$", linea)
        return CopiaPalabra(m.group("var1"), m.group("var2")) if m else None

    def parse_ifalfabetico(self, linea):
        m = re.match(r"^[ ]*IF[ ]*P(?P<var>[0-9]+)[ ]*BEGINS[ ]*(?P<simbolo>[^ ]*)[ ]*GOTO[ ]*L(?P<destino>[0-9]+)[ ]*$", linea)
        return IfAlfabetico(m.group("var"), m.group("simbolo"), m.group("destino")) if m and len(m.group("simbolo")) == 1 else None
