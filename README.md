# S-Sigma — Implementación del lenguaje S^Σ

Implementación en Python del lenguaje **S^Σ** (paradigma imperativo de Neumann). Este lenguaje corresponde al definido en la materia **Lenguajes formales y Computabilidad** de la FaMAF (UNC), dictada por Diego Vaggione y Miguel Campercholi. El apunte está disponible en [www.granlogico.com](https://www.granlogico.com).

La definición formal usada en este proyecto está en **`definicion/`** (def.html, RESUMEN_LENGUAJE_S_SIGMA.md).

**Instalación:** `pip install ssigma` | [PyPI](https://pypi.org/project/ssigma/)

---

## Cómo programar en S^Σ

### Archivos de programa (`.code`)

- **Una instrucción por línea.** La línea puede empezar opcionalmente por una **etiqueta** `L1`, `L2`, … (sin espacio entre L y el número).
- **Línea en blanco** = fin del programa (el parser deja de leer).
- **Mayúsculas/minúsculas**: el parser normaliza a mayúsculas.
- **Variables**: `N1`, `N2`, … (números naturales, índice ≥ 1); `P1`, `P2`, … (palabras sobre el alfabeto).
- **Comentarios**: en archivos `.code` y `.macros`, las líneas que empiezan por `#` se ignoran.

Ejemplo mínimo:

```
N1 <- 0
N1 <- N1 + 1
N1 <- N1 + 1
SKIP
```

(Deja N1 = 2 y termina.)

### Usar macros en un programa

Puedes llamar a macros **predefinidos** (SUMA, RESTA, MULT, etc.) o a los que tú definas:

- **Opción A — Con macros predefinidos:** usa un parser que tenga el registro de macros y escribe en el `.code` una línea como `SUMA(N1, N2, N3)` (resultado en N1, argumentos N2 y N3).
- **Opción B — Incluir tus macros:** en el propio `.code` pon primero `INCLUDE ruta.macros` (ruta relativa al archivo). Después ya puedes usar `NOMBRE(N1, N2, …)` en ese archivo.

### Definir tus propios macros (archivos `.macros`)

En un archivo de texto (p. ej. `mis.macros`) defines macros con la **misma sintaxis** que el lenguaje, pero usando **variables de macro** (V1, V2, … para numéricas; A1, A2, … para etiquetas; W1, W2, … para palabras):

```
MACRO SUMA V1 V2 V3
V4 <- V2
V5 <- V3
V1 <- V4
A1: IF V5 != 0 GOTO A2
GOTO A3
A2: V5 <- V5 -·- 1
V1 <- V1 + 1
GOTO A1
A3: SKIP
ENDMACRO
```

- **MACRO** nombre y lista de parámetros (V1, V2, … en el orden que quieras).
- Cuerpo: instrucciones como siempre, con Vn, An (y opcionalmente N, L). Los nombres que aparezcan en el cuerpo y no estén en la lista de parámetros se tratan como **auxiliares** (se les asignan índices frescos al expandir).
- **ENDMACRO** cierra el bloque. Líneas que empiecen por `#` son comentarios.

Ver **`examples/mi_suma.macros`** y **`examples/prog_con_include.code`**.

---

## Estructura del proyecto

```
ssigma/                 # Paquete principal
  __init__.py           # API pública
  cli.py                # Comando ssigma (ejecutar .code desde la terminal)
  exceptions.py         # SSigmaError, ParseError, LabelNotFoundError, ExecutionError
  instrucciones/        # AST (Ins^Σ)
    base.py             # Clase Instruccion
    numericas.py        # Sucesor, RestaPunto, Cero, CopiaNumerica, IfNumerico, Goto, Skip
    palabras.py        # Agregar, Quitar, VaciarPalabra, CopiaPalabra, IfAlfabetico
  parser/               # Parser de líneas → Programa
    patrones.py         # Regex y fábricas por tipo (data-driven)
    parser.py           # Parser, INCLUDE
    macro_def_parser.py # Carga de archivos .macros (MACRO/ENDMACRO)
  macros.py             # Macro, RegistroMacros, expansión, predefinidos
  programa.py           # Programa, cargar/guardar (pickle)
  maquina.py            # Ejecución (estado, paso, orquilla Ψ_P)
  ejecutor.py           # Semántica: un paso por tipo de instrucción
  infinitupla.py        # Estado s⃗ (numéricas) y σ⃗ (palabras)
examples/               # Programas de ejemplo (.code y .macros)
  fibonacci.code        # n-ésimo Fibonacci
  primo.code            # Test de primalidad
  std.macros            # SUMA y RESTA para INCLUDE
  ...
definicion/             # Definición formal del lenguaje
scripts/
  publish_pypi.sh       # Publicar en PyPI (build + twine)
test.py                 # Script de prueba
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
| **PRINT Nk** (extensión) | `PRINT Nk` | Imprime el valor de Nk |
| **PRINT Pk** (extensión) | `PRINT Pk` | Imprime el valor de Pk |
| **INPUT Nk** (extensión) | `INPUT Nk` | Lee un entero y lo guarda en Nk |
| **INPUT Pk** (extensión) | `INPUT Pk` | Lee una línea y la guarda en Pk |

Las etiquetas son opcionales: **Lk** al inicio de la línea. Índices desde 1 (N1, P1, L1, …).

## Uso desde Python

Desde la raíz del repositorio:

**Programa sin macros:**

```python
from ssigma import Parser, Ejecucion

p = Parser()
prog = p.programa_desde_archivo("examples/solo_numericos.code")
e = Ejecucion(prog)
e.debug = False
e.ejecutar()
print(e.numericas[1])   # resultado en N1
```

**Programa que usa macros (incluidos por INCLUDE o predefinidos):**

```python
from ssigma import Parser, Ejecucion

# Si el .code tiene INCLUDE, no hace falta pasar registro; se crea uno y se cargan los .macros
p = Parser()
prog = p.programa_desde_archivo("examples/prog_con_include.code")
e = Ejecucion(prog)
e.debug = False
e.numericas[2] = 10
e.numericas[3] = 7
e.ejecutar()
print(e.numericas[1])   # 17
```

**Programa con macros predefinidos (SUMA, RESTA, …) sin INCLUDE:**

```python
from ssigma import Parser, Ejecucion, registro_por_defecto

p = Parser(registro_macros=registro_por_defecto())
prog = p.programa_desde_archivo("examples/suma_macro.code")
e = Ejecucion(prog)
e.debug = False
e.numericas[2], e.numericas[3] = 10, 7
e.ejecutar()
print(e.numericas[1])
```

**Orquilla numérica** (entrada/salida como función Ψ_P): estado inicial N1…Nn, P1…Pm; al terminar devuelve N1:

```python
prog = p.programa_desde_archivo("examples/devuelveunoconh.code")
e = Ejecucion(prog)
f = e.orquilla_numerica(0, 1)  # 0 numéricos, 1 palabra (P1)
resultado = f("g")              # P1 = "g" → devuelve N1 al terminar
```

**PRINT e INPUT:** Por defecto PRINT escribe en la salida estándar e INPUT lee con `input()`. Para tests o redirección: asigna `e.salida` (objeto con `.write()`) y/o `e.entrada` (iterador de líneas, p. ej. `iter(["5", "hola"])`).

**Errores:** La librería lanza excepciones claras con contexto:
- **ParseError**: sintaxis inválida o macro no registrada; incluye número de línea, archivo y fragmento de la línea.
- **LabelNotFoundError**: un GOTO/IF referencia un label que no existe; indica desde qué instrucción se referencia.
- **ExecutionError**: fallos en tiempo de ejecución (INPUT no numérico, no hay más entrada, instrucción no reconocida); incluye número de instrucción, paso y código.

**Tests y script de prueba:**

```bash
python3 -m unittest discover -s tests -v
python3 test.py
```

## Resumen rápido

| Qué quieres hacer | Dónde mirar |
|-------------------|-------------|
| Instalar y ejecutar desde terminal | `pip install ssigma` o `pipx install ssigma`; luego `ssigma archivo.code` |
| Sintaxis de cada instrucción | Tabla "Instrucciones implementadas" arriba; **definicion/RESUMEN_LENGUAJE_S_SIGMA.md** |
| Ejemplos de programas | **examples/** y **examples/README.md** (Fibonacci, primo, SUMA, INPUT, etc.) |
| Definir macros en archivos | Sección "Definir tus propios macros" arriba; **examples/mi_suma.macros** |
| Incluir macros desde un .code | Línea `INCLUDE ruta.macros`; **examples/prog_con_include.code**, **examples/std.macros** |
| Errores (sintaxis, ejecución) | Sección "Errores" en "Uso desde Python"; **ParseError**, **ExecutionError** |
| Definición formal del lenguaje | **definicion/def.html** (sección 4.3), **definicion/COBERTURA_IMPLEMENTACION.md** |

## Instalación

- **Desde PyPI** (una vez publicado):
  ```bash
  pip install ssigma
  pipx install ssigma   # comando ssigma en un entorno aislado
  ```

- **Desde el repo** (desarrollo o última versión):
  ```bash
  pip install .
  pipx install .        # desde el directorio del repo
  ```
  Luego puedes ejecutar un programa `.code` con:
  ```bash
  ssigma examples/solo_numericos.code
  ssigma examples/fibonacci.code   # N1=10 → imprime 55
  ssigma -v archivo.code            # modo verbose
  ssigma --help
  ```

- **Sin instalar** (solo tests): desde la raíz del repo, `python -m unittest discover -s tests -v`.

## Publicar en PyPI

1. Actualiza la versión en `pyproject.toml` (y en `ssigma/cli.py` en `--version` si quieres que coincida).
2. Crea un venv, activa y ejecuta:
   ```bash
   pip install -U build twine
   ./scripts/publish_pypi.sh         # sube a Test PyPI
   ./scripts/publish_pypi.sh --pypi   # sube a PyPI real
   ```
   Para PyPI real necesitas configurar token o usuario en `~/.pypirc` o variables de entorno.

## Requisitos

- Python 3.7+.

## Licencia

GPLv3 (según cabeceras en el código original de Pablo Ventura, 2013).
