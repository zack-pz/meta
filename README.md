# Repositorio de algoritmos metaheurísticos y optimización

Este repositorio reúne las prácticas y ejercicios de **optimización** trabajados en clase, con enfoque principal en la implementación de **algoritmos metaheurísticos**. La idea es documentar y comparar distintas estrategias de búsqueda para resolver problemas de optimización, tanto deterministas como bioinspirados.

## Objetivo del repositorio

Centralizar los algoritmos que fueron dejados en la clase, mostrando su lógica, su implementación en Python y, en varios casos, su comportamiento mediante visualizaciones.

## Algoritmos implementados

### 1. Gradiente descendente en 1D
- **Ubicación:** `practica2/gradiante.py`
- **Tipo:** algoritmo de optimización determinista
- **Descripción breve:** minimiza la función `f(x) = x^2 - 5x + 10` avanzando en dirección opuesta al gradiente. Aunque no es una metaheurística, sirve como base para entender cómo una estrategia de búsqueda mejora una solución paso a paso.

### 2. Temple simulado estándar
- **Ubicación:** `practica3/temple-estandar.py`
- **Tipo:** metaheurística
- **Descripción breve:** explora la función `Peaks` permitiendo aceptar, con cierta probabilidad, soluciones peores cuando la temperatura es alta. Esto ayuda a evitar quedar atrapado demasiado pronto en mínimos locales.

### 3. Temple simulado híbrido (versión de clase)
- **Ubicación:** `practica3/temple-clase.py`
- **Tipo:** metaheurística
- **Descripción breve:** es una variante del temple simulado que agrega **detección de estancamiento**, **saltos aleatorios** y **recalentamiento**. Su objetivo es mejorar la exploración del espacio de búsqueda y escapar con más facilidad de óptimos locales.

### 4. Optimización por enjambre de partículas (PSO)
- **Ubicación:** `practica4/pso-simple.py`
- **Tipo:** metaheurística
- **Descripción breve:** simula un conjunto de partículas que se mueven por el espacio de búsqueda ajustando su trayectoria según su mejor posición individual y la mejor posición global encontrada por el enjambre.

### 5. Artificial Bee Colony (ABC)
- **Ubicación:** `ABC/abc.py`
- **Tipo:** metaheurística
- **Descripción breve:** está inspirado en el comportamiento de búsqueda de alimento de una colonia de abejas. Las soluciones candidatas se refinan mediante exploración y explotación para encontrar mejores valores de aptitud.

## Estructura del proyecto

```text
.
├── ABC/
│   └── abc.py
├── practica2/
│   ├── ALGORITMOS.md
│   └── gradiante.py
├── practica3/
│   ├── ALGORITMOS.md
│   ├── README.md
│   ├── temple-clase.py
│   └── temple-estandar.py
├── practica4/
│   └── pso-simple.py
├── README.md
└── requirements.txt
```

## Requisitos

Las dependencias usadas en el repositorio son:

- `numpy`
- `matplotlib`

Instalación:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución de los ejemplos

Desde la raíz del proyecto podés ejecutar cada práctica con comandos como estos:

```bash
python practica2/gradiante.py
python practica3/temple-estandar.py
python practica3/temple-clase.py
python practica4/pso-simple.py
python ABC/abc.py
```

## Documentación adicional

- `practica2/ALGORITMOS.md`: pseudocódigo y explicación del gradiente descendente.
- `practica3/ALGORITMOS.md`: pseudocódigo y diagramas de flujo de las variantes de temple simulado.
- `practica3/README.md`: explicación comparativa entre temple estándar y temple híbrido.

## Enfoque académico

Este repositorio está orientado al aprendizaje y análisis de algoritmos vistos en clase. Más que presentar una librería lista para producción, busca dejar claro **cómo funciona cada algoritmo**, **qué problema resuelve** y **cómo cambia su comportamiento según la estrategia de búsqueda utilizada**.
