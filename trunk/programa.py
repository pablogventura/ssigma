#!/usr/bin/env python
# -*- coding: utf8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.

from instruccion import *
from infinitupla import *
import pickle

def cargar_programa(path):
    f = open(path,"rb")
    result = pickle.load(f)
    f.close()
    return result

def guardar_programa(programa, path):
    f = open(path,"w")
    pickle.dump(programa,f,pickle.HIGHEST_PROTOCOL)
    f.close()

class Programa(object):
    def __init__(self, instrucciones=[]):
        assert type(instrucciones) == list, "no es lista"
        self.ins = instrucciones
        
        for i in self.ins:
            if type(i) in [IfAlfabetico, IfNumerico]:
                self.encontrar_label(i.destino)
    
    def encontrar_label(self, label):
        for i in self.ins:
            if i.label == label:
                return self.ins.index(i)
        
        assert False, "no existe el label %s" % label
    
    def __str__(self):
        result = ""
        for i in self.ins:
            result += i.__str__() + "\r\n"
        return result


class Ejecucion(object):
    def __init__(self, programa):
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
        codigo = "def result("
        for i in range(numericos):
            codigo += "n%s, " % (i+1)
        for i in range(alfabeticos):
            codigo += "p%s, " % (i+1)
        codigo += "):\r\n "
        for i in range(numericos):
            codigo += "self.numericas[%s] = n%s \r\n " % (i+1,i+1)
        for i in range(alfabeticos):
            codigo += "self.alfabeticas[%s] = p%s \r\n " % (i+1,i+1)
        codigo += "self.ejecutar()\r\n r = self.numericas[1]\r\n "
        codigo += "self.reset()\r\n return r\r\n"
        exec codigo in locals()
        return result
    
    def ejecutar(self, pasos=None):
        if pasos:
            for i in range(pasos):
                self.paso()
        else:
            while not self.termino:
                self.paso()

    def paso(self):
        if 0 <= self.linea < len(self.programa.ins):
            linea = self.programa.ins[self.linea]
            if self.debug:
                if linea.es_numerica:
                    print "%s:\t%s\t N%s=%s" % (self.linea, linea, linea.var, self.numericas[linea.var])
                else:
                    print "%s:\t%s\t P%s=%s" % (self.linea, linea, linea.var, self.alfabeticas[linea.var])
        
            if linea.es_numerica:
                if type(linea) == Sucesor:
                    self.numericas[linea.var] += 1
                    self.linea += 1
                elif type(linea) == RestaPunto:
                    self.numericas[linea.var] = max(0, self.numericas[linea.var] - 1)
                    self.linea += 1
                elif type(linea) == IfNumerico:
                    if self.numericas[linea.var] != 0:
                        self.linea = self.programa.encontrar_label(linea.destino)
                    else:
                        self.linea += 1
                        
            else: # es alfabetica
                if type(linea) == Agregar:
                    self.alfabeticas[linea.var] += linea.simbolo
                    self.linea += 1
                elif type(linea) == Quitar:
                    self.alfabeticas[linea.var] = self.alfabeticas[linea.var][1:]
                    self.linea += 1
                elif type(linea) == IfAlfabetico:

                    if self.alfabeticas[linea.var].startswith(linea.simbolo):
                        self.linea = self.programa.encontrar_label(linea.destino)
                    else:
                        self.linea += 1
        else: # no hay linea con ese numero
            self.termino = True
                    
    def descripcion_instantanea(self):
        pass
        
    def __str__(self):
        result = "Variables Numericas: %s\r\n" % (self.numericas)
        result += "Variables Alfabeticas: %s\r\n" % (self.alfabeticas)
        result += "linea: %s" % self.linea
        
        return result
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
