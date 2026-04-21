import argparse
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


def construir_histograma_probabilidad(imagen_gris):
    """Regresa histograma absoluto y probabilidad para intensidades 0..255."""
    hist = np.bincount(imagen_gris.ravel(), minlength=256).astype(float)
    prob = hist / np.sum(hist)
    return hist, prob


def precomputar_acumuladas(probabilidad):
    """Precalcula sumas acumuladas para evaluación rápida del objetivo Otsu."""
    niveles = np.arange(256, dtype=float)
    omega = np.cumsum(probabilidad)
    mu = np.cumsum(probabilidad * niveles)
    mu_total = float(mu[-1])
    return omega, mu, mu_total


def suma_en_rango(acumulada, inicio, fin):
    """Suma en rango [inicio, fin] usando una señal acumulada."""
    if inicio > fin:
        return 0.0
    if inicio <= 0:
        return float(acumulada[fin])
    return float(acumulada[fin] - acumulada[inicio - 1])


def evaluar_otsu_multinivel(umbrales, omega, mu, mu_total):
    """
    Evalúa la varianza entre clases de Otsu para múltiples umbrales.

    Si hay clases vacías (peso ~0), se penaliza con 0.0.
    """
    limites = [-1, *umbrales, 255]
    sigma_b2 = 0.0

    for i in range(len(limites) - 1):
        inicio = limites[i] + 1
        fin = limites[i + 1]

        peso = suma_en_rango(omega, inicio, fin)
        if peso <= 1e-12:
            return 0.0

        media = suma_en_rango(mu, inicio, fin) / peso
        sigma_b2 += peso * (media - mu_total) ** 2

    return float(sigma_b2)


def construir_heuristica_valle(histograma):
    """
    Heurística para ACO: favorece intensidades en valles del histograma.

    Cuanto menor frecuencia local, mayor valor heurístico.
    """
    kernel = np.array([1.0, 2.0, 3.0, 2.0, 1.0], dtype=float)
    kernel = kernel / np.sum(kernel)
    suavizado = np.convolve(histograma, kernel, mode="same")

    heuristica = 1.0 / (suavizado + 1.0)
    heuristica = heuristica / (np.max(heuristica) + 1e-12)
    return np.clip(heuristica, 1e-8, None)


def aco_umbralizacion_multinivel(
    omega,
    mu,
    mu_total,
    histograma,
    n_umbrales,
    n_hormigas=32,
    n_iteraciones=140,
    alpha=1.0,
    beta=2.0,
    rho=0.20,
    q=1.0,
    semilla=42,
):
    """
    ACO para buscar umbrales múltiples en [0, 255].

    Cada hormiga construye una secuencia estrictamente creciente de umbrales.
    Se maximiza el criterio de Otsu multinivel.
    """
    if n_umbrales < 1:
        raise ValueError("n_umbrales debe ser >= 1")

    rng = np.random.default_rng(semilla)
    feromonas = np.ones((n_umbrales, 256), dtype=float)
    heuristica = construir_heuristica_valle(histograma)

    mejor_umbrales = None
    mejor_calidad = -np.inf
    historial = []

    for _ in range(n_iteraciones):
        soluciones = []

        for _ in range(n_hormigas):
            umbrales = []
            inferior = 0

            for j in range(n_umbrales):
                superior = 255 - (n_umbrales - j - 1)
                candidatos = np.arange(inferior, superior + 1, dtype=int)

                tau = np.power(feromonas[j, candidatos], alpha)
                eta = np.power(heuristica[candidatos], beta)
                pesos = tau * eta + 1e-12
                probabilidades = pesos / np.sum(pesos)

                elegido = int(rng.choice(candidatos, p=probabilidades))
                umbrales.append(elegido)
                inferior = elegido + 1

            calidad = evaluar_otsu_multinivel(umbrales, omega, mu, mu_total)
            soluciones.append((np.array(umbrales, dtype=int), float(calidad)))

            if calidad > mejor_calidad:
                mejor_calidad = float(calidad)
                mejor_umbrales = np.array(umbrales, dtype=int)

        feromonas *= 1.0 - rho

        soluciones_ordenadas = sorted(soluciones, key=lambda x: x[1], reverse=True)
        top_k = max(1, n_hormigas // 5)
        referencia = soluciones_ordenadas[0][1] + 1e-12

        for umbrales, calidad in soluciones_ordenadas[:top_k]:
            delta = q * (calidad / referencia)
            for j, t in enumerate(umbrales):
                feromonas[j, t] += delta

        for j, t in enumerate(mejor_umbrales):
            feromonas[j, t] += q

        feromonas = np.clip(feromonas, 1e-8, 1e6)
        historial.append(mejor_calidad)

    return mejor_umbrales, mejor_calidad, np.array(historial, dtype=float)


def segmentar_multinivel(imagen_gris, umbrales):
    """Segmenta la imagen en N niveles según los umbrales encontrados."""
    umbrales = np.sort(np.asarray(umbrales, dtype=int))
    bordes = np.concatenate(([0], umbrales + 1, [256]))

    imagen_segmentada = np.zeros_like(imagen_gris, dtype=np.uint8)
    tonos = np.linspace(0, 255, len(bordes) - 1, dtype=np.uint8)

    for i in range(len(bordes) - 1):
        inicio, fin = int(bordes[i]), int(bordes[i + 1])
        mascara = (imagen_gris >= inicio) & (imagen_gris < fin)
        imagen_segmentada[mascara] = tonos[i]

    return imagen_segmentada


def guardar_histograma_con_umbrales(histograma, umbrales, ruta_salida):
    plt.figure(figsize=(8.5, 4.8))
    plt.bar(np.arange(256), histograma, width=1.0, color="gray", alpha=0.9)

    for i, t in enumerate(umbrales, start=1):
        plt.axvline(
            int(t),
            color="red",
            linestyle="--",
            linewidth=1.8,
            label=f"t{i}={int(t)}",
        )

    plt.title("Histograma y umbrales óptimos (ACO multinivel)")
    plt.xlabel("Intensidad")
    plt.ylabel("Frecuencia")
    plt.xlim(0, 255)
    plt.grid(alpha=0.2)
    plt.legend()
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close()


def guardar_convergencia(historial, ruta_salida):
    plt.figure(figsize=(8.5, 4.8))
    plt.plot(historial, color="tab:blue", linewidth=1.9)
    plt.title("Convergencia de ACO (Otsu multinivel)")
    plt.xlabel("Iteración")
    plt.ylabel("Mejor valor objetivo")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close()


def guardar_comparacion(imagen_original, imagen_segmentada, ruta_salida):
    fig, ejes = plt.subplots(1, 2, figsize=(10, 4.8))
    ejes[0].imshow(imagen_original, cmap="gray", vmin=0, vmax=255)
    ejes[0].set_title("Imagen original")
    ejes[0].axis("off")

    ejes[1].imshow(imagen_segmentada, cmap="gray", vmin=0, vmax=255)
    ejes[1].set_title("Segmentación multinivel (ACO)")
    ejes[1].axis("off")

    plt.tight_layout()
    fig.savefig(ruta_salida, dpi=150)
    plt.close(fig)


def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description=(
            "Segmentación multinivel de imagen usando Ant Colony Optimization (ACO) "
            "y criterio de Otsu multinivel."
        )
    )
    parser.add_argument(
        "--imagen",
        type=str,
        required=True,
        help="Ruta de imagen de entrada (obligatoria).",
    )
    parser.add_argument(
        "--niveles",
        type=int,
        default=4,
        help="Número de niveles de segmentación (>=2).",
    )
    parser.add_argument("--hormigas", type=int, default=32, help="Número de hormigas.")
    parser.add_argument("--iteraciones", type=int, default=140, help="Iteraciones de ACO.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Peso de feromonas.")
    parser.add_argument("--beta", type=float, default=2.0, help="Peso de la heurística.")
    parser.add_argument("--rho", type=float, default=0.20, help="Tasa de evaporación.")
    parser.add_argument("--q", type=float, default=1.0, help="Intensidad de depósito.")
    parser.add_argument("--semilla", type=int, default=42, help="Semilla reproducible.")
    return parser.parse_args()


def main():
    args = parsear_argumentos()

    if args.niveles < 2:
        raise ValueError("--niveles debe ser >= 2")

    n_umbrales = args.niveles - 1
    if n_umbrales >= 256:
        raise ValueError("El número de umbrales debe ser menor que 256")

    ruta_entrada = Path(args.imagen)
    if not ruta_entrada.exists():
        raise FileNotFoundError(f"No existe la imagen de entrada: {ruta_entrada}")

    carpeta_salida = Path("practica7")
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    imagen_gris = cargar_imagen_grises(ruta_entrada)
    histograma, probabilidad = construir_histograma_probabilidad(imagen_gris)
    omega, mu, mu_total = precomputar_acumuladas(probabilidad)

    mejores_umbrales, mejor_calidad, historial = aco_umbralizacion_multinivel(
        omega=omega,
        mu=mu,
        mu_total=mu_total,
        histograma=histograma,
        n_umbrales=n_umbrales,
        n_hormigas=args.hormigas,
        n_iteraciones=args.iteraciones,
        alpha=args.alpha,
        beta=args.beta,
        rho=args.rho,
        q=args.q,
        semilla=args.semilla,
    )

    imagen_segmentada = segmentar_multinivel(imagen_gris, mejores_umbrales)
    nombre_base = ruta_entrada.stem

    ruta_segmentada = carpeta_salida / f"{nombre_base}-segmentada-aco-{args.niveles}niveles.png"
    ruta_histograma = carpeta_salida / f"{nombre_base}-histograma-umbrales-aco.png"
    ruta_convergencia = carpeta_salida / f"{nombre_base}-convergencia-aco.png"
    ruta_comparacion = carpeta_salida / f"{nombre_base}-comparacion-aco.png"

    plt.imsave(ruta_segmentada, imagen_segmentada, cmap="gray", vmin=0, vmax=255)
    guardar_histograma_con_umbrales(histograma, mejores_umbrales, ruta_histograma)
    guardar_convergencia(historial, ruta_convergencia)
    guardar_comparacion(imagen_gris, imagen_segmentada, ruta_comparacion)

    print("\nRESULTADO FINAL (Segmentación multinivel con ACO)")
    print(f"Niveles de segmentación: {args.niveles}")
    print(f"Umbrales óptimos encontrados: {mejores_umbrales.tolist()}")
    print(f"Mejor valor objetivo (Otsu multinivel): {mejor_calidad:.6f}")
    print(f"Imagen segmentada guardada en: {ruta_segmentada}")
    print(f"Histograma con umbrales guardado en: {ruta_histograma}")
    print(f"Convergencia guardada en: {ruta_convergencia}")
    print(f"Comparación guardada en: {ruta_comparacion}")


if __name__ == "__main__":
    main()
