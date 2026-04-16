---
name: academic-doc-ieee
description: >
  Estructura y convenciones para redactar documentos académicos estilo IEEE
  para la materia de algoritmos de optimización (CUCEI, Ingeniería en Computación).
  Trigger: Cuando el usuario pide crear, redactar o completar un documento académico
  sobre un algoritmo de optimización (gradiente descendente, temple simulado, etc.).
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

## Cuándo usar esta skill

- El usuario pide crear un documento académico sobre un algoritmo de optimización
- El usuario pide completar o corregir un `.docx` de práctica universitaria
- El usuario menciona CUCEI, CUCEA, o Licenciatura en Ingeniería en Computación
- El documento describe implementación + análisis de un algoritmo metaheurístico o de primer orden

---

## Estructura del documento (IEEE-style académico)

El documento sigue formato de paper IEEE de dos columnas. Todas las secciones usan estilo
`Normal` en Word — **no se usan estilos de encabezado (Heading 1/2/3)**. Las listas usan
estilo `List Paragraph`.

### Bloque de cabecera (sin sección numerada)

```
TÍTULO DEL ALGORITMO                    ← TODO EN MAYÚSCULAS
Nombre Completo del Autor
Centro Universitario de Ciencias Exactas e Ingenierías
Licenciatura en Ingeniería en Computación
Guadalajara, Mexico
correo@alumnos.udg.mx
```

### RESUMEN (sin número de sección)

Etiqueta: `RESUMEN` (mayúsculas, sin número)

Contiene **3 párrafos** en este orden:
1. **Contexto + objetivo**: qué problema resuelve el algoritmo y qué se estudia
2. **Metodología/variante**: cómo se implementó, qué variante se diseñó (si aplica)
3. **Resultados clave**: métricas concretas (tiempo, precisión, convergencia, desviación estándar)

> Tip: El resumen NO menciona "este documento", usa voz pasiva técnica.
> Incluye valores numéricos concretos (ej. "desviación estándar de 0.000", "40 iteraciones").

---

### I. INTRODUCCIÓN

**Párrafo de contexto** (~2 párrafos):
- Define el dominio del problema (optimización, NP-hard, etc.)
- Explica por qué los métodos exactos son insuficientes
- Introduce el algoritmo a estudiar

**Subsección: Justificación**
- Por qué este algoritmo es relevante
- Ventajas y limitaciones conocidas
- Qué justifica su estudio

**Subsección: Objetivos**
Lista con `List Paragraph`, exactamente **3 ítems**:
- Objetivo 1: Implementar el algoritmo (con detalles de lenguaje/entorno)
- Objetivo 2: Analizar un parámetro crítico (ej. tasa de aprendizaje, temperatura)
- Objetivo 3: Validar/comparar el comportamiento en un caso de prueba específico

---

### II. MARCO TEÓRICO

**Párrafo introductorio** del fundamento matemático del algoritmo.

**Subsecciones temáticas** (sin número, solo texto en negrita o normal):
- Fundamento principal del algoritmo (fórmulas, vector gradiente, criterio de Metrópolis, etc.)
- Análisis de la topología del problema (convexidad, multimodalidad, etc.)
- Si hay variante híbrida: subsección **"Variante Híbrida"** explicando la extensión

**Convención de fórmulas**:
- Las ecuaciones se escriben inline como texto o en párrafo separado
- Variables matemáticas: usar notación estándar (α para learning rate, T para temperatura, etc.)
- No se usan bloques de código para fórmulas — son texto matemático puro

---

### III. METODOLOGÍA

**Subsección: Especificación/Descripción del Algoritmo**
- Flujo lógico del algoritmo (no pseudocódigo aún)
- Para variantes: describir **ambas versiones** (estándar e híbrida) por separado
- Comparar diferencias clave entre versiones

**Subsección: Configuración de Hiperparámetros / Parámetros de Control**
Lista con `List Paragraph` de los parámetros usados:
- Nombre del parámetro: valor usado + justificación técnica de por qué ese valor

**Subsección: Funciones de Prueba**
- Define la función objetivo usada (fórmula + propiedades)
- Calcula analíticamente el gradiente/derivada
- Especifica el óptimo teórico conocido

**Subsección: Pseudocódigo**
- Descripción narrativa de las 3 fases del algoritmo:
  1. Inicialización
  2. Ciclo iterativo
  3. Actualización y criterio de parada

**Subsección: Entorno de Desarrollo**
Lista con `List Paragraph`:
- Lenguaje de programación + justificación
- Bibliotecas técnicas usadas (NumPy, Matplotlib, etc.)
- Sistema operativo

---

### IV. RESULTADOS

**Presentación objetiva de datos** — sin interpretar todavía.

**Subsección: Tablas Comparativas**
- Si hay una sola variante: tabla de iteración vs valor de función
- Si hay dos variantes: tabla comparativa con columnas: Ejecución | SA Estándar | SA Híbrido | Tiempo

> Incluir nota aclaratoria debajo de la tabla si los valores requieren interpretación.

**Subsección: Gráficas de Convergencia**
- Describir lo que se observa en las gráficas generadas (los archivos `.png`)
- Para una variante: comportamiento asintótico, densidad de puntos cerca del mínimo
- Para dos variantes: contrastar curvas (monotónica vs picos de recalentamiento)

**Subsección: Comportamiento del parámetro crítico**
- Cómo el gradiente/temperatura evolucionó durante la ejecución
- Valores numéricos concretos en intervalos clave (iteraciones 1-10, 30-40, etc.)

---

### V. DISCUSIÓN

**Párrafo principal de análisis de desempeño**:
- Evaluar qué tan bien convergió el algoritmo
- Explicar causas del comportamiento observado (convexidad, parámetros, topología)
- Si hay comparación: declarar superioridad de una variante con evidencia

**Subsección: Comportamiento de los Parámetros**
- Análisis de sensibilidad al parámetro crítico
- Qué pasa con valores extremos (muy alto, muy bajo)

**Subsección: Limitaciones** (incluir siempre)
Lista con `List Paragraph` de al menos **2 limitaciones**:
- Factores externos que pudieron afectar los resultados
- Parámetros arbitrarios o sensibles que requieren más estudio

---

### VI. CONCLUSIONES

**Párrafo 1**: Confirmar la hipótesis principal con evidencia numérica.
**Párrafo 2**: Análisis del parámetro crítico — qué valor es óptimo y por qué.
**Párrafo 3**: Recomendación práctica — cuándo usar este algoritmo vs alternativas.

> Las conclusiones NO repiten la metodología. Van directo al impacto y la recomendación.

---

### REFERENCIAS

Formato numerado: `[N] Apellido, N. (año). Título. Fuente. URL`

- Mínimo **5 referencias**
- Mix de artículos académicos, blogs técnicos especializados, y libros/cursos
- Incluir DOI cuando sea un journal paper
- Estilo APA con URL al final

---

## Convenciones de formato Word

| Elemento | Estilo Word |
|---|---|
| Todo el texto | `Normal` |
| Ítems de lista | `List Paragraph` |
| Títulos de sección (I. INTRODUCCIÓN) | `Normal` (texto en mayúsculas + negrita implícita) |
| Subtítulos de subsección | `Normal` (texto en negrita o solo mayúscula inicial) |
| Fórmulas matemáticas | `Normal` (texto inline o párrafo separado) |

> **IMPORTANTE**: No usar estilos `Heading 1/2/3`. Todos los párrafos son `Normal`.
> El formato visual IEEE (dos columnas, márgenes ajustados) se logra con configuración
> de página, no con estilos de párrafo.

---

## Checklist de calidad antes de entregar

- [ ] El resumen incluye valores numéricos concretos
- [ ] Los objetivos son exactamente 3 ítems en lista
- [ ] El marco teórico incluye las fórmulas matemáticas centrales del algoritmo
- [ ] La metodología especifica los hiperparámetros con justificación técnica
- [ ] Los resultados referencian los archivos de gráficas generados (`.png`)
- [ ] La discusión tiene subsección de Limitaciones
- [ ] Las conclusiones incluyen recomendación de cuándo NO usar el algoritmo
- [ ] Las referencias son al menos 5 y tienen URLs válidas
- [ ] Ningún estilo es `Heading` — todo es `Normal` o `List Paragraph`

---

## Ejemplo de apertura del RESUMEN

```
El presente documento/estudio expone/aborda [la implementación y análisis / la comparación]
del algoritmo de [NOMBRE], [descripción de una línea del algoritmo]. El estudio se centra
en evaluar [métrica principal] sobre [contexto del problema].

[Metodología: cómo se implementó, qué herramientas, qué variante].

Los resultados demuestran [resultado principal con número concreto]. Se concluye que
[recomendación práctica con evidencia].
```
