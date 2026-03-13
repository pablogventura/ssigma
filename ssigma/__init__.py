# -*- coding: utf-8 -*-
# S-Sigma: implementación del lenguaje S^Σ (paradigma imperativo de Neumann).
# Definición formal: definicion/def.html (sección 4.3), definicion/RESUMEN_LENGUAJE_S_SIGMA.md

from .parser import Parser
from .programa import Programa, cargar_programa, guardar_programa
from .maquina import Ejecucion
from .infinitupla import Infinitupla
from .instrucciones import (
    Instruccion, Sucesor, RestaPunto, Cero, CopiaNumerica,
    IfNumerico, Goto, Skip,
    Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico,
)

__all__ = [
    "Parser", "Programa", "Ejecucion", "Infinitupla",
    "cargar_programa", "guardar_programa",
    "Instruccion", "Sucesor", "RestaPunto", "Cero", "CopiaNumerica",
    "IfNumerico", "Goto", "Skip",
    "Agregar", "Quitar", "VaciarPalabra", "CopiaPalabra", "IfAlfabetico",
]
