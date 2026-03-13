# -*- coding: utf-8 -*-
# Semántica: un paso de transición S_P. Despacha por tipo de instrucción.

from .instrucciones import (
    Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip,
    PrintNumerico, PrintPalabra, InputNumerico, InputPalabra,
    Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico,
)
from .exceptions import ExecutionError, LabelNotFoundError


def _ir_a_label(prog, destino, maquina, instruccion):
    """Resuelve label y actualiza maquina.linea; lanza ExecutionError si el label no existe."""
    try:
        maquina.linea = prog.encontrar_label(destino, desde_instruccion=maquina.linea)
    except LabelNotFoundError as e:
        raise ExecutionError(
            "No existe el label L%s." % e.label,
            num_instruccion=maquina.linea,
            num_paso=getattr(maquina, "num_pasos", None),
            instruccion=instruccion,
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
            _ir_a_label(prog, instruccion.destino, maquina, instruccion)
        else:
            maquina.linea += 1

    elif type(instruccion) == Goto:
        _ir_a_label(prog, instruccion.destino, maquina, instruccion)

    elif type(instruccion) == Skip:
        maquina.linea += 1

    elif type(instruccion) == PrintNumerico:
        salida = getattr(maquina, "salida", None)
        if salida is not None:
            salida.write(str(num[instruccion.var]) + "\n")
        else:
            print(num[instruccion.var])
        maquina.linea += 1

    elif type(instruccion) == PrintPalabra:
        salida = getattr(maquina, "salida", None)
        if salida is not None:
            salida.write(alf[instruccion.var] + "\n")
        else:
            print(alf[instruccion.var])
        maquina.linea += 1

    elif type(instruccion) == InputNumerico:
        entrada = getattr(maquina, "entrada", None)
        try:
            if entrada is not None:
                linea = next(entrada)
            else:
                linea = input()
        except StopIteration:
            raise ExecutionError(
                "No hay más entrada disponible para INPUT N%s (se esperaba un valor numérico)." % instruccion.var,
                num_instruccion=maquina.linea,
                num_paso=getattr(maquina, "num_pasos", None),
                instruccion=instruccion,
            )
        try:
            num[instruccion.var] = int(linea.strip())
        except ValueError:
            raise ExecutionError(
                "Entrada no numérica para INPUT N%s: %r (se esperaba un entero)." % (instruccion.var, linea[:50]),
                num_instruccion=maquina.linea,
                num_paso=getattr(maquina, "num_pasos", None),
                instruccion=instruccion,
            )
        maquina.linea += 1

    elif type(instruccion) == InputPalabra:
        entrada = getattr(maquina, "entrada", None)
        try:
            if entrada is not None:
                linea = next(entrada)
            else:
                linea = input()
        except StopIteration:
            raise ExecutionError(
                "No hay más entrada disponible para INPUT P%s." % instruccion.var,
                num_instruccion=maquina.linea,
                num_paso=getattr(maquina, "num_pasos", None),
                instruccion=instruccion,
            )
        alf[instruccion.var] = linea.strip() if isinstance(linea, str) else str(linea).strip()
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
            _ir_a_label(prog, instruccion.destino, maquina, instruccion)
        else:
            maquina.linea += 1

    else:
        raise ExecutionError(
            "Tipo de instrucción no reconocido: %s." % type(instruccion).__name__,
            num_instruccion=maquina.linea,
            num_paso=getattr(maquina, "num_pasos", None),
            instruccion=instruccion,
        )
