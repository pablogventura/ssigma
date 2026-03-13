# -*- coding: utf-8 -*-
# Excepciones propias del paquete S-Sigma.


class SSigmaError(Exception):
    """Base para errores de S-Sigma."""
    pass


class ParseError(SSigmaError):
    """Error al parsear una línea del programa."""
    def __init__(self, mensaje, linea=None):
        self.linea = linea
        super(ParseError, self).__init__(mensaje)


class LabelNotFoundError(SSigmaError):
    """No existe ninguna instrucción con el label referenciado."""
    def __init__(self, label):
        self.label = label
        super(LabelNotFoundError, self).__init__("no existe el label %s" % label)
