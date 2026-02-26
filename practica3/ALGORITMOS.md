# Pseudocódigo y Diagramas de Flujo - Temple Simulado

Este documento detalla la lógica de las dos versiones del algoritmo de Temple Simulado (Simulated Annealing) implementadas en esta práctica.

---

## 1. Temple Simulado Estándar
Sigue una trayectoria continua y utiliza el criterio de Metrópolis.

### Pseudocódigo
```text
Algoritmo Temple_Simulado_Estandar
    // Inicialización
    S_actual = Generar_Solucion_Aleatoria()
    T = T_inicial
    S_mejor = S_actual
    
    Mientras T > T_final Y iteración < Max_Iteraciones Hacer:
        // Generar un vecino cercano (Búsqueda Local)
        S_vecino = Generar_Vecino(S_actual)
        
        Delta_E = Energia(S_vecino) - Energia(S_actual)
        
        // Criterio de Aceptación (Metrópolis)
        Si Delta_E < 0 Entonces:
            S_actual = S_vecino
        Sino:
            Probabilidad = exp(-Delta_E / T)
            Si Aleatorio(0, 1) < Probabilidad Entonces:
                S_actual = S_vecino
        FinSi
        
        // Actualizar mejor solución global
        Si Energia(S_actual) < Energia(S_mejor) Entonces:
            S_mejor = S_actual
        FinSi
        
        // Enfriamiento Geométrico
        T = T * Factor_Enfriamiento
        iteración = iteración + 1
    FinMientras
    
    Retornar S_mejor
FinAlgoritmo
```

### Diagrama de Flujo
```mermaid
graph TD
    A([Inicio]) --> B[Inicializar S_actual, T, S_mejor]
    B --> C{¿Iteración < Max?}
    C -- No --> Z([Fin: Retornar S_mejor])
    C -- Sí --> D[Generar S_vecino cercano]
    D --> E{¿Aceptar S_vecino? <br/>Criterio Metrópolis}
    E -- Sí --> F[S_actual = S_vecino]
    E -- No --> G{¿S_actual mejor que S_mejor?}
    F --> G
    G -- Sí --> H[S_mejor = S_actual]
    G -- No --> I[T = T * Factor_Enfriamiento]
    H --> I
    I --> C
```

---

## 2. Temple Simulado Híbrido (Clase)
Incluye detección de estancamiento, saltos aleatorios y recalentamiento.

### Pseudocódigo
```text
Algoritmo Temple_Simulado_Hibrido
    // Inicialización
    S_actual = Generar_Solucion_Aleatoria()
    T = T_inicial
    S_mejor = S_actual
    no_improve_count = 0
    
    Mientras T > T_final Y iteración < Max_Iteraciones Hacer:
        S_vecino = Generar_Vecino(S_actual)
        Delta_E = Energia(S_vecino) - Energia(S_actual)
        
        // Intento de movimiento
        Si Criterio_Metropolis(Delta_E, T) es Aceptado Entonces:
            S_actual = S_vecino
        FinSi
        
        // Gestión de Mejora y Estancamiento
        Si Energia(S_actual) < Energia(S_mejor) Entonces:
            S_mejor = S_actual
            no_improve_count = 0  // Reiniciar contador
        Sino:
            no_improve_count = no_improve_count + 1
        FinSi
        
        // Salto Aleatorio por Estancamiento
        Si no_improve_count >= Max_No_Mejora Entonces:
            S_actual = Generar_Solucion_Aleatoria()  // Reinicio en otro punto
            T = T * 1.05                             // Recalentamiento leve
            no_improve_count = 0
        FinSi
        
        T = T * Factor_Enfriamiento
        iteración = iteración + 1
    FinMientras
    
    Retornar S_mejor
FinAlgoritmo
```

### Diagrama de Flujo
```mermaid
graph TD
    A([Inicio]) --> B[Inicializar S_actual, T, S_mejor, <br/>no_improve_count = 0]
    B --> C{¿Iteración < Max?}
    
    C -- No --> Z([Fin: Retornar S_mejor])
    C -- Sí --> D[Generar S_vecino cercano]
    
    D --> E{¿Aceptar S_vecino? <br/>Criterio Metrópolis}
    
    E -- Sí --> F[S_actual = S_vecino]
    E -- No --> G{¿S_actual mejor que S_mejor?}
    
    F --> G
    
    G -- Sí --> H[S_mejor = S_actual <br/>no_improve_count = 0]
    G -- No --> I[no_improve_count += 1]
    
    H --> J{¿no_improve_count >= <br/>max_no_improve?}
    I --> J
    
    J -- Sí --> K[<b>SALTO ALEATORIO</b><br/>S_actual = Nueva Posición Aleatoria<br/>no_improve_count = 0<br/>T = T * 1.05 recalentamiento]
    J -- No --> L[T = T * cooling_rate <br/>enfriamiento]
    
    K --> L
    L --> C
```
