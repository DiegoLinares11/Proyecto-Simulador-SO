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
        
        # Data storage
        self.processes = []
        self.resources = []
        self.actions = []
        self.current_timeline = []
        self.simulation_running = False
        self.animation_speed = 100  # milliseconds
        
        # Color scheme for processes
        self.process_colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
            "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        return None

    
    