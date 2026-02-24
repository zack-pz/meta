# Optimización con Simulated Annealing (Recocido Simulado)

Este proyecto implementa el algoritmo de **Recocido Simulado** (Simulated Annealing) para encontrar el mínimo global de la función matemática `peaks`. El código incluye una mejora de "saltos aleatorios" para evitar que el algoritmo se quede atrapado en mínimos locales.

## Características del Código

- **Función Objetivo:** Utiliza la función `peaks` (común en optimización) que presenta múltiples picos y valles.
- **Enfriamiento Adaptativo:** La temperatura disminuye gradualmente para pasar de una exploración amplia a una explotación local.
- **Saltos Aleatorios:** Si tras un número determinado de iteraciones no hay mejora, el algoritmo salta a una nueva posición aleatoria y "recalienta" ligeramente el sistema.
- **Visualización:** Genera un gráfico de contorno con la trayectoria del algoritmo, los puntos de inicio, los saltos realizados y la mejor solución encontrada.

## Requisitos

Las dependencias principales son:
- `numpy`
- `matplotlib`

## Configuración del Entorno

### Opción 1: Usando `venv` (Estándar)

1. Crear el entorno virtual:
   ```bash
   python -m venv .venv
   ```
2. Activar el entorno:
   - **Linux/macOS:** `source .venv/bin/activate`
   - **Windows:** `.venv\Scripts\activate`
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Opción 2: Usando `uv` (Recomendado por velocidad)

1. Crear el entorno e instalar dependencias:
   ```bash
   uv venv
   source .venv/bin/activate  # O el comando de activación correspondiente
   uv pip install -r requirements.txt
   ```
   *Nota: También puedes usar `uv run template.py` directamente si tienes `uv` configurado.*

## Ejecución

Para ejecutar el script y ver la visualización de la optimización:

```bash
python template.py
```

Al finalizar, se abrirá una ventana con el gráfico de la optimización y se imprimirán los resultados en la terminal.
