import threading
from typing import List, Tuple
from .models import Process, Resource, Action

class SynchronizationSimulator:
    def __init__(self, processes: List[Process], resources: List[Resource], actions: List[Action], sync_type: str):
        self.processes = {p.pid: p for p in processes}
        self.resources = {r.name: r for r in resources}
        self.actions = sorted(actions, key=lambda a: a.cycle)
        self.sync_type = sync_type
        self.timeline = []
        self.current_cycle = 0
        
    def simulate(self) -> List[Tuple[str, int, str, str]]:  # (pid, ciclo, accion, Estado)
        """Simulate synchronization mechanism"""
        waiting_processes = {}  # pid -> (accion, recurso, ciclo)
        
        for action in self.actions:
            self.current_cycle = action.cycle
            resource = self.resources[action.resource]
            
            if action.pid in waiting_processes:
                # Proceso esperando por un recurso
                continue
            
            if self.sync_type == "mutex":
                if resource.counter > 0:
                    # Recurso disponible
                    resource.counter -= 1
                    self.timeline.append((action.pid, action.cycle, action.action_type, "ACCESSED"))
                    # Liberar el recurso después de usarlo (simplificado)
                    resource.counter += 1
                else:
                    # Recurso ocupado, el proceso debe esperar
                    self.timeline.append((action.pid, action.cycle, action.action_type, "WAITING"))
                    waiting_processes[action.pid] = (action.action_type, action.resource, action.cycle)
            
            elif self.sync_type == "semaphore":
                if resource.counter > 0:
                    # Recurso disponible
                    resource.counter -= 1
                    self.timeline.append((action.pid, action.cycle, action.action_type, "ACCESSED"))
                    # Recurso se libera después de usarlo
                    resource.counter += 1
                else:
                    # Todos los recursos ocupados, el proceso debe esperar
                    self.timeline.append((action.pid, action.cycle, action.action_type, "WAITING"))
                    waiting_processes[action.pid] = (action.action_type, action.resource, action.cycle)
        
        return self.timeline