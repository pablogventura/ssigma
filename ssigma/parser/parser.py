# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# Parser: líneas de texto → Programa.

import re
from ..programa import Programa
from .patrones import PATRONES, REGEX_LABEL

# Llamada a macro: NOMBRE(Nn, Nn, ...) con N únicamente (macros numéricos).
REGEX_MACRO_LLAMADA = re.compile(
    r"^[ ]*(?P<nombre>\w+)[ ]*\([ ]*(?P<args>N[0-9]+(?:[ ]*,[ ]*N[0-9]+)*)[ ]*\)[ ]*$"
)


def _parsear_args_macro(s):
    """'N3 , N5 , N1' → [3, 5, 1]. s es la parte capturada como 'args'."""
    return [int(m) for m in re.findall(r"N([0-9]+)", s)]


class Parser(object):
    """Parser del lenguaje S^Σ. Una línea → una instrucción (o lista si es macro) o None."""
    def __init__(self, registro_macros=None):
        self.registro_macros = registro_macros

    def programa_desde_archivo(self, path, verbose=True):
        result = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                inst = self.instruccion(line)
                if inst is not None:
                    if verbose:
                        for i in (inst if isinstance(inst, list) else [inst]):
                            print(i)
                    if isinstance(inst, list):
                        result.extend(inst)
                    else:
                        result.append(inst)
                else:
                    break
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

    def instruccion(self, linea):
        """Parsea una línea; devuelve Instruccion, lista de Instruccion (macro), o None."""
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
                try:
                    expansion = self.registro_macros.expandir_llamada(nombre, args)
                except Exception:
                    return None
                if expansion and label is not None:
                    expansion[0].label = label
                return expansion
        return None

    def _parse_label(self, linea):
        m = REGEX_LABEL.match(linea)
        if m:
            return int(m.group("label")), m.group("resto").strip()
        return None, linea
