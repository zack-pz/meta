import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def generar_ciudades(n_ciudades=20, semilla=7):
    """Genera coordenadas 2D reproducibles para el TSP."""
    rng = np.random.default_rng(semilla)
    return rng.uniform(0, 100, size=(n_ciudades, 2))


def matriz_distancias(ciudades):
    """Calcula la matriz de distancias euclidianas entre ciudades."""
    dif = ciudades[:, np.newaxis, :] - ciudades[np.newaxis, :, :]
    return np.sqrt(np.sum(dif**2, axis=2))


def distancia_ruta(ruta, distancias):
    """Suma la distancia total de la ruta cerrada (vuelve al inicio)."""
    return np.sum(distancias[ruta, np.roll(ruta, -1)])


def vecino(ruta, rng):
    """
    Genera un vecino para problema combinatorio:
    - swap de 2 ciudades, o
    - inversión de un segmento.
    """
    nueva = ruta.copy()
    i, j = sorted(rng.choice(len(ruta), size=2, replace=False))

    if rng.random() < 0.5:
        nueva[i], nueva[j] = nueva[j], nueva[i]
    else:
        nueva[i : j + 1] = nueva[i : j + 1][::-1]

    return nueva


def abc_tsp(
    distancias,
    n_fuentes=40,
    n_iteraciones=300,
    limite=35,
    semilla=42,
):
    """
    Artificial Bee Colony (ABC) básico para TSP.

    Fases:
    1) Empleadas: exploran vecindad de su fuente.
    2) Observadoras: eligen fuentes por ruleta según calidad.
    3) Exploradoras: reinician fuentes estancadas.
    """
    rng = np.random.default_rng(semilla)
    n_ciudades = distancias.shape[0]

    # Fuentes de alimento iniciales (permutaciones)
    fuentes = np.array([rng.permutation(n_ciudades) for _ in range(n_fuentes)])
    costos = np.array([distancia_ruta(r, distancias) for r in fuentes], dtype=float)
    intentos = np.zeros(n_fuentes, dtype=int)

    idx_mejor = np.argmin(costos)
    mejor_ruta = fuentes[idx_mejor].copy()
    mejor_costo = costos[idx_mejor]
    historial = [mejor_costo]

    for it in range(n_iteraciones):
        # -------------------------
        # 1) Abejas empleadas
        # -------------------------
        for i in range(n_fuentes):
            candidata = vecino(fuentes[i], rng)
            costo_candidata = distancia_ruta(candidata, distancias)

            if costo_candidata < costos[i]:
                fuentes[i] = candidata
                costos[i] = costo_candidata
                intentos[i] = 0
            else:
                intentos[i] += 1

        # -------------------------
        # 2) Abejas observadoras
        # -------------------------
        aptitud = 1.0 / (1.0 + costos)  # mejor costo => mayor aptitud
        probabilidades = aptitud / aptitud.sum()

        for _ in range(n_fuentes):
            i = rng.choice(n_fuentes, p=probabilidades)
            candidata = vecino(fuentes[i], rng)
            costo_candidata = distancia_ruta(candidata, distancias)

            if costo_candidata < costos[i]:
                fuentes[i] = candidata
                costos[i] = costo_candidata
                intentos[i] = 0
            else:
                intentos[i] += 1

        # -------------------------
        # 3) Abejas exploradoras
        # -------------------------
        for i in range(n_fuentes):
            if intentos[i] >= limite:
                fuentes[i] = rng.permutation(n_ciudades)
                costos[i] = distancia_ruta(fuentes[i], distancias)
                intentos[i] = 0

        idx_iter = np.argmin(costos)
        if costos[idx_iter] < mejor_costo:
            mejor_costo = costos[idx_iter]
            mejor_ruta = fuentes[idx_iter].copy()

        historial.append(mejor_costo)

        if (it + 1) % 50 == 0:
            print(f"Iteración {it + 1:3d} | Mejor distancia = {mejor_costo:.2f}")

    return mejor_ruta, mejor_costo, np.array(historial)


def cerrar_ruta(ruta):
    """Devuelve la ruta cerrada agregando el nodo inicial al final."""
    return np.append(ruta, ruta[0])


def construir_camino_nodos(ruta):
    """Construye el camino como lista de aristas (nodo_origen, nodo_destino)."""
    ruta_cerrada = cerrar_ruta(ruta)
    return [(int(a), int(b)) for a, b in zip(ruta_cerrada[:-1], ruta_cerrada[1:])]


def graficar_ruta(ciudades, ruta, archivo_salida="practica5/abc-viajero-ruta.png"):
    """Grafica nodos y camino de la mejor ruta TSP."""
    ruta_cerrada = cerrar_ruta(ruta)
    recorrido = ciudades[ruta_cerrada]

    plt.figure(figsize=(8, 6))
    plt.plot(
        recorrido[:, 0],
        recorrido[:, 1],
        "-o",
        color="tab:blue",
        linewidth=1.5,
        markersize=5,
    )

    for i, (x, y) in enumerate(ciudades):
        plt.text(x + 1.0, y + 1.0, str(i), fontsize=8)

    # Resaltar nodo de inicio/fin
    inicio = ruta[0]
    plt.scatter(
        ciudades[inicio, 0],
        ciudades[inicio, 1],
        color="red",
        s=70,
        zorder=3,
        label=f"Inicio/fin ({inicio})",
    )

    plt.title("ABC para TSP - Camino con nodos")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    salida = Path(archivo_salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(salida, dpi=150)
    plt.close()

    return str(salida)


if __name__ == "__main__":
    ciudades = generar_ciudades(n_ciudades=20, semilla=7)
    distancias = matriz_distancias(ciudades)

    mejor_ruta, mejor_distancia, historial = abc_tsp(
        distancias,
        n_fuentes=40,
        n_iteraciones=300,
        limite=35,
        semilla=42,
    )

    ruta_cerrada = cerrar_ruta(mejor_ruta)
    ruta_legible = " -> ".join(map(str, ruta_cerrada.tolist()))
    camino_nodos = construir_camino_nodos(mejor_ruta)
    archivo_grafica = graficar_ruta(ciudades, mejor_ruta)

    print("\nRESULTADO FINAL (ABC para TSP):")
    print(f"Mejor distancia encontrada: {mejor_distancia:.2f}")
    print(f"Ruta: {ruta_legible}")
    print(f"Camino (aristas nodo->nodo): {camino_nodos}")
    print(f"Historial (último valor): {historial[-1]:.2f}")
    print(f"Gráfica guardada en: {archivo_grafica}")
