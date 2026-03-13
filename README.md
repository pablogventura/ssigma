# S-Sigma — Implementación del lenguaje S^Σ

Implementación en Python del lenguaje **S^Σ** (paradigma imperativo de Neumann). La definición formal está en el directorio **`definicion/`** del repositorio:

- **definicion/def.html** — Documento principal (sección 4.3)
- **definicion/RESUMEN_LENGUAJE_S_SIGMA.md** — Resumen de sintaxis y semántica

## Estructura

```
ssigma/             # Paquete principal
  __init__.py       # API pública
  instrucciones.py  # AST: todas las instrucciones (Ins^Σ)
  parser.py         # Parser de líneas → Programa
  programa.py       # Programa (lista de instrucciones, encontrar_label)
  maquina.py        # Ejecución (configuración, paso S_P, orquilla Ψ_P)
  infinitupla.py    # Estado s⃗ (numéricas) y σ⃗ (palabras)
examples/
  devuelveunoconh.code
definicion/         # Definición formal del lenguaje
test.py             # Script de prueba
```

## Instrucciones implementadas

Notación formal (definición) vs ASCII (esta implementación):

| Definición     | Sintaxis en código   | Descripción              |
|----------------|----------------------|--------------------------|
| Nk̄←Nk̄+1       | `Nk <- Nk + 1`       | Sucesor                  |
| Nk̄←Nk̄˙−1      | `Nk <- Nk -·- 1`     | Predecesor (RestaPunto)  |
| Nk̄←0          | `Nk <- 0`            | Cero                     |
| Nk̄←Nn̄         | `Nk <- Nn`           | Copia numérica           |
| IF Nk̄≠0 GOTO Lm̄ | `IF Nk != 0 GOTO Lm` | Condicional numérico     |
| GOTO Lm̄       | `GOTO Lm`            | Salto incondicional      |
| SKIP          | `SKIP`               | Nop                      |
| Pk̄←^↷Pk̄      | `Pk <- ^Pk`          | Quitar primer símbolo    |
| Pk̄←Pk̄.a       | `Pk <- Pk a`         | Concatenar símbolo       |
| Pk̄←ε          | `Pk <- epsilon`      | Vaciar palabra           |
| Pk̄←Pn̄         | `Pk <- Pn`           | Copia palabra            |
| IF Pk̄ BEGINS a GOTO Lm̄ | `IF Pk BEGINS a GOTO Lm` | Condicional palabra |

Las etiquetas son opcionales: **Lk** al inicio de la línea. Índices desde 1 (N1, P1, L1, …).

## Uso

Desde la raíz del repositorio:

```python
from ssigma import Parser, Ejecucion

p = Parser()
prog = p.programa_desde_archivo("examples/devuelveunoconh.code")
e = Ejecucion(prog)

# Orquilla numérica: función (n₁,…,nₙ, p₁,…,pₘ) → N1 al terminar (Ψ_P^{n,m,#})
f = e.orquilla_numerica(0, 1)  # 0 entradas numéricas, 1 alfabética (P1)
resultado = f("g")             # P1 = "g", devuelve N1 al terminar
```

Ejecutar el script de prueba:

```bash
python3 test.py
```

## Requisitos

- Python 3.

## Licencia

GPLv3 (según cabeceras en el código original de Pablo Ventura, 2013).
