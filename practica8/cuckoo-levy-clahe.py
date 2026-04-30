import argparse
from math import gamma, pi, sin
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def cargar_imagen_grises(ruta_imagen):
    """Carga imagen y la devuelve en escala de grises uint8 [0, 255]."""
    imagen = plt.imread(ruta_imagen)

    if imagen.ndim == 3:
        if imagen.shape[2] == 4:
            imagen = imagen[:, :, :3]

        imagen = (
            0.299 * imagen[:, :, 0]
            + 0.587 * imagen[:, :, 1]
            + 0.114 * imagen[:, :, 2]
        )

    imagen = imagen.astype(float)
    maximo = float(np.max(imagen)) if imagen.size else 0.0
    minimo = float(np.min(imagen)) if imagen.size else 0.0

    if maximo <= 1.0:
        imagen = imagen * 255.0
    elif maximo > 255.0 or minimo < 0.0:
        denominador = max(maximo - minimo, 1e-12)
        imagen = 255.0 * (imagen - minimo) / denominador

    return np.clip(imagen, 0, 255).astype(np.uint8)


def clip_histograma_y_redistribuir(histograma, limite_clip):
    """CLAHE simple: recorta el histograma y reparte el exceso."""
    hist = histograma.astype(float).copy()
    exceso = np.sum(np.clip(hist - limite_clip, 0.0, None))
    hist = np.minimum(hist, limite_clip)
    hist += exceso / 256.0
    return hist


def construir_cdf_clahe(tile, clip_limit_relativo):
    """Construye la CDF ecualizada de un tile usando clipping."""
    total_pixeles = tile.size
    hist = np.bincount(tile.ravel(), minlength=256).astype(float)

    limite_clip = max(1.0, clip_limit_relativo * total_pixeles / 256.0)
    hist_clip = clip_histograma_y_redistribuir(hist, limite_clip)

    cdf = np.cumsum(hist_clip)
    cdf = 255.0 * cdf / max(cdf[-1], 1e-12)
    return cdf


def localizar_tiles_vecinos(posicion, centros):
    """Obtiene tiles vecinos y peso lineal para una coordenada 1D."""
    if len(centros) == 1:
        return 0, 0, 0.0

    if posicion <= centros[0]:
        return 0, 0, 0.0

    if posicion >= centros[-1]:
        ultimo = len(centros) - 1
        return ultimo, ultimo, 0.0

    derecha = int(np.searchsorted(centros, posicion, side="right"))
    izquierda = derecha - 1
    distancia = centros[derecha] - centros[izquierda]
    peso = (posicion - centros[izquierda]) / max(distancia, 1e-12)
    return izquierda, derecha, float(peso)


def aplicar_clahe_simple(imagen_gris, clip_limit=2.0, tile_size=32):
    """
    CLAHE didáctico con interpolación bilineal entre tiles.

    Divide la imagen en bloques, ecualiza cada bloque con límite de clipping
    y luego mezcla las transformaciones vecinas para evitar la cuadrícula.
    """
    alto, ancho = imagen_gris.shape
    y_inicios = list(range(0, alto, tile_size))
    x_inicios = list(range(0, ancho, tile_size))

    cdfs = []
    centros_y = []
    for y in y_inicios:
        fila_cdfs = []
        h_tile = min(tile_size, alto - y)
        centros_y.append(y + (h_tile - 1) / 2.0)

        fila_centros_x = []
        for x in x_inicios:
            w_tile = min(tile_size, ancho - x)
            tile = imagen_gris[y : y + h_tile, x : x + w_tile]
            fila_cdfs.append(construir_cdf_clahe(tile, clip_limit_relativo=clip_limit))
            fila_centros_x.append(x + (w_tile - 1) / 2.0)

        cdfs.append(fila_cdfs)

    centros_x = np.array(fila_centros_x, dtype=float)
    centros_y = np.array(centros_y, dtype=float)

    salida = np.zeros((alto, ancho), dtype=float)

    for y in range(alto):
        fila_superior, fila_inferior, wy = localizar_tiles_vecinos(y, centros_y)

        for x in range(ancho):
            col_izquierda, col_derecha, wx = localizar_tiles_vecinos(x, centros_x)
            intensidad = int(imagen_gris[y, x])

            cdf_tl = cdfs[fila_superior][col_izquierda][intensidad]
            cdf_tr = cdfs[fila_superior][col_derecha][intensidad]
            cdf_bl = cdfs[fila_inferior][col_izquierda][intensidad]
            cdf_br = cdfs[fila_inferior][col_derecha][intensidad]

            superior = (1.0 - wx) * cdf_tl + wx * cdf_tr
            inferior = (1.0 - wx) * cdf_bl + wx * cdf_br
            salida[y, x] = (1.0 - wy) * superior + wy * inferior

    return np.clip(np.rint(salida), 0, 255).astype(np.uint8)


def entropia_imagen(imagen):
    hist = np.bincount(imagen.ravel(), minlength=256).astype(float)
    prob = hist / max(np.sum(hist), 1.0)
    prob = prob[prob > 1e-12]
    return float(-np.sum(prob * np.log2(prob)))


def evaluar_contraste(imagen_mejorada):
    """
    Función objetivo simple.

    - Desviación estándar alta => más dispersión de intensidades.
    - Entropía alta => más detalle tonal.
    """
    desviacion = float(np.std(imagen_mejorada)) / 64.0
    entropia = entropia_imagen(imagen_mejorada) / 8.0
    return desviacion + entropia


def levy_flight(rng, beta=1.5, dimension=2):
    """Genera un paso de Lévy con el método de Mantegna."""
    numerador = gamma(1 + beta) * sin(pi * beta / 2)
    denominador = gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2)
    sigma_u = (numerador / denominador) ** (1 / beta)

    u = rng.normal(0.0, sigma_u, size=dimension)
    v = rng.normal(0.0, 1.0, size=dimension)
    paso = u / (np.abs(v) ** (1.0 / beta) + 1e-12)
    return paso


def decodificar_solucion(solucion):
    """Pasa del vector continuo a parámetros válidos de CLAHE."""
    clip_limit = float(np.clip(solucion[0], 0.5, 4.0))
    tile_size = int(np.clip(np.rint(solucion[1]), 8, 64))
    return clip_limit, tile_size


def evaluar_solucion(solucion, imagen_gris):
    clip_limit, tile_size = decodificar_solucion(solucion)
    imagen_mejorada = aplicar_clahe_simple(
        imagen_gris,
        clip_limit=clip_limit,
        tile_size=tile_size,
    )
    calidad = evaluar_contraste(imagen_mejorada)
    return calidad, imagen_mejorada, clip_limit, tile_size


def cuckoo_search_clahe(
    imagen_gris,
    n_nidos=12,
    n_iteraciones=40,
    pa=0.25,
    alpha=0.25,
    semilla=42,
):
    """
    Cuckoo Search MUY simple para optimizar CLAHE.

    Cada nido = [clip_limit, tile_size].
    Los vuelos de Lévy generan saltos grandes/pequeños para explorar.
    """
    rng = np.random.default_rng(semilla)

    limites_min = np.array([0.5, 8.0], dtype=float)
    limites_max = np.array([4.0, 64.0], dtype=float)
    escala = limites_max - limites_min

    nidos = rng.uniform(limites_min, limites_max, size=(n_nidos, 2))
    calidades = np.zeros(n_nidos, dtype=float)
    imagenes = [None] * n_nidos

    for i in range(n_nidos):
        calidades[i], imagenes[i], _, _ = evaluar_solucion(nidos[i], imagen_gris)

    idx_mejor = int(np.argmax(calidades))
    mejor_nido = nidos[idx_mejor].copy()
    mejor_calidad = float(calidades[idx_mejor])
    mejor_imagen = imagenes[idx_mejor]
    historial = [mejor_calidad]

    for _ in range(n_iteraciones):
        for i in range(n_nidos):
            paso = levy_flight(rng, beta=1.5, dimension=2)
            candidata = nidos[i] + alpha * paso * (nidos[i] - mejor_nido + 1e-12) * escala
            candidata = np.clip(candidata, limites_min, limites_max)

            calidad_candidata, imagen_candidata, _, _ = evaluar_solucion(candidata, imagen_gris)
            j = int(rng.integers(0, n_nidos))

            if calidad_candidata > calidades[j]:
                nidos[j] = candidata
                calidades[j] = calidad_candidata
                imagenes[j] = imagen_candidata

        n_abandonar = max(1, int(pa * n_nidos))
        peores = np.argsort(calidades)[:n_abandonar]
        for idx in peores:
            nidos[idx] = rng.uniform(limites_min, limites_max, size=2)
            calidades[idx], imagenes[idx], _, _ = evaluar_solucion(nidos[idx], imagen_gris)

        idx_mejor = int(np.argmax(calidades))
        if calidades[idx_mejor] > mejor_calidad:
            mejor_calidad = float(calidades[idx_mejor])
            mejor_nido = nidos[idx_mejor].copy()
            mejor_imagen = imagenes[idx_mejor]

        historial.append(mejor_calidad)

    clip_limit, tile_size = decodificar_solucion(mejor_nido)
    return clip_limit, tile_size, mejor_calidad, mejor_imagen, np.array(historial, dtype=float)


def guardar_convergencia(historial, ruta_salida):
    plt.figure(figsize=(8, 4.5))
    plt.plot(historial, color="tab:blue", linewidth=1.8)
    plt.title("Convergencia de Cuckoo Search")
    plt.xlabel("Iteración")
    plt.ylabel("Mejor calidad")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=140)
    plt.close()


def guardar_comparacion(imagen_original, imagen_mejorada, ruta_salida):
    fig, ejes = plt.subplots(1, 2, figsize=(10, 4.8))

    ejes[0].imshow(imagen_original, cmap="gray", vmin=0, vmax=255)
    ejes[0].set_title("Imagen original")
    ejes[0].axis("off")

    ejes[1].imshow(imagen_mejorada, cmap="gray", vmin=0, vmax=255)
    ejes[1].set_title("CLAHE optimizado con Cuckoo")
    ejes[1].axis("off")

    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=140)
    plt.close(fig)


def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description=(
            "Mejora de contraste usando una versión didáctica de "
            "Cuckoo Search + vuelos de Lévy + CLAHE."
        )
    )
    parser.add_argument(
        "--imagen",
        type=str,
        required=True,
        help="Ruta de imagen de entrada (obligatoria).",
    )
    parser.add_argument("--nidos", type=int, default=12, help="Número de nidos.")
    parser.add_argument("--iteraciones", type=int, default=40, help="Número de iteraciones.")
    parser.add_argument("--pa", type=float, default=0.25, help="Fracción de nidos a abandonar.")
    parser.add_argument("--alpha", type=float, default=0.25, help="Escala del vuelo de Lévy.")
    parser.add_argument("--semilla", type=int, default=42, help="Semilla reproducible.")
    return parser.parse_args()


def main():
    args = parsear_argumentos()

    carpeta_salida = Path("practica8")
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    ruta_entrada = Path(args.imagen)
    if not ruta_entrada.exists():
        raise FileNotFoundError(f"No existe la imagen de entrada: {ruta_entrada}")

    imagen_gris = cargar_imagen_grises(ruta_entrada)
    nombre_base = ruta_entrada.stem

    clip_limit, tile_size, mejor_calidad, imagen_mejorada, historial = cuckoo_search_clahe(
        imagen_gris=imagen_gris,
        n_nidos=args.nidos,
        n_iteraciones=args.iteraciones,
        pa=args.pa,
        alpha=args.alpha,
        semilla=args.semilla,
    )

    ruta_mejorada = carpeta_salida / f"{nombre_base}-clahe-cuckoo.png"
    ruta_convergencia = carpeta_salida / f"{nombre_base}-convergencia-cuckoo.png"
    ruta_comparacion = carpeta_salida / f"{nombre_base}-comparacion-cuckoo.png"

    plt.imsave(ruta_mejorada, imagen_mejorada, cmap="gray", vmin=0, vmax=255)
    guardar_convergencia(historial, ruta_convergencia)
    guardar_comparacion(imagen_gris, imagen_mejorada, ruta_comparacion)

    print("\nRESULTADO FINAL (Cuckoo Search + Lévy + CLAHE simple)")
    print(f"clip_limit óptimo: {clip_limit:.3f}")
    print(f"tile_size óptimo: {tile_size}")
    print(f"Mejor calidad: {mejor_calidad:.6f}")
    print(f"Imagen mejorada guardada en: {ruta_mejorada}")
    print(f"Convergencia guardada en: {ruta_convergencia}")
    print(f"Comparación guardada en: {ruta_comparacion}")


if __name__ == "__main__":
    main()
