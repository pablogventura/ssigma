# Ejemplos de programas S^Σ

Programas en sintaxis concreta. Para cargar y ejecutar (desde la raíz del repo):

```python
from ssigma import Parser, Ejecucion
p = Parser()
prog = p.programa_desde_archivo("examples/solo_numericos.code")  # o prog_con_include.code si usas INCLUDE
e = Ejecucion(prog)
e.debug = False
e.ejecutar()
print(e.numericas[1])  # resultado en N1
```

Si el programa usa macros predefinidos (SUMA, RESTA, …) sin INCLUDE: `Parser(registro_macros=registro_por_defecto())`.

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
| `print_ejemplo.code` | PRINT N1, PRINT N2 (extensión). | Imprime 2 y 3 |
| `input_ejemplo.code` | INPUT N1, INPUT N2, N1+1, PRINT N1, PRINT N2. Para probar sin teclado: `e.entrada = iter(["5", "100"])`. | N1=6, N2=100, imprime 6 y 100 |
| `fibonacci.code` | Calcula F_n (F_0=0, F_1=1). Entrada N1=n, salida N3=F_n y PRINT N3. Requiere SUMA y RESTA (`registro_por_defecto()` o INCLUDE std.macros). | N1=10 → N3=55, F_0=0 |
| `primo.code` | Decide si N1=n es primo (N2=1) o no (N2=0). Usa RESTA para resto y comparación. INCLUDE std.macros o registro. | N1=7 → N2=1; N1=10 → N2=0 |

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
