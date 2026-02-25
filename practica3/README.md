# Práctica 3: Temple Simulado (Simulated Annealing)

Este directorio contiene dos implementaciones del algoritmo de Temple Simulado aplicadas a la optimización de la función **Peaks**.

## ¿Qué es el Temple Simulado?

El **Temple Simulado** (Simulated Annealing) es un algoritmo de búsqueda metaheurística para problemas de optimización global. Su nombre e inspiración provienen del proceso de recocido en la metalurgia, una técnica que implica calentar y luego enfriar lentamente un material para variar sus propiedades físicas.

El algoritmo explora el espacio de búsqueda permitiendo, de forma probabilística, movimientos a soluciones peores. Esta probabilidad de aceptar soluciones "malas" está controlada por un parámetro llamado **Temperatura**, que disminuye gradualmente a lo largo del proceso. Al principio (alta temperatura), el algoritmo es muy exploratorio; al final (baja temperatura), se vuelve más selectivo, comportándose casi como una búsqueda local pura.

---

## Comparativa de Versiones

Hemos implementado dos variantes del algoritmo para observar su comportamiento y eficacia.

### 1. Temple Estándar (`temple-estandar.py`)
Sigue el flujo clásico del algoritmo propuesto originalmente por Kirkpatrick et al.

*   **Búsqueda Local:** Siempre se mueve a partir de la posición actual hacia un vecino cercano.
*   **Enfriamiento Geométrico:** La temperatura disminuye de forma constante (`T = T * cooling_rate`).
*   **Riesgo:** Puede quedar atrapado en un **mínimo local** si la temperatura baja demasiado rápido antes de encontrar la región del óptimo global.
*   **Trayectoria:** Es continua y suave, representando un proceso de refinamiento constante.

### 2. Temple Clase (`temple-clase.py`)
Es una versión mejorada (híbrida) diseñada para ser más robusta frente a óptimos locales.

*   **Detección de Estancamiento:** Cuenta cuántas iteraciones pasan sin que la mejor solución global mejore (`max_no_improve`).
*   **Saltos Aleatorios (Random Restarts):** Si se detecta estancamiento, el algoritmo realiza un "salto" a una posición completamente aleatoria del mapa.
*   **Recalentamiento (Reheating):** Tras un salto, la temperatura se incrementa ligeramente (`T = T * 1.05`) para fomentar la exploración de la nueva zona.
*   **Ventaja:** Tiene una probabilidad mucho mayor de escapar de pozos locales y explorar diversas áreas de la función Peaks.
*   **Trayectoria:** Muestra discontinuidades (saltos) representadas con cuadrados cian en la visualización.

---

## Resultados Esperados

Al ejecutar ambos scripts, se observará que:
- La **versión estándar** a veces converge rápidamente a una solución, pero no siempre es la mejor posible si empezó lejos del óptimo global.
- La **versión de clase** es más resiliente; aunque "pierda" tiempo saltando, suele encontrar valores de energía más bajos al explorar más eficientemente la compleja superficie de la función Peaks.
