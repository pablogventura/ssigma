# -*- coding: utf-8 -*-
# Semántica: un paso de transición S_P. Despacha por tipo de instrucción.

from .instrucciones import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
    Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico,
)


def ejecutar_paso(instruccion, maquina):
    """
    Ejecuta una instrucción sobre la máquina (modifica estado y maquina.linea).
    No hace nada si la instrucción no es reconocida (debería no ocurrir).
    """
    prog = maquina.programa
    num = maquina.numericas
    alf = maquina.alfabeticas

    if type(instruccion) == Sucesor:
        num[instruccion.var] += 1
        maquina.linea += 1

    elif type(instruccion) == RestaPunto:
        num[instruccion.var] = max(0, num[instruccion.var] - 1)
        maquina.linea += 1

    elif type(instruccion) == Cero:
        num[instruccion.var] = 0
        maquina.linea += 1

    elif type(instruccion) == CopiaNumerica:
        num[instruccion.var] = num[instruccion.var_src]
        maquina.linea += 1

    elif type(instruccion) == IfNumerico:
        if num[instruccion.var] != 0:
            maquina.linea = prog.encontrar_label(instruccion.destino)
        else:
            maquina.linea += 1

    elif type(instruccion) == Goto:
        maquina.linea = prog.encontrar_label(instruccion.destino)

    elif type(instruccion) == Skip:
        maquina.linea += 1

    elif type(instruccion) == Agregar:
        alf[instruccion.var] += instruccion.simbolo
        maquina.linea += 1

    elif type(instruccion) == Quitar:
        alf[instruccion.var] = alf[instruccion.var][1:]
        maquina.linea += 1

    elif type(instruccion) == VaciarPalabra:
        alf[instruccion.var] = ""
        maquina.linea += 1

    elif type(instruccion) == CopiaPalabra:
        alf[instruccion.var] = alf[instruccion.var_src]
        maquina.linea += 1

    elif type(instruccion) == IfAlfabetico:
        if alf[instruccion.var].startswith(instruccion.simbolo):
            maquina.linea = prog.encontrar_label(instruccion.destino)
        else:
            maquina.linea += 1

    else:
        raise TypeError("tipo de instrucción no reconocido: %s" % type(instruccion).__name__)
