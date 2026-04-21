# Umbralización simple de imagen con Artificial Bee Colony (ABC)

Esta práctica implementa una **umbralización binaria simple** donde el umbral `t` (0 a 255) se busca con el algoritmo **Artificial Bee Colony (ABC)**.

La calidad de cada umbral se evalúa con el criterio de **varianza entre clases de Otsu**:

- clase 0: píxeles con intensidad `< t`
- clase 1: píxeles con intensidad `>= t`

ABC intenta **maximizar** esa varianza entre clases para obtener la mejor separación fondo/objeto.

## Archivo principal

- `practica6/abc-umbralizacion.py`

## Cómo ejecutar

Desde la raíz del proyecto:

```bash
python practica6/abc-umbralizacion.py --imagen "ruta/a/tu/imagen.png"
```

El parámetro `--imagen` ahora es **obligatorio**.

Parámetros opcionales:

- `--fuentes` (default `24`): número de fuentes de alimento.
- `--iteraciones` (default `120`): iteraciones del ABC.
- `--limite` (default `20`): intentos sin mejora antes de fase exploradora.
- `--semilla` (default `42`): semilla para reproducibilidad.

## Salidas

El script guarda en `practica6/`:

- `*-umbralizada-abc.png`: imagen binaria final.
- `*-histograma.png`: histograma con línea vertical del umbral encontrado.
- `*-convergencia-abc.png`: evolución del mejor valor objetivo por iteración.
