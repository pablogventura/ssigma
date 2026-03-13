# Cobertura de la definición S^Σ por la implementación

Referencia: `definicion/RESUMEN_LENGUAJE_S_SIGMA.md` y `definicion/def.html` (sección 4.3).

## ✅ Totalmente implementado

### 2. Sintaxis (Ins^Σ)

| Definición | Implementación |
|------------|----------------|
| Nk̄←Nk̄˙−1 | `RestaPunto`, parser `Nk <- Nk -·- 1` |
| Nk̄←Nk̄+1 | `Sucesor`, parser `Nk <- Nk + 1` |
| Nk̄←Nn̄ | `CopiaNumerica`, parser `Nk <- Nn` |
| Nk̄←0 | `Cero`, parser `Nk <- 0` |
| IF Nk̄≠0 GOTO Lm̄ | `IfNumerico`, parser `IF Nk != 0 GOTO Lm` |
| Pk̄←^↷Pk̄ | `Quitar`, parser `Pk <- ^Pk` |
| Pk̄←Pk̄.a (a ∈ Σ) | `Agregar`, parser `Pk <- Pk a` |
| Pk̄←Pn̄ | `CopiaPalabra`, parser `Pk <- Pn` |
| Pk̄←ε | `VaciarPalabra`, parser `Pk <- EPSILON` |
| IF Pk̄ BEGINS a GOTO Lm̄ | `IfAlfabetico`, parser `IF Pk BEGINS a GOTO Lm` |
| GOTO Lm̄ | `Goto`, parser `GOTO Lm` |
| SKIP | `Skip`, parser `SKIP` |

- **Etiquetas**: Lk̄ opcional delante de cada instrucción; parser `L(label) resto`.
- **Programa**: secuencia I₁…Iₙ (n ≥ 1); clase `Programa`, validación de que todos los labels referenciados existan.

### 3. Semántica

- **Estado**: (s⃗, σ⃗) como `Infinitupla` numéricas y alfabéticas (índice desde 1).
- **Descripción instantánea**: (i, s⃗, σ⃗); en código `linea` es índice 0-based (equivalente a i−1).
- **S_P**: un paso por `ejecutar_paso` en `ejecutor.py`; máquina en `maquina.py` (`Ejecucion`).
- **Terminación**: cuando la próxima instrucción sería I_{n+1}^P = ε; en código `linea >= len(programa.ins)` → `termino = True`.

### 4. Funciones Ψ

- **Estado inicial estándar**: N1…Nn, P1…Pm fijados; resto en 0 / ε.
- **Ψ_P^{n,m,#}**: implementado como `orquilla_numerica(n_numericos, n_alfabeticos)` → función que devuelve **N1** al terminar.

### 5. Macros (4.3.4)

- Plantillas con variables de macro (Vn, Wn, An), expansión por sustitución, variables/labels auxiliares con índices frescos.
- Macros de asignación (SUMA, RESTA, MULT, PRED, DOBLE, MAX, MIN) y de predicado (IF_CERO, IF_IGUAL, IF_MENOR).
- Registro, expansión por nombre y argumentos.

---

## Diferencias o lagunas menores

1. **Ψ_P^{n,m,*} (salida palabra)**  
   La definición considera salida en **P1**. No hay una función `orquilla_palabra` que devuelva P1; el resultado se obtiene leyendo `e.alfabeticas[1]` tras `e.ejecutar()`.

2. **Alfabeto Σ**  
   En la definición Σ es un alfabeto fijo (ej. {▴,#}). En la implementación las palabras son cadenas de Python (cualquier carácter); no se valida pertenencia a un Σ dado.

3. **Formato de programa**  
   La definición exige unicidad de descomposición de la *palabra* P = I₁…Iₙ sobre Σ∪Σ_p. La implementación parsea **línea a línea** (una instrucción por línea), por lo que no se construye ni se comprueba esa palabra única; la semántica de programas es la misma.

4. **Numerales n̄**  
   En el apunte, los naturales se representan como palabras en base 10 (n̄). En la implementación las variables numéricas son enteros (ω) y la entrada/salida numérica usa enteros directamente; la semántica operacional coincide.

5. **Macros en código fuente**  
   En archivos `.code` solo se admiten llamadas a macros con argumentos **numéricos** (p. ej. `SUMA(N1,N2,N3)`). Los predicados con label (IF_CERO, IF_IGUAL, IF_MENOR) solo están soportados por **API** (`expandir_llamada(nombre, [var, label])`), no por sintaxis en el archivo.

### Extensión: definición de macros en el lenguaje

- **Archivos .macros**: se pueden definir macros en texto con la misma sintaxis S^Σ, usando variables de macro **Vn, Wn, An** (o N, P, L). Formato: `MACRO nombre param1 param2 ...` / cuerpo (instrucciones con V1, A1, etc.) / `ENDMACRO`.
- **INCLUDE**: en un `.code` se permite la línea `INCLUDE ruta.macros`; la ruta es relativa al archivo actual. Los macros cargados quedan disponibles para llamadas `NOMBRE(N1, N2, ...)`.
- Opcionalmente se puede pasar `macro_files=[...]` a `programa_desde_archivo()` para cargar archivos de macros antes de leer el programa.

Esto no modifica la definición del lenguaje (los macros siguen siendo plantillas que se expanden); solo se añade una forma de especificar esas plantillas en archivos de texto en lugar de en Python.

---

## Conclusión

El **núcleo del lenguaje** (sintaxis de instrucciones, programas, semántica S_P, terminación, Ψ numérico y macros de asignación/predicado) está **implementado** y alineado con la definición. Las diferencias son de presentación (Σ no fijo, programa por líneas, índices 0-based), de API (falta orquilla explícita para salida palabra) o de soporte de sintaxis (predicados solo por API). No falta ningún tipo de instrucción base ni regla de transición de la sección 4.3.
