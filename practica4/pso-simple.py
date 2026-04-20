import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------
# 1) Función objetivo (a minimizar)
# ---------------------------------
def objective_function(position):
    """
    Función Sphere en 2D: f(x, y) = x^2 + y^2
    Mínimo global en (0, 0), f=0
    """
    return np.sum(position**2)


# ---------------------------------
# 2) PSO simple (versión canónica)
# ---------------------------------
def pso_simple(
    n_particles=30,
    n_dimensions=2,
    n_iterations=100,
    bounds=(-5.0, 5.0),
    w=0.7,
    c1=1.5,
    c2=1.5,
    seed=42,
):
    np.random.seed(seed)

    lower, upper = bounds

    # Inicialización de posiciones y velocidades
    positions = np.random.uniform(lower, upper, size=(n_particles, n_dimensions))
    velocities = np.random.uniform(-1, 1, size=(n_particles, n_dimensions))

    # Mejor posición personal (pbest)
    pbest_positions = positions.copy()
    pbest_values = np.array([objective_function(p) for p in positions])

    # Mejor posición global (gbest)
    gbest_index = np.argmin(pbest_values)
    gbest_position = pbest_positions[gbest_index].copy()
    gbest_value = pbest_values[gbest_index]

    # Historial para visualización
    gbest_history = [gbest_value]
    trajectory_particle_0 = [positions[0].copy()]

    for iteration in range(n_iterations):
        for i in range(n_particles):
            r1 = np.random.rand(n_dimensions)
            r2 = np.random.rand(n_dimensions)

            # Ecuación de velocidad
            velocities[i] = (
                w * velocities[i]
                + c1 * r1 * (pbest_positions[i] - positions[i])
                + c2 * r2 * (gbest_position - positions[i])
            )

            # Ecuación de posición
            positions[i] = positions[i] + velocities[i]
            positions[i] = np.clip(positions[i], lower, upper)

            # Evaluar y actualizar pbest
            value = objective_function(positions[i])
            if value < pbest_values[i]:
                pbest_values[i] = value
                pbest_positions[i] = positions[i].copy()

                # Si mejora personal también mejora global
                if value < gbest_value:
                    gbest_value = value
                    gbest_position = positions[i].copy()

        gbest_history.append(gbest_value)
        trajectory_particle_0.append(positions[0].copy())

        if (iteration + 1) % 20 == 0:
            print(
                f"Iteración {iteration + 1:3d} | "
                f"Mejor valor global = {gbest_value:.8f} | "
                f"gbest = {gbest_position}"
            )

    return (
        gbest_position,
        gbest_value,
        np.array(gbest_history),
        np.array(trajectory_particle_0),
    )


# ---------------------------------
# 3) Ejecución
# ---------------------------------
best_pos, best_val, history, trajectory = pso_simple()

print("\nRESULTADO FINAL (PSO SIMPLE):")
print(f"Mejor posición encontrada: {best_pos}")
print(f"Mejor valor encontrado: {best_val:.10f}")


# ---------------------------------
# 4) Visualización
# ---------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Gráfica de convergencia
axes[0].plot(history, color="tab:blue")
axes[0].set_title("Convergencia PSO (gbest)")
axes[0].set_xlabel("Iteración")
axes[0].set_ylabel("f(gbest)")
axes[0].grid(True, alpha=0.3)

# Trayectoria de una partícula
axes[1].plot(
    trajectory[:, 0],
    trajectory[:, 1],
    "o-",
    markersize=3,
    color="tab:orange",
    alpha=0.8,
)
axes[1].plot(0, 0, "r*", markersize=12, label="Óptimo real (0,0)")
axes[1].set_title("Trayectoria de la partícula 0")
axes[1].set_xlabel("x")
axes[1].set_ylabel("y")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("practica 4/pso-simple.png")
print("Gráfica guardada en: practica 4/pso-simple.png")
