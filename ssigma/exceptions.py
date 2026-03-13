# -*- coding: utf-8 -*-
# Excepciones propias del paquete S-Sigma.


def _mensaje_completo(mensaje, num_linea=None, archivo=None, fragmento=None, **kwargs):
    """Construye mensaje de error con contexto de línea y archivo."""
    partes = []
    if archivo is not None:
        partes.append("archivo %s" % archivo)
    if num_linea is not None:
        partes.append("línea %d" % num_linea)
    if partes:
        prefijo = "En " + ", ".join(partes) + ": "
    else:
        prefijo = ""
    if fragmento is not None and fragmento.strip():
        prefijo += "%r → " % (fragmento.strip()[:80],)
    return prefijo + mensaje


class SSigmaError(Exception):
    """Base para errores de S-Sigma."""
    pass


class ParseError(SSigmaError):
    """Error de sintaxis al parsear una línea del programa."""
    def __init__(self, mensaje, num_linea=None, archivo=None, fragmento=None):
        self.num_linea = num_linea
        self.archivo = archivo
        self.fragmento = fragmento
        msg = _mensaje_completo(mensaje, num_linea=num_linea, archivo=archivo, fragmento=fragmento)
        super(ParseError, self).__init__(msg)


class LabelNotFoundError(SSigmaError):
    """No existe ninguna instrucción con el label referenciado."""
    def __init__(self, label, desde_instruccion=None):
        self.label = label
        self.desde_instruccion = desde_instruccion
        msg = "No existe el label L%s." % label
        if desde_instruccion is not None:
            msg += " (referenciado desde la instrucción %d del programa)" % (desde_instruccion + 1)
        super(LabelNotFoundError, self).__init__(msg)


class ExecutionError(SSigmaError):
    """Error durante la ejecución del programa (runtime)."""
    def __init__(self, mensaje, num_instruccion=None, num_paso=None, instruccion=None):
        self.num_instruccion = num_instruccion
        self.num_paso = num_paso
        self.instruccion = instruccion
        partes = [mensaje]
        if num_instruccion is not None:
            partes.append("Instrucción del programa: %d (índice %d)." % (num_instruccion + 1, num_instruccion))
        if num_paso is not None:
            partes.append("Paso de ejecución: %d." % num_paso)
        if instruccion is not None:
            partes.append("Código: %s" % (str(instruccion)[:100],))
        msg = " ".join(partes)
        super(ExecutionError, self).__init__(msg)
