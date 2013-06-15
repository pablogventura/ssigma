#!/usr/bin/env python
# -*- coding: utf8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.

import re
from instruccion import *
from programa import *

class Parser(object):
    def programa_desde_archivo(self, path):
        f = open(path,"rb")
        result = []
        continuar = True
        while continuar:
            nueva = self.instruccion(f.readline())
            if nueva is not None:
                print nueva
                result.append(nueva)
            else:
                print "-----FIN PARSEO-----"
                continuar = False
                f.close()
                result = Programa(result)
        return result
    
    def programa(self):
        result = []
        continuar = True
        while continuar:
            nueva = self.instruccion(raw_input("Linea %s:\r\n" % len(result)))
            if nueva is not None:
                print nueva
                result.append(nueva)
            else:
                continuar = False
                result = Programa(result)
        
        return result

    def instruccion(self, linea):

        linea = linea.upper()
        
        label, resto = self.parse_label(linea)
        
        estructuras = [self.parse_sucesor,
                       self.parse_restapunto,
                       self.parse_ifnumerico,
                       self.parse_agregar,
                       self.parse_quitar,
                       self.parse_ifalfabetico]
        
        for parseo in estructuras:
            result = parseo(resto)
            if result:
                result.label = label
                return result

    def parse_label(self, linea):
        m = re.match(r"^[ ]*L(?P<label>[0-9]+)[ ]*(?P<resto>[^$]*)", linea)
        if m:
            return int(m.group("label")),m.group("resto")
        else:
            return None,linea

    def parse_sucesor(self, linea):
        # "N%s <- N%s + 1"
        m = re.match(r"^[ ]*N(?P<var1>[0-9]+)[ ]*<-[ ]*N(?P<var2>[0-9]+)[ ]*\+[ ]*1$", linea)
        if bool(m) and m.group("var1") == m.group("var2"):
            return Sucesor(m.group("var1"))

    def parse_restapunto(self, linea):
        # "N%s <- N%s -·- 1"
        m = re.match(r"^[ ]*N(?P<var1>[0-9]+)[ ]*<-[ ]*N(?P<var2>[0-9]+)[ ]*-·-[ ]*1$", linea)
        if bool(m) and m.group("var1") == m.group("var2"):
            return RestaPunto(m.group("var1"))
            
    def parse_ifnumerico(self, linea):
        # "IF N%s != 0 GOTO L%s"
        m = re.match(r"^[ ]*IF[ ]*N(?P<var>[0-9]+)[ ]*!=[ ]*0[ ]*GOTO[ ]*L(?P<destino>[0-9]+)$", linea)
        if bool(m):
            return IfNumerico(m.group("var"),m.group("destino"))
    
    def parse_agregar(self, linea):
        # "P%s <- P%s%s"
        m = re.match(r"^[ ]*P(?P<var1>[0-9]+)[ ]*<-[ ]*P(?P<var2>[0-9]+)(?P<simbolo>[^ ]*)$", linea)
        if bool(m) and m.group("var1") == m.group("var2") and len(m.group("simbolo")) == 1:
            return Agregar(m.group("var1"), m.group("simbolo"))

    def parse_quitar(self, linea):
        # "N%s <- N%s -·- 1"
        m = re.match(r"^[ ]*P(?P<var1>[0-9]+)[ ]*<-[ ]*\^P(?P<var2>[0-9]+)", linea)
        if bool(m) and m.group("var1") == m.group("var2"):
            return Quitar(m.group("var1"))
            
    def parse_ifalfabetico(self, linea):
        # "IF N%s != 0 GOTO L%s"
        m = re.match(r"^[ ]*IF[ ]*P(?P<var>[0-9]+)[ ]*BEGINS[ ]*(?P<simbolo>[^ ]*)[ ]*GOTO[ ]*L(?P<destino>[0-9]+)$", linea)
        if bool(m) and len(m.group("simbolo")) == 1:
            return IfAlfabetico(m.group("var"),m.group("simbolo"), m.group("destino"))
            



