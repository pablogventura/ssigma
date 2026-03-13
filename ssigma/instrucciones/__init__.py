# -*- coding: utf-8 -*-
# AST del lenguaje S^Σ. Instrucciones base, numéricas/control y palabras.

from .base import Instruccion
from .numericas import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
)
from .palabras import Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico

# Instrucciones que referencian un label (para validación en Programa)
INSTRUCCIONES_CON_DESTINO = (IfNumerico, IfAlfabetico, Goto)

__all__ = [
    "Instruccion",
    "Sucesor", "RestaPunto", "Cero", "CopiaNumerica", "IfNumerico", "Goto", "Skip",
    "Agregar", "Quitar", "VaciarPalabra", "CopiaPalabra", "IfAlfabetico",
    "INSTRUCCIONES_CON_DESTINO",
]
