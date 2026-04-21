# Segmentación de imágenes multinivel con Ant Colony Optimization (ACO)

Esta práctica implementa una **segmentación multinivel** en escala de grises usando **Ant Colony Optimization (ACO)** para encontrar múltiples umbrales óptimos.

La función objetivo que se maximiza es la **varianza entre clases de Otsu multinivel**.

## Archivo principal

- `practica7/aco-segmentacion-multinivel.py`

## Idea general

1. Se calcula el histograma de la imagen en grises.
2. Cada hormiga propone un conjunto ordenado de umbrales `t1 < t2 < ... < tk`.
3. ACO ajusta las probabilidades de selección con:
   - **Feromonas** (memoria colectiva)
   - **Heurística** (valles del histograma)
4. Se conserva la mejor solución global por iteración.
5. Con los umbrales finales, la imagen se cuantiza en `N` niveles.

## Cómo ejecutar

Desde la raíz del proyecto:

```bash
python practica7/aco-segmentacion-multinivel.py --imagen "ruta/a/imagen.png" --niveles 4
```

Parámetros principales:

- `--imagen` (obligatorio): ruta de imagen de entrada.
- `--niveles` (default `4`): niveles finales de segmentación.
- `--hormigas` (default `32`): número de hormigas por iteración.
- `--iteraciones` (default `140`): iteraciones de ACO.
- `--alpha` (default `1.0`): peso de feromonas.
- `--beta` (default `2.0`): peso de heurística.
- `--rho` (default `0.20`): evaporación de feromonas.
- `--q` (default `1.0`): depósito de feromonas.
- `--semilla` (default `42`): reproducibilidad.

## Ejemplo de ejecución

```bash
python practica7/aco-segmentacion-multinivel.py --imagen "practica6/metal_flesh.jpg" --niveles 4
```

## Salidas

El script genera en `practica7/`:

- `*-segmentada-aco-<niveles>niveles.png`: imagen segmentada.
- `*-histograma-umbrales-aco.png`: histograma con umbrales óptimos.
- `*-convergencia-aco.png`: curva de convergencia del mejor valor objetivo.
- `*-comparacion-aco.png`: comparación visual original vs segmentada.
