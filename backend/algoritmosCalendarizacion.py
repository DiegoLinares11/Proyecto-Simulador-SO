from collections import deque
from typing import List, Tuple
from .models import Process

class SchedulingAlgorithm:
    @staticmethod
    def fifo(processes: List[Process]) -> List[Tuple[str, int, int]]:
        """First In First Out scheduling"""
        timeline = []
        ready_queue = sorted(processes, key=lambda p: p.arrival_time)
        current_time = 0
            
        for process in ready_queue:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            process.start_time = current_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            timeline.append((process.pid, current_time, process.burst_time))
            current_time += process.burst_time
        
        return timeline
    
    @staticmethod
    def sjf(processes: List[Process]) -> List[Tuple[str, int, int]]:
        """Shortest Job First scheduling"""
        timeline = []
        processes_copy = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) for p in processes]
        current_time = 0
        completed = 0
        n = len(processes_copy)
        
        while completed < n:
            available = [p for p in processes_copy if p.arrival_time <= current_time and p.completion_time is None]
            
            if not available:
                current_time = min(p.arrival_time for p in processes_copy if p.completion_time is None)
                continue
            
            # Selecciona   el proceso con el menor tiempo de ráfaga
            selected = min(available, key=lambda p: p.burst_time)
            selected.start_time = current_time
            selected.completion_time = current_time + selected.burst_time
            selected.turnaround_time = selected.completion_time - selected.arrival_time
            selected.waiting_time = selected.turnaround_time - selected.burst_time
            
            timeline.append((selected.pid, current_time, selected.burst_time))
            current_time += selected.burst_time
            completed += 1
        
        return timeline
    
    @staticmethod
    def srt(processes: List[Process]) -> List[Tuple[str, int, int]]:
        """Shortest Remaining Time scheduling"""
        timeline = []
        processes_copy = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) for p in processes]
        current_time = 0
        completed = 0
        n = len(processes_copy)
        
        while completed < n:
            available = [p for p in processes_copy if p.arrival_time <= current_time and p.completion_time is None]
            
            if not available:
                current_time = min(p.arrival_time for p in processes_copy if p.completion_time is None)
                continue
            
            # Selecciona el proceso con el menor tiempo restante
            selected = min(available, key=lambda p: p.remaining_time)
            
            # Encuentra el tiempo de ejecución hasta el próximo evento
            next_event = float('inf')
            for p in processes_copy:
                if p.arrival_time > current_time:
                    next_event = min(next_event, p.arrival_time)
            
            execution_time = min(selected.remaining_time, next_event - current_time)
            if execution_time <= 0:
                execution_time = selected.remaining_time
            
            timeline.append((selected.pid, current_time, execution_time))
            selected.remaining_time -= execution_time
            current_time += execution_time
            
            if selected.remaining_time == 0:
                selected.completion_time = current_time
                selected.turnaround_time = selected.completion_time - selected.arrival_time
                selected.waiting_time = selected.turnaround_time - selected.burst_time
                completed += 1
        
        return timeline
    
    @staticmethod
    def round_robin(processes: List[Process], quantum: int) -> List[Tuple[str, int, int]]:
        """Round Robin scheduling"""
        timeline = []
        processes_copy = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) for p in processes]
        ready_queue = deque()
        current_time = 0
        completed = 0
        n = len(processes_copy)
        
        # Agregar procesos que llegan al tiempo 0 a la cola lista
        for p in processes_copy:
            if p.arrival_time == 0:
                ready_queue.append(p)
        
        while completed < n:
            if not ready_queue:
                # Encuentra el próximo proceso que llegue
                next_process = min([p for p in processes_copy if p.completion_time is None], 
                                 key=lambda p: p.arrival_time)
                current_time = next_process.arrival_time
                ready_queue.append(next_process)
            
            current_process = ready_queue.popleft()
            execution_time = min(quantum, current_process.remaining_time)
            
            timeline.append((current_process.pid, current_time, execution_time))
            current_process.remaining_time -= execution_time
            current_time += execution_time
            
            # Agregar procesos que llegan al tiempo actual a la cola lista
            for p in processes_copy:
                if p.arrival_time <= current_time and p not in ready_queue and p.completion_time is None and p != current_process:
                    ready_queue.append(p)
            
            if current_process.remaining_time > 0:
                ready_queue.append(current_process)
            else:
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                completed += 1
        
        return timeline
    
    @staticmethod
    def priority_scheduling(processes: List[Process]) -> List[Tuple[str, int, int]]:
        """Priority scheduling (lower number = higher priority)"""
        timeline = []
        processes_copy = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) for p in processes]
        current_time = 0
        completed = 0
        n = len(processes_copy)
        
        while completed < n:
            available = [p for p in processes_copy if p.arrival_time <= current_time and p.completion_time is None]
            
            if not available:
                current_time = min(p.arrival_time for p in processes_copy if p.completion_time is None)
                continue
            
            # Selecciona el proceso con la mayor prioridad (menor número)
            selected = min(available, key=lambda p: p.priority)
            selected.start_time = current_time
            selected.completion_time = current_time + selected.burst_time
            selected.turnaround_time = selected.completion_time - selected.arrival_time
            selected.waiting_time = selected.turnaround_time - selected.burst_time
            
            timeline.append((selected.pid, current_time, selected.burst_time))
            current_time += selected.burst_time
            completed += 1
        
        return timeline