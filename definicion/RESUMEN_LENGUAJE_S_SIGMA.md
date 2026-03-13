# Resumen: Lenguaje S^Σ (paradigma imperativo de Neumann)

Documento extraído de `definicion/def.html` y `definicion/def.tex`.  
Referencias: sección **4.3** del apunte, IDs en HTML: `#sintaxis-de-mathcalssigma`, `#semántica-de-mathcalssigma`, `#funciones-sigma-computables`, `#macros`, etc.

---

## 1. Estructura del directorio `definicion/`

| Archivo        | Descripción |
|----------------|-------------|
| `def.html`     | Documento principal (HTML generado, con MathJax). |
| `def.tex`      | Fuente LaTeX del documento. |
| `def.md`       | Versión intermedia (Pandoc). |
| `def.log`, `def.aux` | Auxiliares de compilación LaTeX. |
| `clean_tex.py` | Script de limpieza del .tex. |
| `def_files/`   | `MathJax.js`, `custom.js` (recursos del HTML). |

---

## 2. Sintaxis concreta (Sección 4.3.1, id: `SintaxisDeSsigma`)

### 2.1 Alfabetos

- **Σ**  
  Alfabeto de entrada/salida (símbolos de datos).  
  Ejemplo: Σ = {▴, #}.

- **Num** (numerales)  
  Símbolos: `0 1 2 3 4 5 6 7 8 9`.  
  Se usa **n̄** (overline) para la representación en base 10 del natural *n* (palabra en Num*).  
  Convenciones:
  - **Sig**: Num* → Num* (sucesor en base 10; Sig(ε)=1, Sig(α d)= siguiente dígito).
  - **Dec**: ω → Num* (Dec(0)=ε, Dec(n+1)=Sig(Dec(n))); Dec(n) = n̄.

- **Σ_p** (alfabeto del programa)  
  Σ_p = **Num** ∪ { **←**, **+**, **˙−** (dot-minus), **.** , **≠**, **^↷** (curved arrow), **ε**, **N**, **K**, **P**, **L**, **I**, **F**, **G**, **O**, **T**, **B**, **E**, **S** }.  
  La palabra de longitud 0 se denota con el símbolo **ε** ∈ Σ_p.  
  La sintaxis de S^Σ se construye solo con símbolos de **Σ ∪ Σ_p**.

### 2.2 Variables e instrucciones base

- **Variables numéricas**: N1, N2, … (N seguido de n̄). Valores en ω.
- **Variables de palabra**: P1, P2, … (P seguido de n̄). Valores en Σ*.

**Instrucciones base** (conjunto **Ins^Σ**): palabras sobre Σ ∪ Σ_p que denotan exactamente una instrucción. Tipos:

| Tipo (forma de Bas(I)) | Sintaxis | Descripción breve |
|------------------------|----------|-------------------|
| Asignación numérica −1 | Nk̄←Nk̄˙−1 | Nk := Nk −· 1 |
| Asignación numérica +1 | Nk̄←Nk̄+1 | Nk := Nk + 1 |
| Copia numérica | Nk̄←Nn̄ | Nk := Nn |
| Cero | Nk̄←0 | Nk := 0 |
| Condicional numérico | IF Nk̄≠0 GOTO Lm̄ | Si Nk≠0 ir a la instrucción con label Lm̄, si no a la siguiente |
| Quitar primer símbolo | Pk̄←^↷Pk̄ | Pk := quitar primer símbolo de Pk (^↷) |
| Concatenar símbolo | Pk̄←Pk̄.a | Pk := Pk · a (a ∈ Σ) |
| Copia palabra | Pk̄←Pn̄ | Pk := Pn |
| Vaciar palabra | Pk̄←ε | Pk := ε |
| Condicional palabra | IF Pk̄ BEGINS a GOTO Lm̄ | Si Pk comienza con *a*, ir a Lm̄; si no, siguiente |
| Salto incondicional | GOTO Lm̄ | Ir a la primera instrucción con label Lm̄ |
| Nop | SKIP | No hacer nada, pasar a la siguiente |

- **Etiquetas**: L1, L2, … (L seguido de n̄).  
- Una **instrucción (con posible etiqueta)** tiene la forma **Lk̄ J** con *k* ∈ **N** y *J* ∈ Ins^Σ, o bien *J* sin etiqueta.  
- **Bas(I)** (instrucción base): si *I* = Lk̄*J*, entonces Bas(I)=*J*; si no, Bas(I)=*I*.

### 2.3 Programas válidos (Def. “programa”, Pro^Σ)

- Un **programa** es una palabra **P** = I₁ I₂ … Iₙ con *n* ≥ 1, donde cada Iᵢ ∈ Ins^Σ.
- Cada programa tiene una **única** descomposición en secuencia de instrucciones I₁,…,Iₙ (unicidad por “tramo final” de palabras).
- Se definen *n*(P) (número de instrucciones) e Iᵢ^P (instrucción *i*), con Iᵢ^P = ε si *i*=0 o *i* > *n*(P).

---

## 3. Semántica (Sección 4.3.2)

### 3.1 Configuración / descripción instantánea

- **Estado**: par **(s⃗, σ⃗)** donde:
  - **s⃗** ∈ ω^ω: valores de N1, N2, …
  - **σ⃗** ∈ (Σ*)^ω: valores de P1, P2, …
- **Descripción instantánea**: triple **(i, s⃗, σ⃗)** donde *i* ∈ **N** es el **índice de la próxima instrucción** a ejecutar (posición en el programa).

### 3.2 Regla de transición (función S_P)

**S_P(i, s⃗, σ⃗)** = descripción instantánea que resulta de ejecutar la instrucción Iᵢ^P en el estado (s⃗, σ⃗).

- Si **i ∉ {1,…,n(P)}**: S_P(i, s⃗, σ⃗) = (i, s⃗, σ⃗) (sin cambio).
- Según **Bas(Iᵢ^P)** se aplica uno de los casos siguientes (resumen):
  - **Nk̄←Nk̄˙−1**: s'ₖ = sₖ −· 1; siguiente instrucción i+1.
  - **Nk̄←Nk̄+1**: s'ₖ = sₖ+1; i+1.
  - **Nk̄←Nn̄**: s'ₖ = sₙ; i+1.
  - **Nk̄←0**: s'ₖ = 0; i+1.
  - **IF Nk̄≠0 GOTO Lm̄**: si sₖ=0 → (i+1, s⃗, σ⃗); si sₖ≠0 → (min{l : I_l^P tiene label Lm̄}, s⃗, σ⃗).
  - **Pk̄←^↷Pk̄**: σ'ₖ = quitar primer símbolo de σₖ; i+1.
  - **Pk̄←Pk̄.a**: σ'ₖ = σₖ a; i+1.
  - **Pk̄←Pn̄**: σ'ₖ = σₙ; i+1.
  - **Pk̄←ε**: σ'ₖ = ε; i+1.
  - **IF Pk̄ BEGINS a GOTO Lm̄**: si σₖ comienza con *a* → ir a Lm̄; si no → (i+1, s⃗, σ⃗).
  - **GOTO Lm̄**: (min{l : I_l^P tiene label Lm̄}, s⃗, σ⃗).
  - **SKIP**: (i+1, s⃗, σ⃗).

### 3.3 Computación y terminación

- **Computación partiendo del estado (s⃗, σ⃗)**: sucesión de descripciones instantáneas  
  (1, s⃗, σ⃗), S_P(1, s⃗, σ⃗), S_P(S_P(1, s⃗, σ⃗)), …
- **Estado después de t pasos**: la segunda y tercera componente de S_P aplicado *t* veces a (1, s⃗, σ⃗).
- **Terminación**: el programa **termina** partiendo de (s⃗, σ⃗) si en la computación se llega a un punto donde la próxima instrucción sería I_{n(P)+1}^P = ε (no hay instrucción); en ese caso se considera que “queda intentando realizar ε” y la ejecución se detiene.
- **No terminación**: si la sucesión de índices nunca sale de {1,…,n(P)} de forma que se intente ejecutar la instrucción siguiente a la última (p. ej. bucle infinito).

---

## 4. Funciones Ψ y definiciones de computabilidad (Sección 4.3.3)

- **Estado inicial estándar** para *n* variables numéricas y *m* de palabra:  
  N1=x₁,…,Nn=xₙ, Nn+1=0,…; P1=α₁,…,Pm=αₘ, Pm+1=ε,…  
  Se denota estado ∥x₁,…,xₙ, α₁,…,αₘ∥.

- **Ψ_P^{n,m,#}(x⃗, α⃗)** (salida numérica): valor de **N1** en el estado final cuando P termina partiendo del estado ∥x₁,…,xₙ, α₁,…,αₘ∥; **indefinido** si P no termina.

- **Ψ_P^{n,m,*}(x⃗, α⃗)** (salida palabra): valor de **P1** en el estado final cuando P termina; indefinido si no termina.

- **Función Σ-computable** (def. en 4.3.3): *f*: D ⊆ ωⁿ×Σ*ᵐ → ω es **Σ-computable** si existe un programa P en S^Σ tal que, para (x⃗, α⃗) ∈ D, P termina con N1 = f(x⃗, α⃗), y para (x⃗, α⃗) ∉ D, P no termina. (Equivalente a Σ-efectivamente computable.)

- **Conjunto Σ-enumerable / Σ-computable**: definidos en el texto vía funciones características o dominio de funciones Σ-computables (sección 4.3.3 y subsiguientes).

---

## 5. Macros (Sección 4.3.4)

- **Macro**: plantilla de programa con **variables de macro** (numéricas, alfabéticas, labels) que se sustituyen al usarlo.
- **Expansión**: reemplazo de esas variables por variables/labels concretos del programa que usa el macro.
- Tipos útiles:
  - **Macros de asignación**: simulan Vn+1 ← f(V1,…,Vn̄,W1,…,Wm̄) para una función Σ-computable *f*.
  - **Macros de predicado**: simulan IF P(V1,…,Vn̄,W1,…,Wm̄) GOTO A1 para un predicado Σ-computable *P*.
- Los macros dependen del alfabeto Σ; la primera instrucción de un macro suele no ir etiquetada para poder etiquetarla al expandir.

---

## 6. Resumen en tres bloques

### Vocabulario

- **Σ**: alfabeto de datos.  
- **Σ_p**: Num ∪ {←, +, ˙−, ., ≠, ^↷, ε, N, K, P, L, I, F, G, O, T, B, E, S}.  
- **Num**: 0,…,9; n̄ = representación de *n* en base 10.  
- **Variables**: N1, N2, … (ω); P1, P2, … (Σ*).  
- **Labels**: L1, L2, …

### Reglas de formación de programas

- **Instrucciones** son palabras en (Σ∪Σ_p)* que tienen una de las formas sintácticas listadas (Nk̄←…, Pk̄←…, IF … GOTO …, GOTO Lm̄, SKIP), opcionalmente precedidas por Lk̄ (etiqueta).
- **Programa**: secuencia finita no vacía de instrucciones I₁…Iₙ; la descomposición es única.

### Reglas de ejecución (semántica operacional)

- **Configuración**: (i, s⃗, σ⃗) con *i* = índice de la próxima instrucción.
- **Paso**: (i, s⃗, σ⃗) → S_P(i, s⃗, σ⃗) según el tipo de Bas(Iᵢ^P) (asignaciones actualizan s⃗ o σ⃗; condicionales y GOTO cambian *i* al label indicado o a i+1; SKIP solo incrementa *i*).
- **Terminación**: cuando la próxima instrucción sería la “n+1” (inexistente), la máquina se detiene; el resultado se lee en N1 (salida numérica) o P1 (salida palabra).

---

*Referencias en el HTML: `#sintaxis-de-mathcalssigma`, `#semántica-de-mathcalssigma`, `#la-computación-partiendo-de-un-estado`, `#funciones-sigma-computables`, `#macros`.*
