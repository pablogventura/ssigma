# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# Parser: líneas de texto → Programa.

import re
from ..programa import Programa
from .patrones import PATRONES, REGEX_LABEL


class Parser(object):
    """Parser del lenguaje S^Σ. Una línea → una instrucción o None (fin de programa)."""
    def programa_desde_archivo(self, path, verbose=True):
        result = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                inst = self.instruccion(line)
                if inst is not None:
                    if verbose:
                        print(inst)
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
                    print(inst)
                result.append(inst)
            else:
                break
        return Programa(result)

    def instruccion(self, linea):
        """Parsea una línea; devuelve Instruccion o None (línea vacía / fin)."""
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
        return None

    def _parse_label(self, linea):
        m = REGEX_LABEL.match(linea)
        if m:
            return int(m.group("label")), m.group("resto").strip()
        return None, linea
