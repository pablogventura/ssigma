# -*- coding: utf-8 -*-
"""CLI para ejecutar programas S^Σ desde archivos .code."""
from __future__ import print_function

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Ejecuta un programa S^Σ desde un archivo .code"
    )
    parser.add_argument(
        "archivo",
        nargs="?",
        help="Ruta al archivo .code a ejecutar",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Muestra las instrucciones al cargar y modo debug al ejecutar",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    args = parser.parse_args()

    if not args.archivo:
        parser.print_help()
        sys.exit(0)

    path = os.path.abspath(args.archivo)
    if not os.path.isfile(path):
        print("Error: no existe el archivo %r" % args.archivo, file=sys.stderr)
        sys.exit(1)

    try:
        from . import Parser, Ejecucion, registro_por_defecto
    except ImportError:
        from ssigma import Parser, Ejecucion, registro_por_defecto

    p = Parser(registro_por_defecto())
    try:
        prog = p.programa_desde_archivo(path, verbose=args.verbose)
    except Exception as e:
        print("Error al cargar el programa: %s" % e, file=sys.stderr)
        sys.exit(1)

    e = Ejecucion(prog)
    e.debug = args.verbose
    try:
        e.ejecutar()
    except Exception as err:
        print("Error durante la ejecución: %s" % err, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
