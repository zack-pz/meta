ARTIFICIAL BEE COLONY PARA EL PROBLEMA DEL VIAJERO  
Nombre Completo del Autor  
Centro Universitario de Ciencias Exactas e Ingenierías  
Licenciatura en Ingeniería en Computación  
Guadalajara, Mexico  
correo@alumnos.udg.mx

RESUMEN

Se aborda el problema del viajero (Traveling Salesperson Problem, TSP), un problema clásico de optimización combinatoria NP-hard en el que se busca una ruta cerrada de costo mínimo que visite cada ciudad exactamente una vez. El estudio se centró en implementar una variante discreta del algoritmo Artificial Bee Colony (ABC) para una instancia euclidiana de 20 ciudades y en evaluar su capacidad de convergencia sobre una función objetivo definida por la longitud total de la ruta.

La metodología se desarrolló en Python mediante una representación por permutaciones, con una matriz de distancias euclidianas precomputada y tres fases operativas del ABC: abejas empleadas, observadoras y exploradoras. La adaptación combinatoria sustituyó la actualización continua estándar por operadores de vecindad tipo intercambio de dos ciudades e inversión de segmento. Se usaron 40 fuentes de alimento, 300 iteraciones y un límite base de abandono de 35 intentos; adicionalmente, se analizó la sensibilidad del parámetro `limite` con valores 10, 35 y 70.

Los resultados mostraron que, con semilla 42 y `limite = 35`, la mejor distancia descendió de 846.07 a 463.10 en 300 iteraciones, equivalente a una reducción de 45.26 %, con un tiempo de ejecución de 0.663 s. En cinco ejecuciones con semillas 40–44, la configuración base produjo una distancia promedio de 471.39 con desviación estándar de 8.09. El análisis paramétrico indicó que `limite = 70` mejoró el promedio a 454.45 con desviación estándar de 9.38 y tiempo medio de 0.673 s.

I. INTRODUCCIÓN

El problema del viajero constituye uno de los referentes más importantes de la optimización combinatoria, debido a que su tamaño de búsqueda crece factorialmente con el número de ciudades y a que modela situaciones reales de ruteo, logística, manufactura y planeación de recorridos. Cuando el número de nodos aumenta, los métodos exactos tienden a incrementar de manera importante su costo computacional, por lo que las metaheurísticas se vuelven alternativas atractivas para encontrar soluciones de buena calidad en tiempos razonables.

Dentro de esas metaheurísticas, Artificial Bee Colony destaca por su simplicidad conceptual y por el equilibrio que establece entre exploración y explotación. El algoritmo original fue propuesto para optimización continua; sin embargo, su estructura de búsqueda puede adaptarse a espacios discretos como el TSP si la solución se representa como una permutación de ciudades y si la generación de vecindarios respeta esa naturaleza combinatoria.

**Justificación.** ABC es relevante porque su diseño separa de forma explícita la explotación local, realizada por abejas empleadas y observadoras, de la exploración global, inducida por abejas exploradoras. Esa arquitectura permite estudiar de manera clara el efecto de parámetros de control como el límite de abandono. Su principal limitación en TSP es que la fórmula continua estándar no puede aplicarse de forma directa a permutaciones; por ello, su estudio es útil para comprender cómo se transforman metaheurísticas bioinspiradas continuas en procedimientos discretos viables.

**Objetivos.**

- Implementar en Python una versión simple de ABC para TSP usando rutas representadas como permutaciones, matriz de distancias euclidianas y visualización con Matplotlib.
- Analizar el efecto del parámetro crítico `limite` sobre la calidad de la solución y la estabilidad del algoritmo para la misma instancia de 20 ciudades.
- Validar el comportamiento del algoritmo mediante una ejecución base, una gráfica de convergencia y una gráfica del camino cerrado construido con nodos etiquetados.

II. MARCO TEÓRICO

Artificial Bee Colony modela el comportamiento de búsqueda de alimento de una colonia de abejas. Cada fuente de alimento representa una solución candidata y su calidad determina la probabilidad de ser explotada por las observadoras. En la formulación continua original, una nueva candidata se genera como `v_ij = x_ij + φ_ij (x_ij - x_kj)`, donde `φ_ij ∈ [-1, 1]` es un factor aleatorio y `k` es otra solución de referencia. En el caso del TSP esa actualización no es válida, porque una ruta debe seguir siendo una permutación sin repetir nodos.

**Fundamento principal del algoritmo.** Para una ruta `π = (π_1, π_2, ..., π_n)`, la función objetivo usada fue `L(π) = Σ_{k=1}^{n} d(π_k, π_{k+1})`, con `π_{n+1} = π_1`. La distancia entre dos ciudades `i` y `j` se calculó como `d(i, j) = sqrt((x_i - x_j)^2 + (y_i - y_j)^2)`. Como ABC selecciona con mayor probabilidad las soluciones de menor costo, se utilizó la aptitud `fit_i = 1 / (1 + L_i)`, donde `L_i` es la longitud de la ruta de la fuente `i`.

**Topología del problema.** En esta práctica el espacio de búsqueda es el conjunto de permutaciones `S_n`. Para `n = 20`, el número de recorridos posibles es `20! ≈ 2.43 × 10^18`, lo que evidencia la imposibilidad práctica de una enumeración exhaustiva. Además, la formulación es discreta, no convexa y carece de gradiente analítico útil en el sentido clásico; por ese motivo la mejora de soluciones se realiza mediante operadores de vecindad y no mediante derivadas.

**Adaptación combinatoria.** La variante implementada sustituyó la perturbación continua por dos operadores discretos: intercambio de dos ciudades (swap) e inversión de un segmento de la ruta. Ambos preservan la factibilidad de la permutación. Cuando una fuente acumula demasiados intentos sin mejora, se considera estancada y se reinicializa aleatoriamente; esa fase corresponde al comportamiento de las abejas exploradoras.

III. METODOLOGÍA

**Especificación del algoritmo.** La implementación parte de una instancia sintética de 20 ciudades con coordenadas en el intervalo `[0, 100] × [0, 100]`, generadas con semilla fija para garantizar reproducibilidad. A partir de esas coordenadas se construyó la matriz completa de distancias euclidianas. Cada fuente de alimento se inicializó como una permutación aleatoria de las 20 ciudades. En la fase de abejas empleadas, cada fuente genera un vecino con swap o inversión y lo acepta si reduce la longitud de la ruta. En la fase de observadoras, las fuentes se seleccionan por ruleta según `fit_i` y vuelven a ser perturbadas por el mismo esquema de vecindad. En la fase de exploradoras, las fuentes que alcanzan el umbral `limite` se reemplazan por nuevas permutaciones aleatorias. El algoritmo conserva la mejor ruta global hasta completar 300 iteraciones.

**Configuración de hiperparámetros / parámetros de control.**

- Número de ciudades: 20; permite observar comportamiento combinatorio sin volver ilegible la visualización de la ruta.
- Semilla de ciudades: 7; fija la misma instancia euclidiana en todas las ejecuciones para comparar resultados de manera justa.
- Número de fuentes de alimento (`n_fuentes`): 40; ofrece diversidad inicial suficiente sin aumentar demasiado el tiempo de cómputo.
- Número de iteraciones (`n_iteraciones`): 300; da margen para observar convergencia y posibles mesetas del algoritmo.
- Límite de abandono base (`limite`): 35; valor intermedio elegido para balancear reinicio de fuentes y explotación local.
- Vecindario: 50 % swap y 50 % inversión de segmento; combina cambios locales cortos con modificaciones estructurales más amplias.
- Semilla base del algoritmo: 42; utilizada para las gráficas y para la corrida principal reproducible.
- Semillas para análisis paramétrico: 40, 41, 42, 43 y 44; permiten estimar promedio, mejor caso y desviación estándar.

**Función de prueba.** La función objetivo corresponde a la suma de distancias de la ruta cerrada sobre la instancia de 20 ciudades. Dado que las ciudades se modelan como puntos `c_i = (x_i, y_i)` del plano, la distancia entre ciudades se obtiene por la métrica euclidiana. En esta formulación discreta no existe un gradiente analítico sobre el espacio de permutaciones, por lo que el concepto de derivada no se emplea en la actualización. Tampoco se dispone de un óptimo teórico cerrado para la instancia aleatoria generada; por ello la evaluación se basa en convergencia relativa, comparación entre ejecuciones y estabilidad estadística.

**Pseudocódigo.** La fase de inicialización crea 40 rutas aleatorias, evalúa sus distancias y registra la mejor solución inicial. En el ciclo iterativo, primero cada abeja empleada modifica su ruta actual y acepta la candidata si mejora el costo; después, las observadoras seleccionan fuentes promisorias mediante ruleta y vuelven a aplicar operadores de vecindad. En la fase de actualización, las fuentes que superan el umbral `limite` se reinician y el mejor costo global se almacena en el historial de convergencia. El criterio de parada es alcanzar las 300 iteraciones establecidas.

**Entorno de desarrollo.**

- Lenguaje de programación: Python 3; se eligió por su claridad sintáctica y por facilitar la implementación rápida de metaheurísticas reproducibles.
- Bibliotecas técnicas: NumPy para manejo vectorizado de coordenadas y matriz de distancias; Matplotlib para la gráfica del camino y la gráfica de convergencia.
- Sistema operativo: Linux.

IV. RESULTADOS

Los resultados que se presentan a continuación corresponden a mediciones directas obtenidas con el script `practica5/abc-viajero.py` y con ejecuciones adicionales para el análisis del parámetro `limite`. La corrida base usada para las gráficas empleó semilla 42.

**Tablas comparativas.**

Tabla 1. Historial de convergencia para la corrida base (`limite = 35`, semilla 42).

| Iteración | Mejor distancia acumulada |
|---|---:|
| 0 | 846.07 |
| 50 | 574.15 |
| 100 | 506.15 |
| 150 | 466.61 |
| 200 | 466.61 |
| 250 | 463.10 |
| 300 | 463.10 |

Nota: la iteración 0 representa la mejor ruta encontrada en la población inicial de 40 fuentes aleatorias.

Tabla 2. Resultados por ejecución con la configuración base (`limite = 35`).

| Ejecución (semilla) | Distancia final | Tiempo (s) |
|---|---:|---:|
| 40 | 470.62 | 0.693 |
| 41 | 467.26 | 0.675 |
| 42 | 463.10 | 0.663 |
| 43 | 486.76 | 0.650 |
| 44 | 469.23 | 0.660 |

Tabla 3. Sensibilidad del parámetro `limite` en cinco ejecuciones por configuración.

| `limite` | Distancia promedio | Desviación estándar | Mejor distancia | Peor distancia | Tiempo medio (s) |
|---|---:|---:|---:|---:|---:|
| 10 | 542.75 | 14.36 | 524.47 | 556.20 | 0.712 |
| 35 | 471.39 | 8.09 | 463.10 | 486.76 | 0.730 |
| 70 | 454.45 | 9.38 | 437.13 | 462.78 | 0.673 |

**Gráficas de convergencia.** La gráfica `practica5/abc-viajero-convergencia.png` muestra una curva descendente por escalones, con una caída pronunciada durante las primeras 100 iteraciones y estabilización a partir de la iteración 250 para la corrida base. La gráfica `practica5/abc-viajero-ruta.png` presenta las 20 ciudades etiquetadas y el ciclo cerrado encontrado: `19 → 11 → 18 → 10 → 16 → 5 → 15 → 14 → 7 → 6 → 12 → 3 → 2 → 13 → 9 → 0 → 8 → 4 → 1 → 17 → 19`.

**Comportamiento del parámetro crítico.** Con `limite = 10`, las distancias finales quedaron entre 524.47 y 556.20. Con `limite = 35`, las distancias se ubicaron entre 463.10 y 486.76. Con `limite = 70`, el intervalo descendió a 437.13–462.78. Los tiempos medios fueron 0.712 s, 0.730 s y 0.673 s, respectivamente. En la corrida base con `limite = 35`, la mejor distancia permaneció constante entre las iteraciones 150 y 200, y volvió a mejorar en la iteración 250.

V. DISCUSIÓN

El algoritmo convergió de manera consistente hacia rutas considerablemente más cortas que las de la población inicial. En la corrida base, la reducción de 846.07 a 463.10 indica una mejora relativa de 45.26 %, lo que confirma que la combinación de selección por aptitud y vecindarios discretos permite explotar rutas prometedoras sin perder la factibilidad de la permutación. La curva por escalones observada en la convergencia es coherente con una metaheurística de aceptación estricta: sólo se actualiza el historial global cuando aparece una solución mejor.

**Comportamiento de los parámetros.** El parámetro `limite` resultó decisivo. Un valor bajo (`limite = 10`) reinició fuentes con demasiada frecuencia y redujo el tiempo disponible para explotación local, por lo que el promedio empeoró a 542.75. El valor intermedio (`limite = 35`) ofreció un balance razonable y fue suficiente para obtener la ruta base de 463.10. Sin embargo, para esta instancia y presupuesto de 300 iteraciones, `limite = 70` fue superior: alcanzó el mejor promedio (454.45) y el mejor caso (437.13), lo que sugiere que una exploración menos agresiva favorece la profundización de rutas prometedoras antes de descartar una fuente.

**Limitaciones.**

- La instancia utilizada contiene sólo 20 ciudades generadas aleatoriamente; por lo tanto, los resultados no pueden generalizarse de forma directa a instancias grandes o a benchmarks clásicos como TSPLIB.
- No se realizó comparación contra un solucionador exacto ni contra otras metaheurísticas del repositorio, por lo que no puede afirmarse superioridad absoluta del método sobre alternativas como PSO, temple simulado u OR-Tools.
- El análisis paramétrico se concentró en `limite`; parámetros como `n_fuentes`, mezcla de operadores de vecindad y número de iteraciones todavía requieren estudio sistemático.

VI. CONCLUSIONES

La implementación discreta de Artificial Bee Colony resolvió de manera satisfactoria la instancia euclidiana de 20 ciudades, reduciendo la mejor distancia desde 846.07 hasta 463.10 en la corrida base y mostrando comportamiento estable en múltiples ejecuciones. La evidencia numérica respalda la hipótesis de que ABC puede adaptarse al TSP mediante representación por permutaciones y operadores de vecindad que preserven la factibilidad.

El análisis del parámetro crítico mostró que `limite = 70` fue la mejor configuración entre las evaluadas, con distancia promedio de 454.45 frente a 471.39 para `limite = 35` y 542.75 para `limite = 10`. En esta práctica, un umbral más alto permitió explotar mejor cada fuente antes de reiniciarla, lo que mejoró la calidad final sin penalización importante en tiempo.

Se recomienda usar ABC cuando se necesita una solución de buena calidad para TSP sin exigir optimalidad certificada y cuando se desea un algoritmo simple de implementar y fácil de visualizar. No se recomienda como primera opción cuando la instancia es pequeña y puede resolverse exactamente, ni cuando se requiere garantía formal de optimalidad o comparación rigurosa contra benchmarks estandarizados sin un ajuste paramétrico adicional.

REFERENCIAS

[1] Karaboga, D. (2005). *An idea based on honey bee swarm for numerical optimization*. Technical Report TR06, Erciyes University. https://abc.erciyes.edu.tr/pub/tr06_2005.pdf

[2] Karaboga, D., & Basturk, B. (2007). *A powerful and efficient algorithm for numerical function optimization: artificial bee colony (ABC) algorithm*. Journal of Global Optimization, 39(3), 459–471. https://doi.org/10.1007/s10898-007-9149-x

[3] Karaboga, D., & Basturk, B. (2008). *On the performance of artificial bee colony (ABC) algorithm*. Applied Soft Computing, 8(1), 687–697. https://doi.org/10.1016/j.asoc.2007.05.007

[4] Google for Developers. (2025). *Traveling Salesperson Problem | OR-Tools*. Google. https://developers.google.com/optimization/routing/tsp

[5] Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., Wieser, E., Taylor, J., Berg, S., Smith, N. J., Kern, R., Picus, M., Hoyer, S., van Kerkwijk, M. H., Brett, M., Haldane, A., del Río, J. F., Wiebe, M., Peterson, P., et al. (2020). *Array programming with NumPy*. Nature, 585(7825), 357–362. https://doi.org/10.1038/s41586-020-2649-2

[6] Hunter, J. D. (2007). *Matplotlib: A 2D graphics environment*. Computing in Science & Engineering, 9(3), 90–95. https://doi.org/10.1109/MCSE.2007.55
