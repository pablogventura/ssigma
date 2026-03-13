# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# Parser: líneas de texto → Programa.

import re
import os
from ..programa import Programa
from ..instrucciones import Skip
from ..exceptions import ParseError
from .patrones import PATRONES, REGEX_LABEL
from .macro_def_parser import cargar_archivo_macros, cargar_macros_desde_ruta

# Llamada a macro: NOMBRE(Nn, Nn, ...) con N únicamente (macros numéricos).
REGEX_MACRO_LLAMADA = re.compile(
    r"^[ ]*(?P<nombre>\w+)[ ]*\([ ]*(?P<args>N[0-9]+(?:[ ]*,[ ]*N[0-9]+)*)[ ]*\)[ ]*$"
)

# INCLUDE path (relativo al archivo actual)
REGEX_INCLUDE = re.compile(r"^[ ]*INCLUDE[ ]+(.+)$", re.IGNORECASE)


def _parsear_args_macro(s):
    """'N3 , N5 , N1' → [3, 5, 1]. s es la parte capturada como 'args'."""
    return [int(m) for m in re.findall(r"N([0-9]+)", s)]


class Parser(object):
    """Parser del lenguaje S^Σ. Una línea → una instrucción (o lista si es macro) o None."""
    def __init__(self, registro_macros=None):
        self.registro_macros = registro_macros

    def programa_desde_archivo(self, path, verbose=True, macro_files=None, encoding="utf-8"):
        """
        Carga un programa desde un archivo.
        macro_files: lista opcional de rutas a archivos .macros a cargar antes (resueltas respecto al dir de path).
        Si el archivo contiene líneas INCLUDE otro.macros, se cargan esos archivos (relativos al archivo actual).
        """
        if self.registro_macros is None:
            from ..macros import RegistroMacros
            self.registro_macros = RegistroMacros()
        if macro_files:
            for mf in macro_files:
                cargar_macros_desde_ruta(path, mf, self.registro_macros, encoding)
        result = []
        next_aux = [1000]
        archivo_nombre = os.path.basename(path) if path else None
        with open(path, "r", encoding=encoding) as f:
            for num_linea, line in enumerate(f, start=1):
                linea_strip = line.strip()
                if linea_strip:
                    mm = REGEX_INCLUDE.match(linea_strip)
                else:
                    mm = None
                if mm:
                    path_include = mm.group(1).strip().strip('"\'')
                    cargar_macros_desde_ruta(path, path_include, self.registro_macros, encoding)
                    if verbose:
                        print("(INCLUDE %s)" % path_include)
                    continue
                if linea_strip.startswith("#"):
                    continue
                if not linea_strip:
                    break
                try:
                    inst = self.instruccion(line, next_aux=next_aux)
                except Exception as err:
                    raise ParseError(
                        "error al expandir macro o instrucción: %s" % err,
                        num_linea=num_linea,
                        archivo=archivo_nombre,
                        fragmento=line
                    )
                if inst is not None:
                    if verbose:
                        for i in (inst if isinstance(inst, list) else [inst]):
                            print(i)
                    if isinstance(inst, list):
                        result.extend(inst)
                    else:
                        result.append(inst)
                else:
                    raise ParseError(
                        "instrucción no reconocida (sintaxis inválida o macro no registrada). "
                        "Formato esperado: Nk<-0, Nk<-Nn, Nk<-Nk+1, Nk<-Nk-·-1, IF Nk!=0 GOTO Lm, GOTO Lm, SKIP, PRINT Nk, INPUT Nk, o MACRO(Na,Nb,...)",
                        num_linea=num_linea,
                        archivo=archivo_nombre,
                        fragmento=line
                    )
        if verbose:
            print("-----FIN PARSEO-----")
        return Programa(result)

    def programa(self, prompt=True):
        """Lee instrucciones desde stdin hasta una línea vacía."""
        result = []
        while True:
            linea = input("Linea %s:\n" % len(result)) if prompt else input()
            inst = self.instruccion(linea)
            if inst is not None:
                if prompt:
                    for i in (inst if isinstance(inst, list) else [inst]):
                        print(i)
                if isinstance(inst, list):
                    result.extend(inst)
                else:
                    result.append(inst)
            else:
                break
        return Programa(result)

    def instruccion(self, linea, next_aux=None):
        """Parsea una línea; devuelve Instruccion, lista de Instruccion (macro), o None.
        next_aux: lista [int] opcional; se usa y actualiza para labels/vars auxiliares únicos por expansión."""
        if linea is None:
            return None
        linea = linea.upper().strip()
        if not linea:
            return None
        label, resto = self._parse_label(linea)
        for patron, factory in PATRONES:
            m = re.match(patron, resto)
            if m:
                inst = factory(m)
                if inst is not None:
                    inst.label = label
                    return inst
        if self.registro_macros:
            mm = REGEX_MACRO_LLAMADA.match(resto)
            if mm:
                nombre = mm.group("nombre")
                args_str = mm.group("args")
                args = _parsear_args_macro(args_str)
                aux = next_aux[0] if next_aux is not None else 1000
                expansion = self.registro_macros.expandir_llamada(
                    nombre, args, aux_var_inicio=aux, aux_label_inicio=aux
                )
                if next_aux is not None:
                    next_aux[0] = aux + max(len(expansion), 50)
                if expansion and label is not None:
                    return [Skip(label=label)] + expansion
                return expansion
        return None

    def _parse_label(self, linea):
        m = REGEX_LABEL.match(linea)
        if m:
            resto = m.group("resto").strip()
            if resto.startswith(":"):
                resto = resto[1:].strip()
            return int(m.group("label")), resto
        return None, linea
