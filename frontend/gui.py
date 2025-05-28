import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from backend.models import Process, Resource, Action
from backend.algoritmosCalendarizacion import SchedulingAlgorithm
from backend.sincronizacionMecanismos import SynchronizationSimulator

class OSSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistemas Operativos")
        self.root.geometry("1200x800")
        
        # Almacenamiento de datos
        self.processes = []
        self.resources = []
        self.actions = []
        self.current_timeline = []
        self.simulation_running = False
        self.animation_speed = 100  # mmilisegundos
        
        # Colores para los procesos
        self.process_colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
            "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main para los tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # tab de calendarizacion 
        self.scheduling_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scheduling_frame, text="Simulación de Calendarización")
        self.setup_scheduling_tab()
        
        # Tab de sincronización
        self.sync_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sync_frame, text="Simulación de Sincronización")
        self.setup_synchronization_tab()
    
    def setup_scheduling_tab(self):
        # Controles para el panel izquierdo
        left_frame = ttk.Frame(self.scheduling_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Selecion del algoritmo. 
        ttk.Label(left_frame, text="Algoritmo de Calendarización:").pack(anchor=tk.W)
        self.algorithm_var = tk.StringVar(value="FIFO")
        algorithms = ["FIFO", "SJF", "SRT", "Round Robin", "Priority"]
        self.algorithm_combo = ttk.Combobox(left_frame, textvariable=self.algorithm_var, values=algorithms)
        self.algorithm_combo.pack(fill=tk.X, pady=5)
        self.algorithm_combo.bind("<<ComboboxSelected>>", self.on_algorithm_change)
        
        # Configuracion del quantum para Round Robin
        self.quantum_frame = ttk.Frame(left_frame)
        self.quantum_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.quantum_frame, text="Quantum:").pack(side=tk.LEFT)
        self.quantum_var = tk.IntVar(value=2)
        self.quantum_spin = tk.Spinbox(self.quantum_frame, from_=1, to=10, textvariable=self.quantum_var, width=5)
        self.quantum_spin.pack(side=tk.RIGHT)
        self.quantum_frame.pack_forget()  #Inicialmente oculto
        
        # Operaciones de archivo
        ttk.Label(left_frame, text="Cargar Procesos:").pack(anchor=tk.W, pady=(20, 0))
        ttk.Button(left_frame, text="Cargar desde archivo", command=self.load_processes_file).pack(fill=tk.X, pady=5)
        
        # Lista de procesos cargados
        ttk.Label(left_frame, text="Procesos cargados:").pack(anchor=tk.W, pady=(10, 0))
        self.process_listbox = tk.Listbox(left_frame, height=8)
        self.process_listbox.pack(fill=tk.X, pady=5)
        
        # Botones de control
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Ejecutar Simulación", command=self.run_scheduling_simulation).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_scheduling_data).pack(fill=tk.X, pady=2)
        
        # Métricas de eficiencia
        ttk.Label(left_frame, text="Métricas:").pack(anchor=tk.W, pady=(20, 0))
        self.metrics_text = scrolledtext.ScrolledText(left_frame, height=6, width=30)
        self.metrics_text.pack(fill=tk.X, pady=5)
        
        # Panel derecho - Visualización
        right_frame = ttk.Frame(self.scheduling_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Encabezado del timeline
        timeline_header = ttk.Frame(right_frame)
        timeline_header.pack(fill=tk.X, pady=5)
        ttk.Label(timeline_header, text="Diagrama de Gantt - Línea de Tiempo").pack(side=tk.LEFT)
        self.cycle_label = ttk.Label(timeline_header, text="Ciclo: 0")
        self.cycle_label.pack(side=tk.RIGHT)
        
        # Canvas para la línea de tiempo con scrollbar
        canvas_frame = ttk.Frame(right_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.timeline_canvas = tk.Canvas(canvas_frame, bg="white", height=300)
        self.timeline_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.timeline_canvas.xview)
        self.timeline_canvas.configure(xscrollcommand=self.timeline_scrollbar.set)
        
        self.timeline_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.timeline_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_synchronization_tab(self):
        # Controles para el panel izquierdo
        left_frame = ttk.Frame(self.sync_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Selección del mecanismo de sincronización
        ttk.Label(left_frame, text="Mecanismo de Sincronización:").pack(anchor=tk.W)
        self.sync_var = tk.StringVar(value="mutex")
        sync_mechanisms = ["mutex", "semaphore"]
        self.sync_combo = ttk.Combobox(left_frame, textvariable=self.sync_var, values=sync_mechanisms)
        self.sync_combo.pack(fill=tk.X, pady=5)
        
        # Operaciones de archivo para sincronización
        ttk.Label(left_frame, text="Cargar Archivos:").pack(anchor=tk.W, pady=(20, 0))
        ttk.Button(left_frame, text="Cargar Procesos", command=self.load_sync_processes_file).pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="Cargar Recursos", command=self.load_resources_file).pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="Cargar Acciones", command=self.load_actions_file).pack(fill=tk.X, pady=2)
        
        # Lista de procesos y recursos cargados
        ttk.Label(left_frame, text="Datos cargados:").pack(anchor=tk.W, pady=(10, 0))
        self.sync_data_text = scrolledtext.ScrolledText(left_frame, height=12, width=30)
        self.sync_data_text.pack(fill=tk.X, pady=5)
        
        # Botones de control para sincronización
        sync_button_frame = ttk.Frame(left_frame)
        sync_button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(sync_button_frame, text="Ejecutar Simulación", command=self.run_sync_simulation).pack(fill=tk.X, pady=2)
        ttk.Button(sync_button_frame, text="Limpiar", command=self.clear_sync_data).pack(fill=tk.X, pady=2)
        
        # Panel derecho - Visualización de sincronización
        right_frame = ttk.Frame(self.sync_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Encabezado del timeline de sincronización
        sync_timeline_header = ttk.Frame(right_frame)
        sync_timeline_header.pack(fill=tk.X, pady=5)
        ttk.Label(sync_timeline_header, text="Línea de Tiempo - Sincronización").pack(side=tk.LEFT)
        self.sync_cycle_label = ttk.Label(sync_timeline_header, text="Ciclo: 0")
        self.sync_cycle_label.pack(side=tk.RIGHT)
        
        # Canvas para la línea de tiempo de sincronización con scrollbar
        sync_canvas_frame = ttk.Frame(right_frame)
        sync_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.sync_timeline_canvas = tk.Canvas(sync_canvas_frame, bg="white", height=300)
        self.sync_timeline_scrollbar = ttk.Scrollbar(sync_canvas_frame, orient=tk.HORIZONTAL, command=self.sync_timeline_canvas.xview)
        self.sync_timeline_canvas.configure(xscrollcommand=self.sync_timeline_scrollbar.set)
        
        self.sync_timeline_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.sync_timeline_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def on_algorithm_change(self, event=None):
        if self.algorithm_var.get() == "Round Robin":
            self.quantum_frame.pack(fill=tk.X, pady=5)
        else:
            self.quantum_frame.pack_forget()
    
    def load_processes_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de procesos",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.processes = []
                with open(filename, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = [p.strip() for p in line.split(',')]
                            if len(parts) >= 4:
                                pid, bt, at, priority = parts[0], int(parts[1]), int(parts[2]), int(parts[3])
                                self.processes.append(Process(pid, bt, at, priority))
                
                self.update_process_listbox()
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.processes)} procesos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo: {str(e)}")
    
    def load_sync_processes_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de procesos para sincronización",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.processes = []
                with open(filename, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = [p.strip() for p in line.split(',')]
                            if len(parts) >= 4:
                                pid, bt, at, priority = parts[0], int(parts[1]), int(parts[2]), int(parts[3])
                                self.processes.append(Process(pid, bt, at, priority))
                
                self.update_sync_data_display()
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.processes)} procesos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo: {str(e)}")
    
    def load_resources_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de recursos",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.resources = []
                with open(filename, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = [p.strip() for p in line.split(',')]
                            if len(parts) >= 2:
                                name, counter = parts[0], int(parts[1])
                                self.resources.append(Resource(name, counter))
                
                self.update_sync_data_display()
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.resources)} recursos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo: {str(e)}")
    
    def load_actions_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de acciones",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.actions = []
                with open(filename, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = [p.strip() for p in line.split(',')]
                            if len(parts) >= 4:
                                pid, action, resource, cycle = parts[0], parts[1], parts[2], int(parts[3])
                                self.actions.append(Action(pid, action, resource, cycle))
                
                self.update_sync_data_display()
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.actions)} acciones")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo: {str(e)}")
    
    def update_process_listbox(self):
        self.process_listbox.delete(0, tk.END)
        for process in self.processes:
            self.process_listbox.insert(tk.END, f"{process.pid}: BT={process.burst_time}, AT={process.arrival_time}, P={process.priority}")
    
    def update_sync_data_display(self):
        self.sync_data_text.delete(1.0, tk.END)
        
        if self.processes:
            self.sync_data_text.insert(tk.END, "PROCESOS:\n")
            for p in self.processes:
                self.sync_data_text.insert(tk.END, f"  {p.pid}: BT={p.burst_time}, AT={p.arrival_time}, P={p.priority}\n")
            self.sync_data_text.insert(tk.END, "\n")
        
        if self.resources:
            self.sync_data_text.insert(tk.END, "RECURSOS:\n")
            for r in self.resources:
                self.sync_data_text.insert(tk.END, f"  {r.name}: Count={r.counter}\n")
            self.sync_data_text.insert(tk.END, "\n")
        
        if self.actions:
            self.sync_data_text.insert(tk.END, "ACCIONES:\n")
            for a in self.actions:
                self.sync_data_text.insert(tk.END, f"  {a.pid} {a.action_type} {a.resource} @ Ciclo {a.cycle}\n")
    
    def run_scheduling_simulation(self):
        if not self.processes:
            messagebox.showwarning("Advertencia", "Debe cargar procesos primero")
            return
        
        if self.simulation_running:
            return
        
        algorithm = self.algorithm_var.get()
        
        try:
            if algorithm == "FIFO":
                timeline = SchedulingAlgorithm.fifo(self.processes)
            elif algorithm == "SJF":
                timeline = SchedulingAlgorithm.sjf(self.processes)
            elif algorithm == "SRT":
                timeline = SchedulingAlgorithm.srt(self.processes)
            elif algorithm == "Round Robin":
                quantum = self.quantum_var.get()
                timeline = SchedulingAlgorithm.round_robin(self.processes, quantum)
            elif algorithm == "Priority":
                timeline = SchedulingAlgorithm.priority_scheduling(self.processes)
            else:
                messagebox.showerror("Error", "Algoritmo no implementado")
                return
            
            self.current_timeline = timeline
            self.animate_scheduling_timeline()
            self.calculate_and_display_metrics()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en simulación: {str(e)}")
    
    def animate_scheduling_timeline(self):
        self.simulation_running = True
        self.timeline_canvas.delete("all")
        
        # Dibujo de la base del timeline
        canvas_width = 1000
        canvas_height = 300
        self.timeline_canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))
        
        # Mapeo de colores para los procesos
        process_color_map = {}
        for i, process in enumerate(self.processes):
            process_color_map[process.pid] = self.process_colors[i % len(self.process_colors)]
        
        # Animacion
        y_start = 50
        block_height = 40
        scale = 20  # pixels por ciclo
        
        def draw_step(step_index):
            if step_index >= len(self.current_timeline):
                self.simulation_running = False
                return
            
            pid, start_time, duration = self.current_timeline[step_index]
            color = process_color_map[pid]
            
            x1 = start_time * scale + 50
            x2 = (start_time + duration) * scale + 50
            y1 = y_start
            y2 = y_start + block_height
            
            # Dibujar bloque de acción
            self.timeline_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)
            self.timeline_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=pid, font=("Arial", 10, "bold"))
            
            # Actualizar contador de ciclos
            current_cycle = start_time + duration
            self.cycle_label.config(text=f"Ciclo: {current_cycle}")
            
            # Desplazar el canvas para mostrar la animación
            self.timeline_canvas.xview_moveto((x2 - 200) / canvas_width)
            
            # Programar el siguiente paso de la animación
            self.root.after(self.animation_speed, lambda: draw_step(step_index + 1))
        
        # Dibujar etiquetas de procesos
        max_time = max(start + duration for _, start, duration in self.current_timeline) if self.current_timeline else 0
        for i in range(0, max_time + 1, 5):
            x = i * scale + 50
            self.timeline_canvas.create_line(x, y_start + block_height, x, y_start + block_height + 10, fill="black")
            self.timeline_canvas.create_text(x, y_start + block_height + 20, text=str(i), font=("Arial", 8))
        
        # Inicializar la animación
        draw_step(0)
    
    def calculate_and_display_metrics(self):
        if not self.processes:
            return
        
        total_waiting_time = sum(p.waiting_time for p in self.processes)
        total_turnaround_time = sum(p.turnaround_time for p in self.processes)
        avg_waiting_time = total_waiting_time / len(self.processes)
        avg_turnaround_time = total_turnaround_time / len(self.processes)
        
        metrics_text = f"MÉTRICAS DE EFICIENCIA\n"
        metrics_text += f"{'='*30}\n\n"
        metrics_text += f"Tiempo de espera promedio: {avg_waiting_time:.2f}\n"
        metrics_text += f"Tiempo de retorno promedio: {avg_turnaround_time:.2f}\n\n"
        metrics_text += f"DETALLE POR PROCESO:\n"
        metrics_text += f"{'-'*30}\n"
        
        for process in self.processes:
            metrics_text += f"{process.pid}:\n"
            metrics_text += f"  Espera: {process.waiting_time}\n"
            metrics_text += f"  Retorno: {process.turnaround_time}\n"
            metrics_text += f"  Inicio: {process.start_time}\n"
            metrics_text += f"  Fin: {process.completion_time}\n\n"
        
        self.metrics_text.delete(1.0, tk.END)
        self.metrics_text.insert(1.0, metrics_text)
    
    def run_sync_simulation(self):
        if not self.processes or not self.resources or not self.actions:
            messagebox.showwarning("Advertencia", "Debe cargar procesos, recursos y acciones")
            return
        
        if self.simulation_running:
            return
        
        sync_type = self.sync_var.get()
        
        try:
            simulator = SynchronizationSimulator(self.processes, self.resources, self.actions, sync_type)
            timeline = simulator.simulate()
            self.current_timeline = timeline
            self.animate_sync_timeline()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en simulación: {str(e)}")
    
    def animate_sync_timeline(self):
        self.simulation_running = True
        self.sync_timeline_canvas.delete("all")
        
        # Dibujo de la base del timeline
        canvas_width = 1000
        canvas_height = 400
        self.sync_timeline_canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))
        
        # Mapeo de colores para los procesos
        process_color_map = {}
        unique_pids = list(set(item[0] for item in self.current_timeline))
        for i, pid in enumerate(unique_pids):
            process_color_map[pid] = self.process_colors[i % len(self.process_colors)]
        
        # Determinar filas para cada proceso
        process_rows = {}
        row_height = 60
        y_start = 50
        
        for i, pid in enumerate(unique_pids):
            process_rows[pid] = y_start + i * row_height
        
        # Animación
        scale = 30  # pixels por ciclo
        
        def draw_step(step_index):
            if step_index >= len(self.current_timeline):
                self.simulation_running = False
                return
            
            pid, cycle, action, state = self.current_timeline[step_index]
            color = process_color_map[pid]
            
            # Determinar colores y estilos según el estado
            if state == "ACCESSED":
                fill_color = color
                outline_color = "green"
                outline_width = 3
            else:  # Esperando
                fill_color = "lightgray"
                outline_color = "red"
                outline_width = 3
            
            x1 = cycle * scale + 50
            x2 = (cycle + 1) * scale + 50
            y1 = process_rows[pid]
            y2 = y1 + 40
            
            # Dibujar bloque de acción
            self.sync_timeline_canvas.create_rectangle(x1, y1, x2, y2, 
                                                    fill=fill_color, 
                                                    outline=outline_color, 
                                                    width=outline_width)
            
            # Agregar texto al bloque
            text = f"{pid}\n{action}\n{state}"
            self.sync_timeline_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, 
                                                text=text, font=("Arial", 8, "bold"))
            
            # Actualizar contador de ciclos
            self.sync_cycle_label.config(text=f"Ciclo: {cycle}")
            
            # Desplazar el canvas para mostrar la animación
            self.sync_timeline_canvas.xview_moveto((x2 - 200) / canvas_width)
            
            # Programar el siguiente paso de la animación
            self.root.after(self.animation_speed * 2, lambda: draw_step(step_index + 1))
        
        # Dibujar etiquetas de procesos
        for pid, y_pos in process_rows.items():
            self.sync_timeline_canvas.create_text(25, y_pos + 20, text=pid, 
                                                font=("Arial", 10, "bold"), anchor="center")
        
        # Dibujar líneas de tiempo
        max_cycle = max(cycle for _, cycle, _, _ in self.current_timeline) if self.current_timeline else 0
        for i in range(0, max_cycle + 2):
            x = i * scale + 50
            y_bottom = y_start + len(unique_pids) * row_height
            self.sync_timeline_canvas.create_line(x, y_bottom, x, y_bottom + 10, fill="black")
            self.sync_timeline_canvas.create_text(x, y_bottom + 20, text=str(i), font=("Arial", 8))
        
        # Dibujar leyenda
        legend_y = y_start + len(unique_pids) * row_height + 40
        self.sync_timeline_canvas.create_text(50, legend_y, text="Leyenda:", font=("Arial", 10, "bold"), anchor="w")
        self.sync_timeline_canvas.create_rectangle(50, legend_y + 15, 70, legend_y + 35, fill="lightblue", outline="green", width=3)
        self.sync_timeline_canvas.create_text(80, legend_y + 25, text="ACCESSED", font=("Arial", 9), anchor="w")
        self.sync_timeline_canvas.create_rectangle(180, legend_y + 15, 200, legend_y + 35, fill="lightgray", outline="red", width=3)
        self.sync_timeline_canvas.create_text(210, legend_y + 25, text="WAITING", font=("Arial", 9), anchor="w")
        
        # Iniciar la animación
        if self.current_timeline:
            draw_step(0)
    
    def clear_scheduling_data(self):
        self.processes = []
        self.current_timeline = []
        self.process_listbox.delete(0, tk.END)
        self.metrics_text.delete(1.0, tk.END)
        self.timeline_canvas.delete("all")
        self.cycle_label.config(text="Ciclo: 0")
        self.simulation_running = False
    
    def clear_sync_data(self):
        self.processes = []
        self.resources = []
        self.actions = []
        self.current_timeline = []
        self.sync_data_text.delete(1.0, tk.END)
        self.sync_timeline_canvas.delete("all")
        self.sync_cycle_label.config(text="Ciclo: 0")
        self.simulation_running = False