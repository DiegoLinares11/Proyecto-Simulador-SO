# Proyecto-Simulador-SO
# Proyecto-Simulador-SO
# Simulador de Planificación y Sincronización

Este proyecto implementa un **simulador interactivo con interfaz gráfica en Python** que permite visualizar la ejecución de diferentes **algoritmos de planificación de procesos** y **mecanismos de sincronización**, simulando el comportamiento de un sistema operativo en un entorno educativo.

## Funcionalidades principales

### 1. Algoritmos de planificación soportados

- **FIFO (First In, First Out)**  
- **SJF (Shortest Job First)**  
- **SRT (Shortest Remaining Time)**  
- **Round Robin (con quantum configurable)**  
- **Priority Scheduling (No-preemptivo)**

Cada algoritmo calcula:
- Tiempo de inicio, finalización, espera y retorno.
- Línea de tiempo de ejecución para representar el diagrama de Gantt.

### 2. Mecanismos de sincronización soportados

- **Mutex**
- **Semáforo (con contador)**

Cada recurso puede tener:
- Una cola de espera.
- Control de acceso a procesos.
- Soporte para múltiples intentos de adquisición por parte de procesos.

### 3. Entrada por archivo `.txt`

El simulador permite cargar archivos de entrada con datos como:
- Lista de procesos (PID, tiempo de llegada, duración, prioridad).
- Recursos definidos (mutex/semaforo).
- Acciones secuenciales de cada proceso: `wait`, `signal`, `compute`.

Ejemplo de entrada:


```bash
resources:
mutex R1
semaphore R2 2

processes:
P1 0 5 1
P2 2 4 2

actions:
P1 wait R1
P1 compute 3
P1 signal R1
P2 wait R1
P2 compute 2
P2 signal R1
```

### 4. Interfaz gráfica (Tkinter)

- Menús para cargar archivos, seleccionar algoritmo y modo de simulación.
- Visualización animada paso a paso o ejecución completa.
- Visualización tipo Gantt del planificador.
- Estados de procesos, recursos y métricas al finalizar.

---

## Estructura del proyecto

```bash
├── main.py # Lanzador principal de la interfaz
├── AlgoritmosCalendarizacion/
│ ├── process.py # Clase Process (PID, tiempos, prioridad, etc.)
│ ├── resource.py # Clase Resource para mutex y semáforos
│ ├── action.py # Clase Action (wait, signal, compute)
├── scheduling/
│ └── scheduling_algorithms.py # Implementación de FIFO, SJF, etc.
│ └── synchronization_simulator.py # Lógica de ejecución de sincronización
├── frontend/
│ └── gui.py # Interfaz gráfica (Tkinter)
├── assets/ # Íconos, temas, colores, etc.
├── README.md
```


---

##  Cómo ejecutar

### Requisitos

- Python 3.10 o superior
- Tkinter (incluido por defecto en Python)
- No requiere instalación de librerías externas

### Ejecución

```bash
python main.py
```

Objetivo educativo

Este simulador fue desarrollado como parte de un laboratorio universitario para comprender de forma visual e interactiva:

    Los distintos tipos de planificación de procesos.

    La competencia por recursos compartidos usando sincronización.

    El impacto de distintas políticas en la eficiencia del sistema.

    
