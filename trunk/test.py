#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script de prueba para S-Sigma.

import os
from ssigma import Parser, Ejecucion

def main():
    p = Parser()
    ruta = os.path.join(os.path.dirname(__file__), "examples", "devuelveunoconh.code")
    prog = p.programa_desde_archivo(ruta)
    e = Ejecucion(prog)
    f = e.orquilla_numerica(0, 1)  # 0 numéricos, 1 alfabético (P1)
    result = f("g")
    print("Resultado N1:", result)

if __name__ == "__main__":
    main()
