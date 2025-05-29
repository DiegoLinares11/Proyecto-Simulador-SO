from collections import defaultdict, deque
from typing import List, Tuple
from .models import Process, Resource, Action

class SynchronizationSimulator:
    def __init__(self, processes: List[Process], resources: List[Resource], actions: List[Action], sync_type: str):
        self.processes = {p.pid: p for p in processes}
        self.resources = {r.name: r for r in resources}  # Diccionario por nombre
        self.actions = actions
        self.sync_type = sync_type
        self.timeline = []
        
    def simulate(self) -> List[Tuple[str, int, str, str]]:
        """Versión corregida con gestión adecuada de tiempos y recursos"""
        # 1. Estructuras mejoradas
        max_cycle = max(action.cycle for action in self.actions) + 50
        actions_by_cycle = defaultdict(list)
        for action in self.actions:
            actions_by_cycle[action.cycle].append(action)
        
        # CORRECCIÓN: Usar nombres de recursos como claves
        waiting_queues = {res_name: deque() for res_name in self.resources.keys()}
        resource_holders = {res_name: {"pids": [], "durations": {}} for res_name in self.resources.keys()}
        action_durations = {"READ": 2, "WRITE": 3}
        
        # 2. Simulación por ciclo
        for cycle in range(max_cycle):
            # A. Actualizar recursos en uso
            for res_name, res_data in resource_holders.items():
                completed = []
                for pid in res_data["pids"]:
                    res_data["durations"][pid] -= 1
                    if res_data["durations"][pid] <= 0:
                        completed.append(pid)
                        self.resources[res_name].counter += 1  # Acceder al recurso por nombre
                
                for pid in completed:
                    res_data["pids"].remove(pid)
                    del res_data["durations"][pid]

            # B. Procesar colas de espera
            for res_name, queue in waiting_queues.items():
                if not queue:
                    continue
                    
                resource = self.resources[res_name]  # Obtener objeto Resource por nombre
                new_queue = deque()
                
                if self.sync_type == "mutex":
                    if resource.counter > 0 and not resource_holders[res_name]["pids"]:
                        action = queue.popleft()
                        resource.counter -= 1
                        resource_holders[res_name]["pids"].append(action.pid)
                        resource_holders[res_name]["durations"][action.pid] = action_durations[action.action_type]
                        self.timeline.append((action.pid, cycle, action.action_type, "ACCESSED"))
                    new_queue = queue
                
                elif self.sync_type == "semaforo":
                    while queue and resource.counter > 0:
                        action = queue.popleft()
                        resource.counter -= 1
                        resource_holders[res_name]["pids"].append(action.pid)
                        resource_holders[res_name]["durations"][action.pid] = action_durations[action.action_type]
                        self.timeline.append((action.pid, cycle, action.action_type, "ACCESSED"))
                    new_queue = queue
                
                waiting_queues[res_name] = new_queue

            # C. Procesar nuevas acciones
            for action in actions_by_cycle.get(cycle, []):
                res_name = action.resource
                resource = self.resources[res_name]  # Obtener recurso por nombre
                
                if resource.counter > 0:
                    resource.counter -= 1
                    resource_holders[res_name]["pids"].append(action.pid)
                    resource_holders[res_name]["durations"][action.pid] = action_durations[action.action_type]
                    self.timeline.append((action.pid, cycle, action.action_type, "ACCESSED"))
                else:
                    waiting_queues[res_name].append(action)
                    self.timeline.append((action.pid, cycle, action.action_type, "WAITING"))

        return self.timeline