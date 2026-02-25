import numpy as np
import math
import random
import matplotlib.pyplot as plt

# ---------------------
# Definición de funciones
# ---------------------

# Función peaks
def peaks(x, y):
    return  3*(1 - x)**2 * np.exp(-(x**2) - (y + 1)**2) \
          - 10*(x/5 - x**3 - y**5) * np.exp(-x**2 - y**2) \
          - (1/3)*np.exp(-(x + 1)**2 - y**2)

# Función objetivo (minimizamos peaks)
def objective_function(position):
    x, y = position
    return peaks(x, y)

# Límites del espacio de búsqueda
lower_bound = np.array([-3, -3])
upper_bound = np.array([3, 3])

# Generar vecino dentro de los límites (Búsqueda Local)
def neighbor(position, step_size=0.1):
    new_position = position + np.random.uniform(-step_size, step_size, size=2)
    return np.clip(new_position, lower_bound, upper_bound)

# Probabilidad de aceptación (Criterio de Metrópolis)
def acceptance_probability(current_energy, neighbor_energy, temperature):
    if neighbor_energy < current_energy:
        return 1.0
    # Evitar división por cero si la temperatura es muy baja
    if temperature <= 0:
        return 0.0
    return math.exp((current_energy - neighbor_energy) / temperature)

# Simulated Annealing ESTÁNDAR
def simulated_annealing(initial_solution, initial_temperature,
                        cooling_rate, max_iterations):
    
    current_solution = initial_solution
    current_energy = objective_function(current_solution)
    
    best_solution = current_solution
    best_energy = current_energy

    temperature = initial_temperature
    path = [current_solution.copy()]

    for iteration in range(max_iterations):
        # 1. Generar un vecino cercano
        new_solution = neighbor(current_solution)
        new_energy = objective_function(new_solution)

        # 2. Decidir si aceptamos el movimiento
        if acceptance_probability(current_energy, new_energy, temperature) > random.random():
            current_solution = new_solution
            current_energy = new_energy
            path.append(current_solution.copy())

        # 3. Actualizar la mejor solución encontrada hasta ahora
        if current_energy < best_energy:
            best_solution = current_solution
            best_energy = current_energy

        # 4. Enfriamiento (Esquema geométrico estándar)
        temperature *= cooling_rate

    return best_solution, best_energy, path

# ---------------------
# Parámetros (Iguales a la versión de clase para comparar)
# ---------------------

initial_solution = np.random.uniform(lower_bound, upper_bound)
initial_temperature = 1000
cooling_rate = 0.95
max_iterations = 10000

# Ejecutar algoritmo
best_solution, best_energy, path = simulated_annealing(
    initial_solution,
    initial_temperature,
    cooling_rate,
    max_iterations
)

# ---------------------
# Visualización
# ---------------------

x = np.linspace(lower_bound[0], upper_bound[0], 300)
y = np.linspace(lower_bound[1], upper_bound[1], 300)
X, Y = np.meshgrid(x, y)
Z = peaks(X, Y)

path = np.array(path)
px, py = path[:, 0], path[:, 1]

plt.figure(figsize=(10, 8))
contour = plt.contourf(X, Y, Z, levels=50, cmap='viridis')
plt.colorbar(label='f(x, y)')

# Trayectoria (Sin saltos bruscos)
plt.plot(px, py, color='white', linestyle='-', linewidth=0.5, alpha=0.7, label='Trayectoria')

# Punto inicial
plt.plot(px[0], py[0], 'o', color='blue', label='Inicio')

# Mejor solución encontrada
plt.plot(best_solution[0], best_solution[1], 'o', color='red', markersize=12, label='Mejor solución')

plt.title("Simulated Annealing Estándar (Función Peaks)")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.xlim(lower_bound[0], upper_bound[0])
plt.ylim(lower_bound[1], upper_bound[1])
plt.show()

# ---------------------
# Resultado final
# ---------------------
print("\nRESULTADO FINAL (VERSIÓN ESTÁNDAR):")
print(f"Mejor solución encontrada: x = {best_solution[0]:.5f}, y = {best_solution[1]:.5f}")
print(f"Valor mínimo de f(x, y) = {best_energy:.5f}")
