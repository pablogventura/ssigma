#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script de prueba para S-Sigma.

import os
from ssigma import Parser, Ejecucion, Programa, registro_por_defecto

def main():
    # Test 1: programa desde archivo (como antes)
    p = Parser()
    ruta = os.path.join(os.path.dirname(__file__), "examples", "devuelveunoconh.code")
    prog = p.programa_desde_archivo(ruta)
    e = Ejecucion(prog)
    f = e.orquilla_numerica(0, 1)  # 0 numéricos, 1 alfabético (P1)
    result = f("g")
    print("Resultado N1:", result)

    # Test 2: macro SUMA por API — N1 <- N2 + N3
    reg = registro_por_defecto()
    expansion = reg.expandir_llamada("SUMA", [1, 2, 3])  # V1=1, V2=2, V3=3
    prog_suma = Programa(expansion)
    e2 = Ejecucion(prog_suma)
    e2.numericas[2] = 4
    e2.numericas[3] = 5
    e2.ejecutar()
    assert e2.numericas[1] == 9, "SUMA(4,5) debe ser 9"
    print("SUMA(N2,N3) con N2=4, N3=5 -> N1=%s (ok)" % e2.numericas[1])

    # Test 3: parser con macro SUMA en código
    p_macro = Parser(registro_macros=reg)
    linea = "SUMA(N1, N2, N3)"
    insts = p_macro.instruccion(linea)
    assert isinstance(insts, list) and len(insts) > 1
    prog3 = Programa(insts)
    e3 = Ejecucion(prog3)
    e3.numericas[2] = 10
    e3.numericas[3] = 7
    e3.ejecutar()
    assert e3.numericas[1] == 17
    print("Parser SUMA(N1,N2,N3) con N2=10, N3=7 -> N1=%s (ok)" % e3.numericas[1])

if __name__ == "__main__":
    main()
