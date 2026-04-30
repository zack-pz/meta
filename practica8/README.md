OPTIMIZACIÓN DE CLAHE MEDIANTE CUCKOO SEARCH CON VUELOS DE LÉVY PARA MEJORA DE CONTRASTE EN IMÁGENES

Nombre Completo del Autor
Centro Universitario de Ciencias Exactas e Ingenierías
Licenciatura en Ingeniería en Computación
Guadalajara, Mexico
correo@alumnos.udg.mx

**RESUMEN**

Se abordó la mejora de contraste local en imágenes digitales mediante la optimización automática de los parámetros de Contrast Limited Adaptive Histogram Equalization (CLAHE) con el algoritmo Cuckoo Search apoyado por vuelos de Lévy. El problema es relevante porque la ecualización global suele perder detalle regional cuando la iluminación no es uniforme o cuando el contraste útil está distribuido de manera no homogénea. El caso de prueba empleado fue la imagen `gato.png` con resolución de 186 × 193 píxeles.

La implementación se desarrolló en Python y modeló cada nido como un vector continuo de dos dimensiones: `clip_limit` y `tile_size`. La calidad de cada solución se evaluó con la suma normalizada de la desviación estándar y la entropía de la imagen resultante. Los artefactos experimentales disponibles muestran una corrida de 60 iteraciones y una convergencia prácticamente inmediata después de la primera mejora significativa.

Los resultados finales muestran un incremento de la desviación estándar de 37.269 a 56.781, un aumento de la entropía de 7.097 a 7.545 y una mejora de la función de calidad de 1.469 a 1.830 sobre la imagen exportada. Además, la curva `gato-convergencia-cuckoo.png` registra un salto aproximado de 1.800 a 1.858 entre la iteración inicial y la primera iteración efectiva, seguido de una meseta estable hasta la iteración 60. La evidencia indica que la estrategia híbrida logró expandir el rango dinámico tonal sin destruir la estructura visual principal del objeto.

**I. INTRODUCCIÓN**

La optimización aplicada al procesamiento digital de imágenes busca ajustar parámetros de transformación para maximizar criterios de calidad visual o estadística. En escenarios reales, la relación entre parámetros de mejora y percepción final no suele ser lineal ni convexa, por lo que el ajuste manual resulta ineficiente y altamente dependiente de la experiencia del operador. Este comportamiento se vuelve más evidente en métodos locales como CLAHE, donde pequeñas variaciones en los parámetros modifican tanto la textura fina como la amplificación del ruido.

Los métodos exactos o basados en derivadas no siempre son adecuados para este tipo de problema. La razón es que la función objetivo depende de histogramas discretos, clipping, redondeo del tamaño de bloque e interpolación bilineal, lo que introduce discontinuidades y regiones multimodales. En este contexto, Cuckoo Search constituye una alternativa apropiada porque combina exploración global mediante vuelos de Lévy con reemplazo competitivo de soluciones, permitiendo ubicar configuraciones de realce adecuadas sin requerir gradientes analíticos.

**Justificación**

El estudio de Cuckoo Search es pertinente porque permite resolver problemas de optimización no convexos con una parametrización relativamente compacta. Su aplicación sobre CLAHE resulta académicamente valiosa debido a que integra una metaheurística de búsqueda global con un operador clásico de realce local. Entre sus ventajas destacan la simplicidad estructural, la capacidad de escapar de zonas pobres del espacio de búsqueda y la facilidad para adaptarse a funciones objetivo definidas por métricas de imagen. Como limitación, su desempeño depende de la calibración de los parámetros de exploración y de la calidad del criterio de evaluación elegido.

**Objetivos**

- Implementar en Python una versión didáctica de Cuckoo Search con vuelos de Lévy para ajustar automáticamente los parámetros `clip_limit` y `tile_size` de CLAHE.
- Analizar el efecto del criterio de calidad y del comportamiento convergente del algoritmo durante una corrida de 60 iteraciones sobre una imagen de prueba en escala de grises.
- Validar la mejora obtenida mediante comparación visual y estadística entre la imagen original `gato.png` y la imagen resultante `gato-clahe-cuckoo.png`.

**II. MARCO TEÓRICO**

El fundamento matemático del método parte de dos componentes: una metaheurística de búsqueda global y un operador local de realce de contraste. Cuckoo Search modela cada solución como un nido y utiliza vuelos de Lévy para generar desplazamientos largos y cortos en el espacio de búsqueda. CLAHE, por su parte, divide la imagen en bloques, limita el crecimiento del histograma local y combina los mapas de intensidad mediante interpolación bilineal.

**Fundamento del algoritmo**

Sea una solución `x = [c, t]`, donde `c` representa `clip_limit` y `t` representa `tile_size`. La nueva candidata se genera con la relación `x_i^(k+1) = x_i^k + α · L(β) · (x_i^k - x_mejor^k) · s`, donde `α` es la escala del vuelo, `L(β)` es el paso de Lévy con parámetro `β = 1.5` y `s` es el tamaño del rango de búsqueda por dimensión. El paso de Lévy se construye con el esquema de Mantegna, cuya desviación se expresa como `σ_u = [Γ(1 + β) · sin(πβ/2) / (Γ((1 + β)/2) · β · 2^((β - 1)/2))]^(1/β)`.

La función objetivo usada en la práctica fue `J(I') = σ(I')/64 + H(I')/8`, donde `σ(I')` es la desviación estándar de la imagen mejorada y `H(I') = -Σ p_i log2(p_i)` es su entropía de Shannon. El primer término favorece dispersión tonal y el segundo premia riqueza informacional. El problema se plantea como una maximización de `J`.

**Topología del problema**

El espacio de búsqueda es mixto y no convexo. `clip_limit` es continuo en el intervalo `[0.5, 4.0]`, mientras que `tile_size` se redondea a un entero en `[8, 64]`. Esa mezcla continuo-discreta vuelve no derivable la función objetivo respecto a todos sus parámetros. Además, el recorte del histograma y la interpolación entre tiles producen zonas planas y cambios abruptos, por lo que pueden existir múltiples óptimos locales.

**Variante Híbrida**

La práctica no aplica Cuckoo Search sobre una función analítica convencional, sino sobre un pipeline híbrido de procesamiento de imagen. La metaheurística propone parámetros y CLAHE actúa como transformador del dominio. La aptitud no proviene directamente de la solución, sino de la calidad estadística de la imagen generada. Esta hibridación es importante porque desplaza el problema desde la optimización abstracta hacia la optimización de un proceso perceptual y estadístico.

**III. METODOLOGÍA**

**Especificación del algoritmo**

La versión base de Cuckoo Search considera un conjunto de nidos, la generación de candidatas mediante vuelos de Lévy, la comparación contra soluciones existentes y el abandono de una fracción `p_a` de los peores nidos. En la práctica, esa estructura se mantuvo, pero la evaluación de cada solución se reemplazó por la ejecución de CLAHE sobre la imagen de entrada y el cálculo de la función `J(I')`.

La versión híbrida usada en esta práctica difiere del esquema estándar en que cada nido codifica parámetros de un operador de visión por computadora en lugar de representar directamente un punto sobre una función matemática clásica. La diferencia clave entre ambas versiones es que aquí la evaluación es considerablemente más costosa y depende de propiedades emergentes de la imagen procesada, no de una expresión cerrada simple.

**Configuración de hiperparámetros / parámetros de control**

- `n_nidos = 12`: se eligió una población pequeña para mantener bajo el costo computacional sin anular diversidad inicial.
- `n_iteraciones = 60`: la gráfica de convergencia disponible registra 61 puntos, equivalentes a la iteración inicial más 60 iteraciones de búsqueda.
- `p_a = 0.25`: se abandonó el 25 % de los peores nidos para reinyectar exploración sin destruir la memoria colectiva.
- `α = 0.25`: se empleó una escala moderada del vuelo de Lévy para evitar saltos excesivos en un espacio de sólo dos dimensiones.
- `β = 1.5`: valor común en vuelos de Lévy porque balancea exploración de largo alcance con refinamiento local.
- `semilla = 42`: se usó para reproducibilidad experimental.
- `clip_limit ∈ [0.5, 4.0]`: rango suficiente para evitar tanto subrealce como sobresaturación severa.
- `tile_size ∈ [8, 64]`: intervalo adecuado para cubrir desde contraste muy local hasta comportamiento cercano a una ecualización menos localizada.

**Funciones de prueba**

La imagen de trabajo fue `gato.png`, con tamaño de 186 × 193 píxeles y almacenamiento PNG en RGBA. Previo a la optimización, la imagen se convirtió a escala de grises con la relación `Y = 0.299R + 0.587G + 0.114B`, manteniendo intensidades en `[0, 255]`.

La función objetivo fue `J(I') = σ(I')/64 + H(I')/8`. No se calculó un gradiente analítico porque `tile_size` es discreto, el clipping del histograma introduce discontinuidades y la entropía depende de frecuencias cuantizadas. Por lo tanto, no existe en este caso un óptimo teórico cerrado ni una derivada práctica que justifique un método de descenso convencional. La solución óptima se determinó empíricamente como la mejor combinación encontrada durante la búsqueda.

**Pseudocódigo**

1. Inicialización: se generan aleatoriamente los nidos dentro de los límites de `clip_limit` y `tile_size`; cada nido se evalúa aplicando CLAHE y midiendo la calidad resultante.
2. Ciclo iterativo: para cada nido se produce una candidata mediante un vuelo de Lévy, se recorta al rango permitido y se compara contra un nido elegido aleatoriamente; si la candidata es mejor, reemplaza a la solución inferior.
3. Actualización y criterio de parada: en cada iteración se abandonan los peores nidos según `p_a`, se actualiza el mejor global y se almacena el historial de convergencia hasta completar el número total de iteraciones.

**Entorno de desarrollo**

- Lenguaje de programación: Python 3, por su claridad sintáctica y por facilitar la implementación didáctica de metaheurísticas y procesamiento de imagen.
- Bibliotecas usadas: NumPy para operaciones numéricas y manejo matricial; Matplotlib para lectura, guardado y visualización de resultados.
- Sistema operativo: Linux.

**IV. RESULTADOS**

Los resultados se presentan a partir de los artefactos generados en la carpeta `practica8/`: `gato-clahe-cuckoo.png`, `gato-convergencia-cuckoo.png` y `gato-comparacion-cuckoo.png`. La evidencia se divide en evolución de la aptitud y comparación estadística entre la imagen de entrada y la imagen optimizada.

**Tablas comparativas**

Tabla 1. Evolución del mejor valor de calidad durante la búsqueda.

| Iteración | Mejor calidad |
|---|---:|
| 0 | 1.800 |
| 1 | 1.858 |
| 10 | 1.858 |
| 30 | 1.858 |
| 60 | 1.858 |

Nota: los valores de la Tabla 1 se estiman visualmente a partir de la gráfica `gato-convergencia-cuckoo.png`, en la cual no se observan mejoras adicionales después de la primera iteración efectiva.

Tabla 2. Comparación de métricas entre la imagen original y la imagen mejorada exportada.

| Métrica | Original | Mejorada | Cambio relativo |
|---|---:|---:|---:|
| Media de intensidad | 99.431 | 115.573 | +16.23 % |
| Desviación estándar | 37.269 | 56.781 | +52.36 % |
| Entropía | 7.097 | 7.545 | +6.31 % |
| Calidad `J(I')` | 1.469 | 1.830 | +24.56 % |
| Rango dinámico | 185 | 252 | +36.22 % |

Nota: los valores de la Tabla 2 fueron calculados directamente sobre `gato.png` y `gato-clahe-cuckoo.png` a partir de sus intensidades en escala de grises.

**Gráficas de convergencia**

La gráfica `gato-convergencia-cuckoo.png` muestra una mejora abrupta al inicio de la búsqueda y una meseta estable hasta la iteración 60. No se aprecian oscilaciones grandes ni ciclos de degradación, lo que sugiere un problema de baja dimensionalidad donde el mejor nido se descubre rápidamente. La gráfica `gato-comparacion-cuckoo.png` exhibe un incremento visible del contraste en ojos, bigotes, contorno facial y textura del fondo. La imagen `gato-clahe-cuckoo.png` confirma una expansión tonal más amplia, con intensidades mínimas de 1 y máximas de 253.

**Comportamiento del parámetro crítico**

El parámetro crítico del proceso fue la combinación `clip_limit`–`tile_size`, porque controla simultáneamente el grado de recorte del histograma y la escala espacial del realce local. Aunque la corrida almacenada no conserva la traza explícita de ambos parámetros por iteración, su efecto puede inferirse a través de la aptitud y del rango dinámico resultante. Entre las iteraciones 0 y 1 la calidad aumentó aproximadamente de 1.800 a 1.858; entre las iteraciones 1 y 10 se mantuvo prácticamente constante; y entre las iteraciones 30 y 60 continuó estable sin mejoras visibles. Esto indica que la combinación encontrada fue suficiente para saturar tempranamente la capacidad de mejora sobre la imagen de prueba.

**V. DISCUSIÓN**

El algoritmo convergió de forma rápida y consistente. La mejora en la desviación estándar y en la entropía respalda que el contraste local se incrementó sin colapsar la distribución tonal en unas pocas intensidades. La rapidez de convergencia puede explicarse por la baja dimensionalidad del espacio de búsqueda y por el hecho de que la función objetivo combina dos criterios alineados con el realce visual: dispersión e información. En otras palabras, el problema no exigió una exploración extensa para alcanzar una región de alta calidad.

El comportamiento observado también es coherente con la naturaleza no convexa del problema. Aunque la función es irregular, el algoritmo no quedó atrapado en una zona claramente subóptima dentro de la corrida registrada. La superioridad de la solución final frente a la imagen original es evidente en términos estadísticos y visuales: la calidad aumentó 24.56 %, la dispersión tonal 52.36 % y el rango dinámico 36.22 %. Eso sí, la meseta temprana también sugiere que, para esta imagen en particular, el presupuesto de 60 iteraciones fue más que suficiente y probablemente redundante después de la primera mejora fuerte.

**Comportamiento de los parámetros**

Si `clip_limit` toma valores demasiado bajos, CLAHE se comporta de manera conservadora y el contraste local apenas cambia. Si toma valores demasiado altos, aumenta el riesgo de exagerar textura y ruido en regiones homogéneas. De forma análoga, un `tile_size` demasiado pequeño puede introducir realce agresivo y artefactos locales, mientras que uno demasiado grande se acerca a una ecualización menos localizada y pierde sensibilidad a estructuras finas. El experimento sugiere que una combinación intermedia o alta dentro del rango de búsqueda fue suficiente para producir una respuesta estable y visualmente útil.

**Limitaciones**

- El análisis se realizó sobre una sola imagen de prueba, por lo que no puede generalizarse automáticamente a texturas, iluminaciones o niveles de ruido distintos.
- La corrida almacenada no guarda explícitamente la historia completa de `clip_limit` y `tile_size`, por lo que el análisis de sensibilidad de ambos parámetros sólo puede inferirse de forma indirecta.
- No se reportó tiempo de ejecución ni se comparó contra una línea base adicional, como ecualización global o CLAHE con parámetros fijos definidos manualmente.

**VI. CONCLUSIONES**

La hipótesis principal queda respaldada: optimizar los parámetros de CLAHE con Cuckoo Search mejora de manera cuantificable el contraste de la imagen analizada. La evidencia numérica más relevante fue el aumento de la función de calidad de 1.469 a 1.830, junto con un incremento de la desviación estándar de 37.269 a 56.781 y de la entropía de 7.097 a 7.545.

Respecto al parámetro crítico, la evidencia experimental muestra que la combinación `clip_limit`–`tile_size` alcanzó una región estable de alto desempeño casi desde el inicio de la búsqueda. Esto sugiere que, para imágenes de complejidad moderada y una función objetivo bien elegida, no es necesario un número elevado de iteraciones para obtener una configuración efectiva. En términos prácticos, conviene mantener rangos acotados y evitar extremos que amplifiquen ruido o reduzcan demasiado el carácter local del realce.

Como recomendación práctica, esta estrategia debe utilizarse cuando se busca mejorar contraste local en imágenes con detalle fino y distribución tonal irregular, especialmente cuando no existe una parametrización manual confiable. No se recomienda como primera opción cuando el problema requiere interpretabilidad analítica, trazabilidad completa de parámetros o cuando una ecualización global simple ya produce resultados satisfactorios con menor costo computacional.

**REFERENCIAS**

[1] Yang, X. S., & Deb, S. (2009). Cuckoo Search via Lévy flights. 2009 World Congress on Nature & Biologically Inspired Computing (NaBIC). IEEE. https://doi.org/10.1109/NABIC.2009.5393690

[2] Mantegna, R. N. (1994). Fast, accurate algorithm for numerical simulation of Lévy stable stochastic processes. Physical Review E, 49(5), 4677-4683. https://doi.org/10.1103/PhysRevE.49.4677

[3] Pizer, S. M., Amburn, E. P., Austin, J. D., Cromartie, R., Geselowitz, A., Greer, T., ter Haar Romeny, B., Zimmerman, J. B., & Zuiderveld, K. (1987). Adaptive histogram equalization and its variations. Computer Vision, Graphics, and Image Processing, 39(3), 355-368. https://doi.org/10.1016/S0734-189X(87)80186-X

[4] Zuiderveld, K. (1994). Contrast Limited Adaptive Histogram Equalization. Graphics Gems IV, 474-485. https://doi.org/10.1016/B978-0-12-336156-1.50061-6

[5] OpenCV. (2026). cv::CLAHE Class Reference. OpenCV Documentation. https://docs.opencv.org/4.x/d6/db6/classcv_1_1CLAHE.html

[6] MathWorks. (2026). adapthisteq - Contrast-limited adaptive histogram equalization (CLAHE). MATLAB Documentation. https://www.mathworks.com/help/images/ref/adapthisteq.html
