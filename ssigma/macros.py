# -*- coding: utf-8 -*-
# Macros: plantillas con variables de macro (Vn, Wn, An) y expansión por sustitución.
# Definición formal: definicion/def.html sección 4.3.4.

import re
from .instrucciones import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
    Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico,
)
from .exceptions import SSigmaError


class MacroError(SSigmaError):
    """Error en definición o expansión de macro."""
    pass


def _param_refs_en_cuerpo(body):
    """Recorre body y devuelve set de nombres de parámetros (Vn, Wn, An) usados."""
    refs = set()
    for d in body:
        for k, v in d.items():
            if k == "tipo":
                continue
            if isinstance(v, str) and (v.startswith("V") or v.startswith("W") or v.startswith("A")):
                refs.add(v)
    return refs


def _construir_sustitucion_completa(param_names, sustitucion_oficial, body,
                                     aux_var_inicio=1000, aux_label_inicio=1000):
    """
    sustitucion_oficial: dict nombre -> int (solo parámetros oficiales).
    Devuelve dict completo: todos los nombres que aparecen en body mapeados a int.
    Los auxiliares (no en param_names) reciben números frescos.
    """
    refs = _param_refs_en_cuerpo(body)
    oficiales = set(param_names)
    auxiliares = refs - oficiales
    # Separar auxiliares en variables (V,W) y labels (A)
    aux_vars = sorted(r for r in auxiliares if r[0] in "VW")
    aux_labels = sorted(r for r in auxiliares if r[0] == "A")
    sustitucion = dict(sustitucion_oficial)
    for i, name in enumerate(aux_vars):
        sustitucion[name] = aux_var_inicio + i
    for i, name in enumerate(aux_labels):
        sustitucion[name] = aux_label_inicio + i
    return sustitucion


def _valor(k, d, sustitucion):
    """Valor del campo k en el template d: int o sustitución de nombre."""
    v = d.get(k)
    if v is None:
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str) and v in sustitucion:
        return sustitucion[v]
    raise MacroError("parámetro de macro no resuelto: %s (clave %s)" % (v, k))


def _instruccion_desde_template(d, sustitucion):
    """Construye una Instruccion a partir de un dict plantilla y la sustitución."""
    tipo = d.get("tipo")
    label = d.get("label")
    label = _valor("label", d, sustitucion) if isinstance(d.get("label"), str) else label
    if tipo == "Sucesor":
        return Sucesor(_valor("var", d, sustitucion), label=label)
    if tipo == "RestaPunto":
        return RestaPunto(_valor("var", d, sustitucion), label=label)
    if tipo == "Cero":
        return Cero(_valor("var", d, sustitucion), label=label)
    if tipo == "CopiaNumerica":
        return CopiaNumerica(
            _valor("var_dest", d, sustitucion),
            _valor("var_src", d, sustitucion),
            label=label,
        )
    if tipo == "IfNumerico":
        return IfNumerico(
            _valor("var", d, sustitucion),
            _valor("destino", d, sustitucion),
            label=label,
        )
    if tipo == "Goto":
        return Goto(_valor("destino", d, sustitucion), label=label)
    if tipo == "Skip":
        return Skip(label=label)
    if tipo == "Agregar":
        return Agregar(
            _valor("var", d, sustitucion),
            d.get("simbolo"),  # símbolo concreto, no param
            label=label,
        )
    if tipo == "Quitar":
        return Quitar(_valor("var", d, sustitucion), label=label)
    if tipo == "VaciarPalabra":
        return VaciarPalabra(_valor("var", d, sustitucion), label=label)
    if tipo == "CopiaPalabra":
        return CopiaPalabra(
            _valor("var_dest", d, sustitucion),
            _valor("var_src", d, sustitucion),
            label=label,
        )
    if tipo == "IfAlfabetico":
        return IfAlfabetico(
            _valor("var", d, sustitucion),
            d.get("simbolo"),
            _valor("destino", d, sustitucion),
            label=label,
        )
    raise MacroError("tipo de instrucción en macro no reconocido: %s" % tipo)


class Macro(object):
    """
    Macro: plantilla con variables de macro (Vn numéricas, Wn de palabra, An labels).
    param_names: lista ordenada de parámetros oficiales (los que se pasan al expandir).
    body: lista de dicts, cada uno es una plantilla de instrucción (tipo + campos).
    """
    def __init__(self, nombre, param_names, body):
        self.nombre = nombre
        self.param_names = list(param_names)
        self.body = list(body)

    def expandir(self, sustitucion_oficial, aux_var_inicio=1000, aux_label_inicio=1000):
        """
        Sustitucion_oficial: dict que mapea cada param_names a un int (índice de N, P o L).
        Devuelve lista de Instruccion (copia del cuerpo con sustitución aplicada).
        """
        if set(sustitucion_oficial) != set(self.param_names):
            raise MacroError("sustitución debe incluir exactamente %s" % self.param_names)
        sustitucion = _construir_sustitucion_completa(
            self.param_names, sustitucion_oficial, self.body,
            aux_var_inicio, aux_label_inicio,
        )
        return [_instruccion_desde_template(d, sustitucion) for d in self.body]


class RegistroMacros(object):
    """Registro de macros por nombre. Permite expandir por nombre y lista de argumentos."""
    def __init__(self):
        self._macros = {}

    def registrar(self, macro):
        if not isinstance(macro, Macro):
            raise TypeError("se espera una instancia de Macro")
        self._macros[macro.nombre.upper()] = macro

    def obtener(self, nombre):
        return self._macros.get(nombre.upper())

    def expandir_llamada(self, nombre, args, aux_var_inicio=1000, aux_label_inicio=1000):
        """
        args: secuencia de enteros (índices N/P/L) en el orden de param_names del macro.
        Devuelve lista de Instruccion.
        """
        macro = self.obtener(nombre)
        if macro is None:
            raise MacroError("macro no registrado: %s" % nombre)
        if len(args) != len(macro.param_names):
            raise MacroError("macro %s espera %s argumentos, se dieron %s" % (
                nombre, len(macro.param_names), len(args)))
        sustitucion = dict(zip(macro.param_names, args))
        return macro.expandir(sustitucion, aux_var_inicio, aux_label_inicio)


# --- Macro SUMA: [V1←SUMA(V2,V3)] simula Nk ← Nn + Nm ---
# Cuerpo: V4←V2, V5←V3, V1←V4; A1: IF V5≠0 GOTO A2; GOTO A3; A2: V5←V5−·1, V1←V1+1, GOTO A1; A3: SKIP
MACRO_SUMA_CUERPO = [
    {"tipo": "CopiaNumerica", "var_dest": "V4", "var_src": "V2"},
    {"tipo": "CopiaNumerica", "var_dest": "V5", "var_src": "V3"},
    {"tipo": "CopiaNumerica", "var_dest": "V1", "var_src": "V4"},
    {"tipo": "IfNumerico", "var": "V5", "destino": "A2", "label": "A1"},
    {"tipo": "Goto", "destino": "A3"},
    {"tipo": "RestaPunto", "var": "V5", "label": "A2"},
    {"tipo": "Sucesor", "var": "V1"},
    {"tipo": "Goto", "destino": "A1"},
    {"tipo": "Skip", "label": "A3"},
]

def macro_suma():
    """Macro de asignación: V1 ← SUMA(V2, V3). Params: V1=resultado, V2=sumando1, V3=sumando2."""
    return Macro("SUMA", ["V1", "V2", "V3"], MACRO_SUMA_CUERPO)


def registro_por_defecto():
    """Registro con los macros predefinidos (SUMA, etc.)."""
    reg = RegistroMacros()
    reg.registrar(macro_suma())
    return reg
