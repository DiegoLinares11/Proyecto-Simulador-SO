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
        
    def simulate(self) -> List[Tuple[str, int, str, str]]:  # (pid, cycle, action, state)
        """Simulate synchronization mechanism"""
        waiting_processes = {}  # pid -> (action, resource, start_cycle)
        
        for action in self.actions:
            self.current_cycle = action.cycle
            resource = self.resources[action.resource]
            
            if action.pid in waiting_processes:
                # Process was waiting, check if it can proceed now
                continue
            
            if self.sync_type == "mutex":
                if resource.counter > 0:
                    # Resource available
                    resource.counter -= 1
                    self.timeline.append((action.pid, action.cycle, action.action_type, "ACCESSED"))
                    # Release resource after 1 cycle
                    resource.counter += 1
                else:
                    # Resource busy, process must wait
                    self.timeline.append((action.pid, action.cycle, action.action_type, "WAITING"))
                    waiting_processes[action.pid] = (action.action_type, action.resource, action.cycle)
            
            elif self.sync_type == "semaphore":
                if resource.counter > 0:
                    # Resource available
                    resource.counter -= 1
                    self.timeline.append((action.pid, action.cycle, action.action_type, "ACCESSED"))
                    # Resource will be released after use (simplified)
                    resource.counter += 1
                else:
                    # All resources busy, process must wait
                    self.timeline.append((action.pid, action.cycle, action.action_type, "WAITING"))
                    waiting_processes[action.pid] = (action.action_type, action.resource, action.cycle)
        
        return self.timeline