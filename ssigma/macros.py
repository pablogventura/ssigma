# -*- coding: utf-8 -*-
# Macros: plantillas con variables de macro (Vn, Wn, An) y expansión por sustitución.
# Definición formal: definicion/def.html sección 4.3.4.
#
# Macros predefinidos (registro_por_defecto()):
#   Asignación (resultado en V1, args N/V):
#     SUMA(V1,V2,V3)   N1 := N2 + N3
#     RESTA(V1,V2,V3)  N1 := N2 −· N3 (monus)
#     MULT(V1,V2,V3)   N1 := N2 * N3
#     PRED(V1,V2)      N1 := N2 −· 1
#     DOBLE(V1,V2)     N1 := 2*N2
#     MAX(V1,V2,V3)    N1 := max(N2,N3)
#     MIN(V1,V2,V3)    N1 := min(N2,N3)
#   Predicados (saltan al label A1 si se cumple; usar vía API con [var, label] o [v1, v2, label]):
#     IF_CERO(V1, A1)     si N_V1==0 salta a A1
#     IF_IGUAL(V1,V2, A1) si N_V1==N_V2 salta a A1
#     IF_MENOR(V1,V2, A1) si N_V1 < N_V2 salta a A1

import re
from .instrucciones import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
    PrintNumerico, PrintPalabra, InputNumerico, InputPalabra,
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
    if tipo == "PrintNumerico":
        return PrintNumerico(_valor("var", d, sustitucion), label=label)
    if tipo == "PrintPalabra":
        return PrintPalabra(_valor("var", d, sustitucion), label=label)
    if tipo == "InputNumerico":
        return InputNumerico(_valor("var", d, sustitucion), label=label)
    if tipo == "InputPalabra":
        return InputPalabra(_valor("var", d, sustitucion), label=label)
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

# --- RESTA (monus): V1 ← V2 −· V3 = max(0, V2-V3) ---
MACRO_RESTA_CUERPO = [
    {"tipo": "CopiaNumerica", "var_dest": "V1", "var_src": "V2"},
    {"tipo": "CopiaNumerica", "var_dest": "V4", "var_src": "V3"},
    {"tipo": "IfNumerico", "var": "V4", "destino": "A2", "label": "A1"},
    {"tipo": "Goto", "destino": "A4"},
    {"tipo": "RestaPunto", "var": "V4", "label": "A2"},
    {"tipo": "IfNumerico", "var": "V1", "destino": "A3"},
    {"tipo": "Goto", "destino": "A1"},
    {"tipo": "RestaPunto", "var": "V1", "label": "A3"},
    {"tipo": "Goto", "destino": "A1"},
    {"tipo": "Skip", "label": "A4"},
]

# --- MULT: V1 ← V2 * V3 (V1=0; repetir V3 veces: V1+=V2) ---
# V1←0, V4←V3. A1: IF V4!=0 GOTO A2; GOTO A6. A2: V5←V1, V6←V2 (V1+=V2 con subbucle). A3: IF V6!=0 GOTO A4; GOTO A5. A4: V6--, V1++, GOTO A3. A5: V4--, GOTO A1. A6: SKIP
MACRO_MULT_CUERPO = [
    {"tipo": "Cero", "var": "V1"},
    {"tipo": "CopiaNumerica", "var_dest": "V4", "var_src": "V3"},
    {"tipo": "IfNumerico", "var": "V4", "destino": "A2", "label": "A1"},
    {"tipo": "Goto", "destino": "A6"},
    {"tipo": "CopiaNumerica", "var_dest": "V5", "var_src": "V1", "label": "A2"},
    {"tipo": "CopiaNumerica", "var_dest": "V6", "var_src": "V2"},
    {"tipo": "CopiaNumerica", "var_dest": "V1", "var_src": "V5"},
    {"tipo": "IfNumerico", "var": "V6", "destino": "A4", "label": "A3"},
    {"tipo": "Goto", "destino": "A5"},
    {"tipo": "RestaPunto", "var": "V6", "label": "A4"},
    {"tipo": "Sucesor", "var": "V1"},
    {"tipo": "Goto", "destino": "A3"},
    {"tipo": "RestaPunto", "var": "V4", "label": "A5"},
    {"tipo": "Goto", "destino": "A1"},
    {"tipo": "Skip", "label": "A6"},
]

# --- PRED: V1 ← V2 −· 1 (predecesor, mínimo 0) ---
MACRO_PRED_CUERPO = [
    {"tipo": "CopiaNumerica", "var_dest": "V1", "var_src": "V2"},
    {"tipo": "RestaPunto", "var": "V1"},
]

# --- DOBLE: V1 ← 2 * V2 ---
MACRO_DOBLE_CUERPO = [
    {"tipo": "Cero", "var": "V1"},
    {"tipo": "CopiaNumerica", "var_dest": "V4", "var_src": "V2"},
    {"tipo": "IfNumerico", "var": "V4", "destino": "A2", "label": "A1"},
    {"tipo": "Goto", "destino": "A3"},
    {"tipo": "Sucesor", "var": "V1", "label": "A2"},
    {"tipo": "Sucesor", "var": "V1"},
    {"tipo": "RestaPunto", "var": "V4"},
    {"tipo": "Goto", "destino": "A1"},
    {"tipo": "Skip", "label": "A3"},
]

# --- MAX: V1 ← max(V2, V3). V1←V2, copiar V2,V3 a V4,V5, bucle decrementar ambos; si V5==0 queda V2, si V4==0 V1←V3 ---
MACRO_MAX_CUERPO = [
    {"tipo": "CopiaNumerica", "var_dest": "V1", "var_src": "V2"},
    {"tipo": "CopiaNumerica", "var_dest": "V4", "var_src": "V2"},
    {"tipo": "CopiaNumerica", "var_dest": "V5", "var_src": "V3"},
    {"tipo": "IfNumerico", "var": "V4", "destino": "A2", "label": "A1"},
    {"tipo": "Goto", "destino": "A4"},
    {"tipo": "IfNumerico", "var": "V5", "destino": "A3", "label": "A2"},
    {"tipo": "Goto", "destino": "A5"},
    {"tipo": "RestaPunto", "var": "V4", "label": "A3"},
    {"tipo": "RestaPunto", "var": "V5"},
    {"tipo": "Goto", "destino": "A1"},
    {"tipo": "IfNumerico", "var": "V5", "destino": "A6", "label": "A4"},
    {"tipo": "Goto", "destino": "A5"},
    {"tipo": "CopiaNumerica", "var_dest": "V1", "var_src": "V3", "label": "A6"},
    {"tipo": "Skip", "label": "A5"},
]

# --- MIN: V1 ← min(V2, V3) ---
MACRO_MIN_CUERPO = [
    {"tipo": "CopiaNumerica", "var_dest": "V1", "var_src": "V2"},
    {"tipo": "CopiaNumerica", "var_dest": "V4", "var_src": "V2"},
    {"tipo": "CopiaNumerica", "var_dest": "V5", "var_src": "V3"},
    {"tipo": "IfNumerico", "var": "V4", "destino": "A2", "label": "A1"},
    {"tipo": "Goto", "destino": "A4"},
    {"tipo": "IfNumerico", "var": "V5", "destino": "A3", "label": "A2"},
    {"tipo": "Goto", "destino": "A6"},
    {"tipo": "RestaPunto", "var": "V4", "label": "A3"},
    {"tipo": "RestaPunto", "var": "V5"},
    {"tipo": "Goto", "destino": "A1"},
    {"tipo": "IfNumerico", "var": "V5", "destino": "A6", "label": "A4"},
    {"tipo": "Goto", "destino": "A5"},
    {"tipo": "CopiaNumerica", "var_dest": "V1", "var_src": "V3", "label": "A6"},
    {"tipo": "Skip", "label": "A5"},
]

# --- IF_CERO(V1, A1): si N_V1==0 salta a A1. IF V1!=0 GOTO A2; GOTO A1; A2: SKIP ---
MACRO_IF_CERO_CUERPO = [
    {"tipo": "IfNumerico", "var": "V1", "destino": "A2"},
    {"tipo": "Goto", "destino": "A1"},
    {"tipo": "Skip", "label": "A2"},
]

# --- IF_IGUAL(V1, V2, A1): si N_V1==N_V2 salta a A1. A0 = inicio del bucle (aux). ---
MACRO_IF_IGUAL_CUERPO = [
    {"tipo": "CopiaNumerica", "var_dest": "V3", "var_src": "V1"},
    {"tipo": "CopiaNumerica", "var_dest": "V4", "var_src": "V2"},
    {"tipo": "IfNumerico", "var": "V3", "destino": "A2", "label": "A0"},
    {"tipo": "Goto", "destino": "A4"},
    {"tipo": "IfNumerico", "var": "V4", "destino": "A3", "label": "A2"},
    {"tipo": "Goto", "destino": "A5"},
    {"tipo": "RestaPunto", "var": "V3", "label": "A3"},
    {"tipo": "RestaPunto", "var": "V4"},
    {"tipo": "Goto", "destino": "A0"},
    {"tipo": "IfNumerico", "var": "V4", "destino": "A5", "label": "A4"},
    {"tipo": "Goto", "destino": "A1", "label": "A6"},
    {"tipo": "Skip", "label": "A5"},
]

# --- IF_MENOR(V1, V2, A1): si N_V1 < N_V2 salta a A1. A0 = inicio bucle (aux). ---
MACRO_IF_MENOR_CUERPO = [
    {"tipo": "CopiaNumerica", "var_dest": "V3", "var_src": "V1"},
    {"tipo": "CopiaNumerica", "var_dest": "V4", "var_src": "V2"},
    {"tipo": "IfNumerico", "var": "V3", "destino": "A2", "label": "A0"},
    {"tipo": "Goto", "destino": "A4"},
    {"tipo": "IfNumerico", "var": "V4", "destino": "A3", "label": "A2"},
    {"tipo": "Goto", "destino": "A5"},
    {"tipo": "RestaPunto", "var": "V3", "label": "A3"},
    {"tipo": "RestaPunto", "var": "V4"},
    {"tipo": "Goto", "destino": "A0"},
    {"tipo": "IfNumerico", "var": "V4", "destino": "A6", "label": "A4"},
    {"tipo": "Goto", "destino": "A5"},
    {"tipo": "Goto", "destino": "A1", "label": "A6"},
    {"tipo": "Skip", "label": "A5"},
]


def macro_suma():
    """V1 ← SUMA(V2, V3) = N_V1 := N_V2 + N_V3."""
    return Macro("SUMA", ["V1", "V2", "V3"], MACRO_SUMA_CUERPO)


def macro_resta():
    """V1 ← RESTA(V2, V3) = N_V1 := N_V2 −· N_V3 (monus, mínimo 0)."""
    return Macro("RESTA", ["V1", "V2", "V3"], MACRO_RESTA_CUERPO)


def macro_mult():
    """V1 ← MULT(V2, V3) = N_V1 := N_V2 * N_V3."""
    return Macro("MULT", ["V1", "V2", "V3"], MACRO_MULT_CUERPO)


def macro_pred():
    """V1 ← PRED(V2) = N_V1 := N_V2 −· 1 (predecesor)."""
    return Macro("PRED", ["V1", "V2"], MACRO_PRED_CUERPO)


def macro_doble():
    """V1 ← DOBLE(V2) = N_V1 := 2 * N_V2."""
    return Macro("DOBLE", ["V1", "V2"], MACRO_DOBLE_CUERPO)


def macro_max():
    """V1 ← MAX(V2, V3) = N_V1 := max(N_V2, N_V3)."""
    return Macro("MAX", ["V1", "V2", "V3"], MACRO_MAX_CUERPO)


def macro_min():
    """V1 ← MIN(V2, V3) = N_V1 := min(N_V2, N_V3)."""
    return Macro("MIN", ["V1", "V2", "V3"], MACRO_MIN_CUERPO)


def macro_if_cero():
    """IF_CERO(V1, A1): si N_V1==0 salta al label A1."""
    return Macro("IF_CERO", ["V1", "A1"], MACRO_IF_CERO_CUERPO)


def macro_if_igual():
    """IF_IGUAL(V1, V2, A1): si N_V1==N_V2 salta al label A1."""
    return Macro("IF_IGUAL", ["V1", "V2", "A1"], MACRO_IF_IGUAL_CUERPO)


def macro_if_menor():
    """IF_MENOR(V1, V2, A1): si N_V1 < N_V2 salta al label A1."""
    return Macro("IF_MENOR", ["V1", "V2", "A1"], MACRO_IF_MENOR_CUERPO)


def registro_por_defecto():
    """Registro con todos los macros predefinidos."""
    reg = RegistroMacros()
    reg.registrar(macro_suma())
    reg.registrar(macro_resta())
    reg.registrar(macro_mult())
    reg.registrar(macro_pred())
    reg.registrar(macro_doble())
    reg.registrar(macro_max())
    reg.registrar(macro_min())
    reg.registrar(macro_if_cero())
    reg.registrar(macro_if_igual())
    reg.registrar(macro_if_menor())
    return reg
