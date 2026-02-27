import numpy as np
import matplotlib.pyplot as plt

def funcion_objetivo(x):
    """
    Función objetivo: f(x) = x^2 - 5x + 10
    """
    return x**2 - 5*x + 10

def gradiente(x):
    """
    Derivada de f(x): f'(x) = 2x - 5
    """
    return 2*x - 5

def gradiente_descendente(punto_inicial, tasa_aprendizaje, iteraciones):
    """
    Algoritmo de Gradiente Descendente para una dimensión.
    """
    historial_puntos = [punto_inicial]
    punto_actual = punto_inicial
    
    print(f"Iniciando Gradiente Descendente en x = {punto_inicial}")
    
    for i in range(iteraciones):
        # Calcular el gradiente en el punto actual
        grad = gradiente(punto_actual)
        
        # Actualizar el punto: x = x - lr * gradiente
        punto_actual = punto_actual - tasa_aprendizaje * grad
        
        historial_puntos.append(punto_actual)
        
        if (i + 1) % 5 == 0:
            valor = funcion_objetivo(punto_actual)
            print(f"Iteración {i+1}: x = {punto_actual:.4f}, f(x) = {valor:.6f}")
            
    return np.array(historial_puntos)

# Configuración del algoritmo
punto_inicio = 0.0  # Empezamos desde x = 0
tasa_aprendizaje = 0.1
num_iteraciones = 40

# Ejecución
trayectoria = gradiente_descendente(punto_inicio, tasa_aprendizaje, num_iteraciones)

# Visualización en 2D (x vs f(x))
x_vals = np.linspace(-2, 7, 400)
y_vals = funcion_objetivo(x_vals)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label='f(x) = x² - 5x + 10', color='blue', alpha=0.6)
plt.plot(trayectoria, funcion_objetivo(trayectoria), 'ro-', markersize=5, label='Trayectoria del Gradiente')

# Marcar el mínimo real (f'(x)=0 -> 2x - 5 = 0 -> x = 2.5)
plt.plot(2.5, funcion_objetivo(2.5), 'g*', markersize=15, label='Mínimo Real (2.5, 3.75)')

plt.title(f'Gradiente Descendente: f(x) = x² - 5x + 10 (lr={tasa_aprendizaje})')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)

plt.savefig('trayectoria_gradiente.png')
print("\nGráfica guardada como 'trayectoria_gradiente.png'")
