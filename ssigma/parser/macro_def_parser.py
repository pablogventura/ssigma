# -*- coding: utf-8 -*-
# Parser de definiciones de macros: archivos con MACRO nombre params / cuerpo / ENDMACRO.
# El cuerpo usa la misma sintaxis que S^Σ pero con variables de macro Vn, Wn, An (o Nn, Pn, Ln).

import re
import os
from ..macros import Macro, RegistroMacros, MacroError


def _v(m, pre_key, num_key):
    """Construye nombre de variable/label desde grupos del match: pre_key='var1_pre', num_key='var1_num'."""
    return (m.group(pre_key) or "") + (m.group(num_key) or "")


# Patrones que aceptan N/V para variables numéricas, L/A para labels, N/P para palabras.
# Cada factory devuelve un dict plantilla (tipo + claves con valores "V1", "A2", etc.).
def _tmpl_sucesor(m):
    v1, v2 = _v(m, "v1_pre", "v1_num"), _v(m, "v2_pre", "v2_num")
    if v1 != v2:
        return None
    return {"tipo": "Sucesor", "var": v1}


def _tmpl_restapunto(m):
    v1, v2 = _v(m, "v1_pre", "v1_num"), _v(m, "v2_pre", "v2_num")
    if v1 != v2:
        return None
    return {"tipo": "RestaPunto", "var": v1}


def _tmpl_cero(m):
    return {"tipo": "Cero", "var": _v(m, "v_pre", "v_num")}


def _tmpl_copia_num(m):
    return {"tipo": "CopiaNumerica", "var_dest": _v(m, "v1_pre", "v1_num"), "var_src": _v(m, "v2_pre", "v2_num")}


def _tmpl_if_num(m):
    return {"tipo": "IfNumerico", "var": _v(m, "v_pre", "v_num"), "destino": _v(m, "d_pre", "d_num")}


def _tmpl_goto(m):
    return {"tipo": "Goto", "destino": _v(m, "d_pre", "d_num")}


def _tmpl_skip(m):
    return {"tipo": "Skip"}


def _tmpl_agregar(m):
    sim = m.group("simbolo")
    if not sim or len(sim) != 1:
        return None
    return {"tipo": "Agregar", "var": _v(m, "v1_pre", "v1_num"), "simbolo": sim}


def _tmpl_quitar(m):
    v1, v2 = _v(m, "v1_pre", "v1_num"), _v(m, "v2_pre", "v2_num")
    if v1 != v2:
        return None
    return {"tipo": "Quitar", "var": v1}


def _tmpl_vaciar(m):
    return {"tipo": "VaciarPalabra", "var": _v(m, "v_pre", "v_num")}


def _tmpl_copia_palabra(m):
    return {"tipo": "CopiaPalabra", "var_dest": _v(m, "v1_pre", "v1_num"), "var_src": _v(m, "v2_pre", "v2_num")}


def _tmpl_if_alfabetico(m):
    sim = m.group("simbolo")
    if not sim or len(sim) != 1:
        return None
    return {"tipo": "IfAlfabetico", "var": _v(m, "v_pre", "v_num"), "simbolo": sim, "destino": _v(m, "d_pre", "d_num")}


# Grupo reutilizable: variable numérica N o V
_V = r"(?P<v_pre>N|V)(?P<v_num>[0-9]+)"
_V1 = r"(?P<v1_pre>N|V)(?P<v1_num>[0-9]+)"
_V2 = r"(?P<v2_pre>N|V)(?P<v2_num>[0-9]+)"
# Variable palabra P o W
_W1 = r"(?P<v1_pre>P|W)(?P<v1_num>[0-9]+)"
_W2 = r"(?P<v2_pre>P|W)(?P<v2_num>[0-9]+)"
_W = r"(?P<v_pre>P|W)(?P<v_num>[0-9]+)"
# Label L o A
_D = r"(?P<d_pre>L|A)(?P<d_num>[0-9]+)"

PATRONES_CUERPO = [
    (r"^[ ]*GOTO[ ]*" + _D + r"[ ]*$", _tmpl_goto),
    (r"^[ ]*SKIP[ ]*$", _tmpl_skip),
    (r"^[ ]*" + _V1 + r"[ ]*<-[ ]*" + _V2 + r"[ ]*\+[ ]*1[ ]*$", _tmpl_sucesor),
    (r"^[ ]*" + _V1 + r"[ ]*<-[ ]*" + _V2 + r"[ ]*-·-[ ]*1[ ]*$", _tmpl_restapunto),
    (r"^[ ]*" + _V + r"[ ]*<-[ ]*0[ ]*$", _tmpl_cero),
    (r"^[ ]*" + _V1 + r"[ ]*<-[ ]*" + _V2 + r"[ ]*$", _tmpl_copia_num),
    (r"^[ ]*IF[ ]*" + _V + r"[ ]*!=[ ]*0[ ]*GOTO[ ]*" + _D + r"[ ]*$", _tmpl_if_num),
    (r"^[ ]*" + _W1 + r"[ ]*<-[ ]*" + _W2 + r"[ ]*(?P<simbolo>.)[ ]*$", _tmpl_agregar),
    (r"^[ ]*" + _W1 + r"[ ]*<-[ ]*\^" + _W2 + r"[ ]*$", _tmpl_quitar),
    (r"^[ ]*" + _W + r"[ ]*<-[ ]*EPSILON[ ]*$", _tmpl_vaciar),
    (r"^[ ]*" + _W1 + r"[ ]*<-[ ]*" + _W2 + r"[ ]*$", _tmpl_copia_palabra),
    (r"^[ ]*IF[ ]*" + _W + r"[ ]*BEGINS[ ]*(?P<simbolo>.)[ ]*GOTO[ ]*" + _D + r"[ ]*$", _tmpl_if_alfabetico),
]

REGEX_LABEL_CUERPO = re.compile(r"^[ ]*(?P<lab_pre>L|A)(?P<lab_num>[0-9]+)[ ]*:?[ ]*(?P<resto>.*)$")


def parsear_linea_cuerpo(linea):
    """
    Parsea una línea del cuerpo de un macro (sintaxis S^Σ con V/W/A o N/P/L).
    Devuelve (label, template_dict) donde label es None o "A1", y template_dict es el que espera Macro.
    Si la línea no es una instrucción válida, devuelve (None, None).
    """
    linea = linea.strip()
    if not linea or linea.startswith("#"):
        return None, None
    linea = linea.upper()
    label = None
    resto = linea
    m_label = REGEX_LABEL_CUERPO.match(linea)
    if m_label:
        label = _v(m_label, "lab_pre", "lab_num")
        resto = m_label.group("resto").strip()
    for patron, factory in PATRONES_CUERPO:
        m = re.match(patron, resto)
        if m:
            d = factory(m)
            if d is None:
                return None, None
            if label is not None:
                d["label"] = label
            return label, d
    return None, None


def cargar_archivo_macros(path, registro=None, encoding="utf-8"):
    """
    Lee un archivo de definición de macros y registra cada macro.
    Formato:
      MACRO nombre param1 param2 ...
      línea1 (instrucción con Vn, An, etc.)
      línea2
      ENDMACRO
    path: ruta al archivo .macros (o cualquier extensión).
    registro: RegistroMacros existente (se modifica) o None (se crea uno nuevo).
    Devuelve el registro.
    """
    if registro is None:
        registro = RegistroMacros()
    with open(path, "r", encoding=encoding) as f:
        contenido = f.read()
    lineas = contenido.splitlines()
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip().upper()
        i += 1
        if not linea or linea.startswith("#"):
            continue
        if not linea.startswith("MACRO "):
            raise MacroError("se esperaba MACRO en %s línea aprox. %d: %s" % (path, i, lineas[i-1][:50]))
        partes = linea[6:].strip().split()
        if not partes:
            raise MacroError("MACRO sin nombre en %s línea %d" % (path, i))
        nombre = partes[0]
        params = partes[1:]
        body = []
        while i < len(lineas):
            ln = lineas[i]
            i += 1
            ln_strip = ln.strip().upper()
            if ln_strip == "ENDMACRO":
                break
            if not ln_strip or ln_strip.startswith("#"):
                continue
            _, tmpl = parsear_linea_cuerpo(ln)
            if tmpl is None:
                raise MacroError("línea no válida en macro %s en %s: %s" % (nombre, path, ln[:50]))
            body.append(tmpl)
        else:
            raise MacroError("macro %s en %s no cerrada con ENDMACRO" % (nombre, path))
        if not body:
            raise MacroError("macro %s en %s tiene cuerpo vacío" % (nombre, path))
        macro = Macro(nombre, params, body)
        registro.registrar(macro)
    return registro


def cargar_macros_desde_ruta(ruta_ref, path_include, registro, encoding="utf-8"):
    """Resuelve path_include relativo al directorio de ruta_ref y carga ese archivo en registro."""
    base = os.path.dirname(os.path.abspath(ruta_ref))
    path_abs = os.path.normpath(os.path.join(base, path_include.strip()))
    return cargar_archivo_macros(path_abs, registro, encoding)
