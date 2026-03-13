#!/usr/bin/env python3
"""
1. Elimina bloques matrix+aligned duplicados.
2. Elimina bloques {{}\protect\hypertarget{MathJax-Element-...}}} que acaban en }}}}\( o }}}}\[
   (emparejando llaves correctamente).
"""
import re

with open("def.tex", "r", encoding="utf-8") as f:
    content = f.read()

# 1) Matrix + aligned
MARKER = r'\end{matrix}\]}}}}\[\begin{aligned}'
out = []
i = 0
n = len(content)
while i < n:
    idx = content.find(MARKER, i)
    if idx == -1:
        out.append(content[i:])
        break
    start = idx
    depth = 0
    j = idx - 1
    while j >= 0:
        if content[j] == '}':
            depth += 1
        elif content[j] == '{':
            depth -= 1
            if depth == 0 and j > 0:
                chunk = content[j:j+60]
                if '\\protect\\hypertarget' in chunk and 'MathJax' in chunk:
                    start = j
                    break
        j -= 1
    out.append(content[i:start])
    out.append(r'\[\begin{aligned}')
    i = idx + len(MARKER)
content = "".join(out)

# Paso 2 desactivado: a veces rompe \href o \hypertarget anidados
# START = '{{}\\protect\\hypertarget{MathJax-Element-'
# ... (ver comentario en script)

with open("def.tex", "w", encoding="utf-8") as f:
    f.write(content)

print("Limpieza aplicada.")
