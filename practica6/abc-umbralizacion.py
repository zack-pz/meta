import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def cargar_imagen_grises(ruta_imagen):
    """Carga imagen y la devuelve en escala de grises uint8 [0, 255]."""
    imagen = plt.imread(ruta_imagen)

    if imagen.ndim == 3:
        # Si trae canal alfa, lo descartamos.
        if imagen.shape[2] == 4:
            imagen = imagen[:, :, :3]

        # Conversión RGB -> escala de grises (luminancia perceptual).
        imagen = (
            0.299 * imagen[:, :, 0]
            + 0.587 * imagen[:, :, 1]
            + 0.114 * imagen[:, :, 2]
        )

    imagen = imagen.astype(float)

    # Normalización robusta a [0, 255].
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


def precomputar_objetivo_otsu(prob):
    """
    Precalcula varianza entre clases (criterio de Otsu) para cada umbral t.
    ABC buscará el t que maximiza este criterio.
    """
    niveles = np.arange(256, dtype=float)

    omega = np.cumsum(prob)
    mu = np.cumsum(prob * niveles)
    mu_total = mu[-1]

    numerador = (mu_total * omega - mu) ** 2
    denominador = omega * (1.0 - omega)

    sigma_b2 = np.zeros(256, dtype=float)
    validos = denominador > 1e-12
    sigma_b2[validos] = numerador[validos] / denominador[validos]
    return sigma_b2


def abc_umbral_simple(
    objetivo_por_umbral,
    n_fuentes=24,
    n_iteraciones=120,
    limite=20,
    semilla=42,
):
    """
    Artificial Bee Colony (ABC) para seleccionar un umbral t en [0, 255].

    Cada fuente representa un umbral candidato.
    Se maximiza el criterio objetivo (varianza entre clases de Otsu).
    """
    rng = np.random.default_rng(semilla)

    fuentes = rng.uniform(0, 255, size=n_fuentes)
    intentos = np.zeros(n_fuentes, dtype=int)

    def evaluar(valor_fuente):
        t = int(np.clip(np.rint(valor_fuente), 0, 255))
        return t, float(objetivo_por_umbral[t])

    umbrales = np.zeros(n_fuentes, dtype=int)
    calidades = np.zeros(n_fuentes, dtype=float)

    for i in range(n_fuentes):
        umbrales[i], calidades[i] = evaluar(fuentes[i])

    idx_mejor = int(np.argmax(calidades))
    mejor_umbral = int(umbrales[idx_mejor])
    mejor_calidad = float(calidades[idx_mejor])
    historial_calidad = [mejor_calidad]

    for _ in range(n_iteraciones):
        # 1) Fase de abejas empleadas
        for i in range(n_fuentes):
            k = int(rng.integers(0, n_fuentes - 1))
            if k >= i:
                k += 1

            phi = rng.uniform(-1.0, 1.0)
            candidata = fuentes[i] + phi * (fuentes[i] - fuentes[k])
            candidata = float(np.clip(candidata, 0.0, 255.0))

            t_candidata, q_candidata = evaluar(candidata)

            if q_candidata > calidades[i]:
                fuentes[i] = candidata
                umbrales[i] = t_candidata
                calidades[i] = q_candidata
                intentos[i] = 0
            else:
                intentos[i] += 1

        # 2) Fase de abejas observadoras (selección por ruleta)
        pesos = calidades + 1e-12
        probabilidades = pesos / np.sum(pesos)

        for _ in range(n_fuentes):
            i = int(rng.choice(n_fuentes, p=probabilidades))

            k = int(rng.integers(0, n_fuentes - 1))
            if k >= i:
                k += 1

            phi = rng.uniform(-1.0, 1.0)
            candidata = fuentes[i] + phi * (fuentes[i] - fuentes[k])
            candidata = float(np.clip(candidata, 0.0, 255.0))

            t_candidata, q_candidata = evaluar(candidata)

            if q_candidata > calidades[i]:
                fuentes[i] = candidata
                umbrales[i] = t_candidata
                calidades[i] = q_candidata
                intentos[i] = 0
            else:
                intentos[i] += 1

        # 3) Fase de abejas exploradoras
        for i in range(n_fuentes):
            if intentos[i] >= limite:
                fuentes[i] = rng.uniform(0.0, 255.0)
                umbrales[i], calidades[i] = evaluar(fuentes[i])
                intentos[i] = 0

        idx_iter = int(np.argmax(calidades))
        if calidades[idx_iter] > mejor_calidad:
            mejor_calidad = float(calidades[idx_iter])
            mejor_umbral = int(umbrales[idx_iter])

        historial_calidad.append(mejor_calidad)

    return mejor_umbral, mejor_calidad, np.array(historial_calidad, dtype=float)


def umbralizar(imagen_gris, umbral):
    """Aplica umbralización binaria simple usando t."""
    return np.where(imagen_gris >= umbral, 255, 0).astype(np.uint8)


def guardar_grafica_histograma(histograma, umbral, ruta_salida):
    plt.figure(figsize=(8, 4.5))
    plt.bar(np.arange(256), histograma, width=1.0, color="gray", alpha=0.9)
    plt.axvline(umbral, color="red", linestyle="--", linewidth=2, label=f"Umbral ABC = {umbral}")
    plt.title("Histograma de niveles de gris")
    plt.xlabel("Intensidad")
    plt.ylabel("Frecuencia")
    plt.xlim(0, 255)
    plt.grid(alpha=0.2)
    plt.legend()
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=140)
    plt.close()


def guardar_grafica_convergencia(historial_calidad, ruta_salida):
    plt.figure(figsize=(8, 4.5))
    plt.plot(historial_calidad, color="tab:blue", linewidth=1.8)
    plt.title("Convergencia del ABC (criterio de Otsu)")
    plt.xlabel("Iteración")
    plt.ylabel("Mejor varianza entre clases")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=140)
    plt.close()


def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description="Umbralización simple de una imagen usando Artificial Bee Colony (ABC)."
    )
    parser.add_argument(
        "--imagen",
        type=str,
        required=True,
        help="Ruta de imagen de entrada (obligatoria).",
    )
    parser.add_argument("--fuentes", type=int, default=24, help="Número de fuentes de alimento.")
    parser.add_argument("--iteraciones", type=int, default=120, help="Número de iteraciones de ABC.")
    parser.add_argument("--limite", type=int, default=20, help="Límite de intentos sin mejora.")
    parser.add_argument("--semilla", type=int, default=42, help="Semilla aleatoria reproducible.")
    return parser.parse_args()


def main():
    args = parsear_argumentos()

    carpeta_salida = Path("practica6")
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    ruta_entrada = Path(args.imagen)
    if not ruta_entrada.exists():
        raise FileNotFoundError(f"No existe la imagen de entrada: {ruta_entrada}")
    imagen_gris = cargar_imagen_grises(ruta_entrada)
    nombre_base = ruta_entrada.stem

    hist, prob = construir_histograma_probabilidad(imagen_gris)
    objetivo = precomputar_objetivo_otsu(prob)

    mejor_umbral, mejor_calidad, historial = abc_umbral_simple(
        objetivo_por_umbral=objetivo,
        n_fuentes=args.fuentes,
        n_iteraciones=args.iteraciones,
        limite=args.limite,
        semilla=args.semilla,
    )

    imagen_binaria = umbralizar(imagen_gris, mejor_umbral)

    ruta_umbralizada = carpeta_salida / f"{nombre_base}-umbralizada-abc.png"
    ruta_histograma = carpeta_salida / f"{nombre_base}-histograma.png"
    ruta_convergencia = carpeta_salida / f"{nombre_base}-convergencia-abc.png"

    plt.imsave(ruta_umbralizada, imagen_binaria, cmap="gray", vmin=0, vmax=255)
    guardar_grafica_histograma(hist, mejor_umbral, ruta_histograma)
    guardar_grafica_convergencia(historial, ruta_convergencia)

    print("\nRESULTADO FINAL (Umbralización simple con ABC)")
    print(f"Umbral óptimo encontrado: {mejor_umbral}")
    print(f"Mejor valor objetivo (Otsu): {mejor_calidad:.6f}")
    print(f"Imagen binaria guardada en: {ruta_umbralizada}")
    print(f"Histograma guardado en: {ruta_histograma}")
    print(f"Convergencia guardada en: {ruta_convergencia}")


if __name__ == "__main__":
    main()
