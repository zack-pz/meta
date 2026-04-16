OPTIMIZACIÓN POR ENJAMBRE DE PARTÍCULAS: IMPLEMENTACIÓN DE UN PSO SIMPLE

[Nombre Completo del Autor]

Centro Universitario de Ciencias Exactas e Ingenierías

Licenciatura en Ingeniería en Computación

Guadalajara, Mexico

[correo@alumnos.udg.mx]

**RESUMEN**

La optimización numérica de funciones multivariables aparece en problemas de ingeniería, aprendizaje automático y ajuste de parámetros, donde la búsqueda exhaustiva resulta costosa y los métodos analíticos no siempre son viables. En este contexto, la Optimización por Enjambre de Partículas (Particle Swarm Optimization, PSO) constituye una metaheurística poblacional inspirada en el comportamiento colectivo de aves y peces. El estudio se centró en implementar y analizar una versión canónica de PSO simple para minimizar una función convexa de referencia en dos dimensiones.

La variante desarrollada utilizó 30 partículas, 100 iteraciones, límites de búsqueda en $[-5,5]^2$, peso de inercia $w=0.7$, coeficientes cognitivo y social $c_1=c_2=1.5$, y semilla fija igual a 42 para garantizar reproducibilidad. La función de prueba fue $f(x,y)=x^2+y^2$, cuyo óptimo global teórico se localiza en $(0,0)$. La implementación se realizó en Python 3 con NumPy para cálculo vectorial y Matplotlib para registrar la convergencia global y la trayectoria de una partícula representativa.

Los resultados mostraron una reducción del mejor valor global desde $3.585544434140$ en la iteración 0 hasta $9.116301814501\times10^{-14}$ en la iteración 100, con una mejor posición estimada de $(-9.37562534\times10^{-8},\ 2.87006591\times10^{-7})$. En cinco ejecuciones con la misma semilla, el tiempo promedio fue de $42.206489$ ms, con desviación estándar de $6.030621$ ms, mientras que la desviación estándar del mejor valor fue $0.0$, lo que confirmó comportamiento determinista bajo configuración reproducible.

**I. INTRODUCCIÓN**

La optimización busca determinar los valores de decisión que minimizan o maximizan una función objetivo bajo ciertas condiciones. En problemas de baja dimensión y topología simple, los métodos exactos o basados en gradiente suelen ser suficientes; sin embargo, en escenarios no lineales, con ruido, discontinuidades o funciones multimodales, la construcción de soluciones exactas puede volverse computacionalmente costosa o incluso impracticable. Por esa razón, las metaheurísticas han adquirido relevancia como herramientas flexibles para aproximar soluciones de alta calidad en espacios de búsqueda complejos.

Dentro de este conjunto de métodos, PSO destaca por su simplicidad algorítmica, su bajo número de hiperparámetros y su independencia respecto del gradiente de la función objetivo. Cada partícula del enjambre representa una solución candidata que se desplaza en el espacio de búsqueda de acuerdo con su experiencia individual y con la mejor experiencia colectiva del grupo. En la presente práctica se estudió una versión simple o canónica del algoritmo, aplicada a una función de prueba controlada, con el fin de observar su convergencia y el papel de sus parámetros fundamentales.

**Justificación**

El estudio de PSO es relevante porque introduce una familia de métodos de optimización que no depende de derivadas y que puede adaptarse a funciones no diferenciables o altamente irregulares. Frente a otros enfoques poblacionales, su estructura resulta compacta y fácil de implementar, lo cual favorece su uso didáctico y experimental. No obstante, esta simplicidad también implica limitaciones: la convergencia depende de la calibración de parámetros, no existe garantía universal de encontrar el óptimo global y el costo en evaluaciones puede ser alto frente a métodos especializados para funciones convexas.

**Objetivos**

- Implementar un algoritmo PSO simple en Python 3, apoyado en NumPy y Matplotlib, para resolver un problema de minimización bidimensional con límites acotados.
- Analizar el peso de inercia $w$ como parámetro crítico de control del equilibrio entre exploración y explotación dentro de la dinámica del enjambre.
- Validar el comportamiento del algoritmo sobre la función Sphere $f(x,y)=x^2+y^2$, comparando la solución numérica obtenida contra el óptimo teórico conocido en $(0,0)$.

**II. MARCO TEÓRICO**

PSO es una metaheurística de población en la cual un conjunto de partículas explora un espacio de búsqueda continuo. Cada partícula mantiene una posición $x_i(t)$ y una velocidad $v_i(t)$ en la iteración $t$, además de dos referencias fundamentales: su mejor posición histórica, denotada por $pbest_i$, y la mejor posición global encontrada por todo el enjambre, denotada por $gbest$. El algoritmo actualiza la dinámica de cada partícula combinando memoria, atracción individual y atracción social.

**Fundamento principal del algoritmo**

La ecuación de actualización de velocidad empleada en la práctica fue:

$v_i(t+1)=w\,v_i(t)+c_1 r_1\big(pbest_i-x_i(t)\big)+c_2 r_2\big(gbest-x_i(t)\big)$

donde $w$ es el peso de inercia, $c_1$ es el coeficiente cognitivo, $c_2$ es el coeficiente social, y $r_1$, $r_2$ son variables aleatorias uniformes en $[0,1]$. Posteriormente, la posición se actualiza mediante:

$x_i(t+1)=x_i(t)+v_i(t+1)$

El término de inercia preserva parte del movimiento previo; el término cognitivo atrae a la partícula hacia su mejor experiencia individual; y el término social la orienta hacia la mejor solución global del enjambre. Esta combinación permite explorar el espacio de búsqueda al inicio y concentrar la búsqueda alrededor de regiones prometedoras conforme avanza el proceso.

**Análisis de la topología del problema**

La función objetivo seleccionada fue la función Sphere en dos dimensiones, dada por $f(x,y)=x^2+y^2$. Esta función es continua, diferenciable, convexa y unimodal en todo $\mathbb{R}^2$, por lo que posee un único mínimo global. Su gradiente analítico es $\nabla f(x,y)=(2x,2y)$ y su matriz Hessiana es constante, $H=2I$, lo que confirma convexidad estricta. Aunque PSO no utiliza el gradiente para desplazarse, disponer de esta caracterización permite validar con precisión si el algoritmo converge al óptimo correcto.

El mínimo global teórico ocurre en $(x^\*,y^\*)=(0,0)$, con valor óptimo $f(x^\*,y^\*)=0$. Debido a que no existen mínimos locales competidores, esta función es adecuada para evaluar la estabilidad inicial de la implementación y para observar si la dinámica del enjambre reduce el error numérico de manera consistente.

**III. METODOLOGÍA**

**Especificación y descripción del algoritmo**

La implementación desarrollada corresponde a un PSO simple de tipo global-best. En la fase inicial se generaron 30 partículas con posiciones aleatorias uniformes dentro del intervalo $[-5,5]$ para cada dimensión y velocidades iniciales uniformes en el rango $[-1,1]$. Cada partícula evaluó la función objetivo en su posición inicial para establecer su mejor solución personal. Posteriormente, se determinó la mejor partícula del enjambre para inicializar $gbest$.

En cada iteración, para cada partícula, se generaron dos vectores aleatorios $r_1$ y $r_2$, se actualizó la velocidad con la ecuación canónica del algoritmo y luego se actualizó la posición. Si la nueva posición excedía el espacio de búsqueda, se aplicó una proyección por recorte al intervalo permitido mediante una operación de saturación. Después de cada movimiento se evaluó de nuevo la función objetivo, se actualizó $pbest$ si la partícula había mejorado y se actualizó $gbest$ si dicha mejora superaba el mejor valor global vigente.

Además de la solución global, la implementación almacenó el historial de $gbest$ para construir una gráfica de convergencia y registró la trayectoria de la partícula 0 para observar visualmente el desplazamiento de una solución individual hacia la región óptima. El criterio de parada fue un número fijo de 100 iteraciones.

**Configuración de hiperparámetros / parámetros de control**

- Número de partículas: 30. Se eligió un tamaño de enjambre moderado para cubrir el espacio bidimensional sin elevar en exceso el número de evaluaciones.
- Número de dimensiones: 2. Corresponde a la función Sphere implementada en el plano cartesiano.
- Número de iteraciones: 100. Este valor permitió observar una fase rápida de aproximación y una fase final de refinamiento numérico.
- Límites de búsqueda: $[-5,5]$. Se definió un dominio simétrico y suficientemente amplio alrededor del óptimo global.
- Peso de inercia $w$: 0.7. Se utilizó un valor intermedio para conservar capacidad de desplazamiento sin provocar oscilaciones excesivas.
- Coeficiente cognitivo $c_1$: 1.5. Se asignó una atracción individual moderada para mantener la memoria de las mejores experiencias personales.
- Coeficiente social $c_2$: 1.5. Se equilibró la influencia colectiva con la individual para evitar sesgos extremos hacia exploración o explotación.
- Semilla aleatoria: 42. Se fijó para garantizar reproducibilidad exacta de los resultados reportados.

**Funciones de prueba**

La función utilizada fue:

$f(x,y)=x^2+y^2$

Su derivada parcial respecto de cada variable es:

$\frac{\partial f}{\partial x}=2x$, $\frac{\partial f}{\partial y}=2y$

Por tanto, el gradiente es:

$\nabla f(x,y)=(2x,2y)$

Al resolver $\nabla f(x,y)=(0,0)$ se obtiene el punto crítico $(0,0)$. Dado que la Hessiana es positiva definida, dicho punto corresponde al mínimo global teórico de la función. Esta información se utilizó exclusivamente como referencia de validación, ya que el algoritmo PSO no requiere derivadas para operar.

**Pseudocódigo**

1. **Inicialización.** Se generan posiciones y velocidades aleatorias para todas las partículas; se evalúa la función objetivo; se asignan las mejores posiciones personales iniciales y se determina la mejor posición global del enjambre.
2. **Ciclo iterativo.** Para cada partícula se calculan nuevos vectores aleatorios, se actualiza la velocidad con los componentes de inercia, memoria individual y atracción social, y se calcula la nueva posición dentro de los límites permitidos.
3. **Actualización y criterio de parada.** Se vuelve a evaluar la función, se actualizan $pbest$ y $gbest$ cuando existe mejora, se almacena el historial de convergencia y el proceso termina al completar 100 iteraciones.

**Entorno de desarrollo**

- Lenguaje de programación: Python 3, por su sintaxis clara, soporte científico y rapidez de prototipado en prácticas de optimización.
- Bibliotecas utilizadas: NumPy para operaciones numéricas vectorizadas y Matplotlib para generar la gráfica `pso-simple.png`.
- Sistema operativo: Linux.

**IV. RESULTADOS**

**Tablas comparativas**

La Tabla 1 presenta la evolución del mejor valor global del enjambre en iteraciones representativas. El valor de la iteración 0 corresponde al estado inicial del enjambre antes de aplicar la primera actualización.

| Iteración | Mejor valor global $f(gbest)$ |
|---|---:|
| 0 | $3.585544434140$ |
| 1 | $4.865771387579\times10^{-2}$ |
| 2 | $4.865771387579\times10^{-2}$ |
| 5 | $3.893528764621\times10^{-2}$ |
| 10 | $4.040062399725\times10^{-3}$ |
| 20 | $1.016480098859\times10^{-4}$ |
| 40 | $7.314404400061\times10^{-7}$ |
| 60 | $3.110217359368\times10^{-9}$ |
| 80 | $1.192908961297\times10^{-10}$ |
| 100 | $9.116301814501\times10^{-14}$ |

La mejor posición global final fue $(-9.37562534\times10^{-8},\ 2.87006591\times10^{-7})$, mientras que el mejor valor obtenido fue $9.116301814501\times10^{-14}$. En cinco ejecuciones con la misma semilla, el tiempo promedio de cómputo fue $42.206489$ ms, con desviación estándar de $6.030621$ ms, y la desviación estándar del mejor valor final fue $0.0$.

**Gráficas de convergencia**

La figura generada en `practica 4/pso-simple.png` contiene dos vistas complementarias. En el panel izquierdo se observa la curva de convergencia del mejor valor global del enjambre, con una caída abrupta durante las primeras iteraciones y una fase asintótica cercana a cero a partir de la iteración 40. En el panel derecho se muestra la trayectoria de la partícula 0, cuyo movimiento inicia en $(-1.25459881,\ 4.50714306)$ y termina en $(8.95910982\times10^{-6},\ 5.19287536\times10^{-7})$, acercándose visualmente al óptimo real marcado en el origen.

La densidad de puntos en torno a $(0,0)$ aumenta conforme avanza la trayectoria, lo que evidencia una reducción progresiva del tamaño efectivo de los desplazamientos. No se observaron saltos caóticos ni divergencia visual, lo cual es consistente con el comportamiento esperado para una función convexa y con el valor elegido del peso de inercia.

**Comportamiento del parámetro crítico**

El parámetro crítico analizado fue el peso de inercia $w=0.7$. Durante las iteraciones 1 a 10, el mejor valor global descendió de $4.865771387579\times10^{-2}$ a $4.040062399725\times10^{-3}$, lo que indica una fase inicial de exploración controlada. Entre las iteraciones 10 y 40, el valor cayó a $7.314404400061\times10^{-7}$, reflejando un cambio claro hacia explotación de la región cercana al óptimo. Finalmente, entre las iteraciones 40 y 100, el refinamiento numérico llevó la solución hasta $9.116301814501\times10^{-14}$.

Debido a que $w<1$, la contribución de la velocidad previa se amortigua de manera gradual. En este caso, dicho amortiguamiento evitó oscilaciones grandes alrededor del origen, pero no eliminó por completo la capacidad de desplazamiento al inicio del proceso. El comportamiento observado sugiere que el valor seleccionado mantuvo un equilibrio funcional entre movilidad global y refinamiento local.

**V. DISCUSIÓN**

El desempeño del algoritmo fue satisfactorio para la función estudiada. La disminución del mejor valor global desde $3.585544434140$ hasta $9.116301814501\times10^{-14}$ confirmó que la implementación es coherente con la formulación canónica de PSO y que el enjambre fue capaz de aproximarse al mínimo global con error numérico extremadamente bajo. La convergencia rápida observada durante las primeras 20 iteraciones es consistente con la geometría simple de la función Sphere, cuya superficie convexa dirige naturalmente a las partículas hacia el origen incluso sin disponer de información de gradiente.

El hecho de trabajar con una semilla fija produjo repetibilidad total del mejor valor final, lo que facilitó la validación experimental. Sin embargo, ese mismo control reduce la variabilidad estocástica inherente al algoritmo. En un escenario más realista, con semillas distintas y funciones multimodales, podrían aparecer trayectorias mucho más heterogéneas y una mayor dispersión en la calidad final de las soluciones.

**Comportamiento de los parámetros**

El peso de inercia $w$ regula la persistencia del movimiento previo de cada partícula. Si se emplearan valores demasiado altos, por ejemplo cercanos o superiores a 1, la velocidad heredada dominaría el proceso y sería más probable observar oscilaciones amplias, sobrepasos del óptimo e incluso inestabilidad. Si, por el contrario, se eligieran valores demasiado bajos, la exploración disminuiría de manera temprana y el algoritmo podría perder capacidad para recorrer el espacio de búsqueda.

En la práctica realizada, $w=0.7$ funcionó como un valor operativo adecuado para una superficie convexa y acotada. Los coeficientes $c_1=c_2=1.5$ complementaron esa decisión al distribuir de forma balanceada la influencia individual y social. No obstante, afirmar que ese conjunto es universalmente óptimo sería incorrecto, ya que la calibración de PSO depende de la topología del problema, de la dimensionalidad y del criterio de paro.

**Limitaciones**

- La validación se realizó únicamente sobre la función Sphere en dos dimensiones, cuya topología es favorable y no representa la dificultad de funciones multimodales con múltiples mínimos locales.
- Se utilizó una semilla fija para garantizar reproducibilidad, por lo que la desviación estándar nula del mejor valor no debe interpretarse como robustez general del método frente a distintas inicializaciones.
- No se comparó el resultado contra otros algoritmos, como gradiente descendente o recocido simulado, ni se realizó un barrido sistemático de hiperparámetros.

**VI. CONCLUSIONES**

La hipótesis principal de la práctica quedó confirmada: un PSO simple correctamente implementado puede aproximar el mínimo global de una función continua en dos dimensiones con alta precisión numérica. La evidencia experimental mostró una reducción del mejor valor global desde $3.585544434140$ hasta $9.116301814501\times10^{-14}$ en 100 iteraciones, con una estimación final prácticamente indistinguible del óptimo teórico $(0,0)$.

El parámetro crítico más relevante en esta práctica fue el peso de inercia. Para la configuración evaluada, el valor $w=0.7$ resultó operativamente óptimo, no en sentido universal, sino porque proporcionó un equilibrio efectivo entre exploración inicial y explotación final. La caída acelerada del error en las primeras 20 iteraciones y la estabilización posterior sin oscilaciones severas respaldan esta elección para el caso de prueba utilizado.

Desde una perspectiva práctica, PSO es recomendable cuando la función objetivo es compleja, multimodal, ruidosa o no diferenciable, y cuando no se dispone de gradientes confiables. En cambio, no conviene emplearlo como primera opción en problemas convexos, suaves y de baja dimensión, donde métodos como gradiente descendente o Newton suelen converger más rápido, con menor costo computacional y con fundamentos teóricos más sólidos.

**REFERENCIAS**

[1] Kennedy, J., & Eberhart, R. (1995). Particle swarm optimization. *Proceedings of ICNN'95 - International Conference on Neural Networks*, 4, 1942-1948. https://doi.org/10.1109/ICNN.1995.488968

[2] Clerc, M., & Kennedy, J. (2002). The particle swarm—Explosion, stability, and convergence in a multidimensional complex space. *IEEE Transactions on Evolutionary Computation, 6*(1), 58-73. https://doi.org/10.1109/4235.985692

[3] Poli, R., Kennedy, J., & Blackwell, T. (2007). Particle swarm optimization: An overview. *Swarm Intelligence, 1*(1), 33-57. https://doi.org/10.1007/s11721-007-0002-0

[4] Shi, Y., & Eberhart, R. (1998). A modified particle swarm optimizer. *1998 IEEE International Conference on Evolutionary Computation Proceedings*, 69-73. https://doi.org/10.1109/ICEC.1998.699146

[5] Kennedy, J., Eberhart, R. C., & Shi, Y. (2001). *Swarm Intelligence*. Morgan Kaufmann. https://www.sciencedirect.com/book/9781558605954/swarm-intelligence

[6] Schluneker, D., Ploetz, T., Sorensen, M., Kumaar, A., & Duffy, A. (2024). Particle swarm optimization. *Cornell University Computational Optimization Open Textbook*. https://optimization.cbe.cornell.edu/index.php?title=Particle_swarm_optimization

[7] Tam, A. (2021). A gentle introduction to particle swarm optimization. *Machine Learning Mastery*. https://machinelearningmastery.com/a-gentle-introduction-to-particle-swarm-optimization/
