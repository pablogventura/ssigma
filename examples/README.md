# Ejemplos de programas S^Σ

Programas en sintaxis concreta para cargar con `Parser().programa_desde_archivo(...)` o `Parser(registro_por_defecto()).programa_desde_archivo(...)` si usan macros.

| Archivo | Descripción | Resultado esperado (N1/P1) |
|---------|-------------|----------------------------|
| `devuelveunoconh.code` | IF P1 BEGINS H, N2+1, labels L3/L4, N1+1/-·1. Orquilla(0,1): entrada en P1, salida N1. | Con P1="g" → N1=0 |
| `solo_numericos.code` | N1←0, dos veces N1+1, SKIP. | N1=2 |
| `restapunto.code` | N1+1 tres veces, N1−·1 dos veces, SKIP. | N1=1 |
| `copia_y_salto.code` | N1←0, N2+1 dos veces, N1←N2, IF N1≠0 GOTO L1, N3+1, L1 SKIP. | N1=2, N2=2, N3=0 |
| `palabras.code` | P1←ε, P1←P1·a, P1←P1·b, P2←P1, IF P1 BEGINS a GOTO L1, N1+1, L1 SKIP. | P1=P2="AB", N1=0 |
| `suma_macro.code` | Una línea: SUMA(N1, N2, N3). Requiere parser con `registro_macros=registro_por_defecto()`. | Con N2=10, N3=7 → N1=17 |

Para ejecutar todos los tests (incluyen estos ejemplos):

```bash
python3 -m unittest discover -s tests -v
```
