# Ejemplos de programas S^Σ

Programas en sintaxis concreta para cargar con `Parser().programa_desde_archivo(...)` o `Parser(registro_por_defecto()).programa_desde_archivo(...)` si usan macros.

| Archivo | Descripción | Resultado esperado (N1/P1) |
|---------|-------------|----------------------------|
| `devuelveunoconh.code` | IF P1 BEGINS H, N2+1, labels L3/L4, N1+1/-·1. Orquilla(0,1): entrada en P1, salida N1. | Con P1="g" → N1=0 |
| `solo_numericos.code` | N1←0, dos veces N1+1, SKIP. | N1=2 |
| `restapunto.code` | N1+1 tres veces, N1−·1 dos veces, SKIP. | N1=1 |
| `copia_y_salto.code` | N1←0, N2+1 dos veces, N1←N2, IF N1≠0 GOTO L1, N3+1, L1 SKIP. | N1=2, N2=2, N3=0 |
| `palabras.code` | P1←ε, P1←P1·a, P1←P1·b, P2←P1, IF P1 BEGINS a GOTO L1, N1+1, L1 SKIP. | P1=P2="AB", N1=0 |
| `suma_macro.code` | SUMA(N1, N2, N3). Requiere parser con `registro_macros`. | N2=10, N3=7 → N1=17 |
| `resta_macro.code` | RESTA(N1, N2, N3) = N2 −· N3. Requiere registro_macros. | N2=10, N3=4 → N1=6 |
| `mult_macro.code` | MULT(N1, N2, N3) = N2*N3. Requiere registro_macros. | N2=3, N3=4 → N1=12 |

**Macros disponibles** (todos en `registro_por_defecto()`): SUMA, RESTA, MULT, PRED, DOBLE, MAX, MIN; predicados (solo API): IF_CERO, IF_IGUAL, IF_MENOR.

### Definir e incluir macros en el lenguaje

Puedes **definir macros en archivos** usando la sintaxis S^Σ con variables de macro (Vn, An, Wn):

- Archivo **.macros** (o cualquier nombre): bloques `MACRO nombre param1 param2 ...` / cuerpo (una instrucción por línea, con V1, A1, etc.) / `ENDMACRO`. Comentarios con `#`.
- En un **.code** puedes poner `INCLUDE ruta.macros` (ruta relativa al archivo actual); se cargan esos macros y luego puedes usar `NOMBRE(N1, N2, ...)`.
- Opcional: `Parser().programa_desde_archivo(main.code, macro_files=["carpeta/mis.macros"])` para cargar archivos de macros antes de leer el programa.

Ejemplos: `mi_suma.macros` (define SUMA), `prog_con_include.code` (INCLUDE + SUMA).

Para ejecutar todos los tests (incluyen estos ejemplos):

```bash
python3 -m unittest discover -s tests -v
```
