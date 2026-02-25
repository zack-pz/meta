import numpy as np
import matplotlib.pyplot as plt

def funcion_objetivo(x, y):
    """
    Función cuadrática simple: f(x, y) = x^2 + y^2
    El mínimo global está en (0, 0).
    """
    return x**2 + y**2

def gradiente(x, y):
    """
    Cálculo manual del gradiente de f(x, y) = x^2 + y^2
    df/dx = 2x
    df/dy = 2y
    """
    return np.array([2*x, 2*y])

def gradiente_descendente(punto_inicial, tasa_aprendizaje, iteraciones):
    """
    Implementación del algoritmo de Gradiente Descendente.
    """
    historial_puntos = [punto_inicial]
    punto_actual = np.array(punto_inicial)
    
    print(f"Iniciando Gradiente Descendente en {punto_inicial}")
    
    for i in range(iteraciones):
        # Calcular el gradiente en el punto actual
        grad = gradiente(punto_actual[0], punto_actual[1])
        
        # Actualizar el punto: x = x - lr * gradiente
        punto_actual = punto_actual - tasa_aprendizaje * grad
        
        historial_puntos.append(punto_actual)
        
        if (i + 1) % 10 == 0:
            error = funcion_objetivo(punto_actual[0], punto_actual[1])
            print(f"Iteración {i+1}: Punto {punto_actual}, Valor f(x,y): {error:.6f}")
            
    return np.array(historial_puntos)

# Configuración del algoritmo
punto_inicio = [4.0, 4.0]
tasa_aprendizaje = 0.1
num_iteraciones = 50

# Ejecución
trayectoria = gradiente_descendente(punto_inicio, tasa_aprendizaje, num_iteraciones)

# Visualización
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = funcion_objetivo(X, Y)

plt.figure(figsize=(10, 8))
plt.contour(X, Y, Z, levels=20, cmap='viridis')
plt.plot(trayectoria[:, 0], trayectoria[:, 1], 'ro-', markersize=3, label='Trayectoria del Gradiente')
plt.plot(0, 0, 'b*', markersize=15, label='Mínimo Real (0,0)')
plt.title(f'Gradiente Descendente (lr={tasa_aprendizaje})')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
#plt.show()
plt.savefig('trayectoria_gradiente.png')
print("Gráfica guardada como 'trayectoria_gradiente.png'")