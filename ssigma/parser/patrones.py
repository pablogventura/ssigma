# -*- coding: utf-8 -*-
# Patrones regex y fabricas para cada tipo de instrucción.
# Orden: más específicos primero (p. ej. GOTO antes que IF).

import re
from ..instrucciones import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
    Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico,
)


def _sucesor(m):
    return Sucesor(m.group("var1")) if m.group("var1") == m.group("var2") else None


def _restapunto(m):
    return RestaPunto(m.group("var1")) if m.group("var1") == m.group("var2") else None


def _agregar(m):
    if m.group("var1") != m.group("var2") or len(m.group("simbolo")) != 1:
        return None
    return Agregar(m.group("var1"), m.group("simbolo"))


def _quitar(m):
    return Quitar(m.group("var1")) if m.group("var1") == m.group("var2") else None


def _ifalfabetico(m):
    return IfAlfabetico(m.group("var"), m.group("simbolo"), m.group("destino")) if len(m.group("simbolo")) == 1 else None


# Lista (patrón, fábrica). La fábrica recibe el match y devuelve Instruccion o None.
PATRONES = [
    (r"^[ ]*GOTO[ ]*L(?P<destino>[0-9]+)[ ]*$", lambda m: Goto(m.group("destino"))),
    (r"^[ ]*SKIP[ ]*$", lambda m: Skip()),
    (r"^[ ]*N(?P<var1>[0-9]+)[ ]*<-[ ]*N(?P<var2>[0-9]+)[ ]*\+[ ]*1[ ]*$", _sucesor),
    (r"^[ ]*N(?P<var1>[0-9]+)[ ]*<-[ ]*N(?P<var2>[0-9]+)[ ]*-·-[ ]*1[ ]*$", _restapunto),
    (r"^[ ]*N(?P<var>[0-9]+)[ ]*<-[ ]*0[ ]*$", lambda m: Cero(m.group("var"))),
    (r"^[ ]*N(?P<var1>[0-9]+)[ ]*<-[ ]*N(?P<var2>[0-9]+)[ ]*$", lambda m: CopiaNumerica(m.group("var1"), m.group("var2"))),
    (r"^[ ]*IF[ ]*N(?P<var>[0-9]+)[ ]*!=[ ]*0[ ]*GOTO[ ]*L(?P<destino>[0-9]+)[ ]*$", lambda m: IfNumerico(m.group("var"), m.group("destino"))),
    (r"^[ ]*P(?P<var1>[0-9]+)[ ]*<-[ ]*P(?P<var2>[0-9]+)[ ]*(?P<simbolo>.)[ ]*$", _agregar),
    (r"^[ ]*P(?P<var1>[0-9]+)[ ]*<-[ ]*\^P(?P<var2>[0-9]+)[ ]*$", _quitar),
    (r"^[ ]*P(?P<var>[0-9]+)[ ]*<-[ ]*EPSILON[ ]*$", lambda m: VaciarPalabra(m.group("var"))),
    (r"^[ ]*P(?P<var1>[0-9]+)[ ]*<-[ ]*P(?P<var2>[0-9]+)[ ]*$", lambda m: CopiaPalabra(m.group("var1"), m.group("var2"))),
    (r"^[ ]*IF[ ]*P(?P<var>[0-9]+)[ ]*BEGINS[ ]*(?P<simbolo>[^ ]*)[ ]*GOTO[ ]*L(?P<destino>[0-9]+)[ ]*$", _ifalfabetico),
]

REGEX_LABEL = re.compile(r"^[ ]*L(?P<label>[0-9]+)[ ]*(?P<resto>.*)$")
