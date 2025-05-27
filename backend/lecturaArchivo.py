from .models import Process, Resource, Action
from tkinter import ttk, filedialog, messagebox, scrolledtext

class FileLoader:
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