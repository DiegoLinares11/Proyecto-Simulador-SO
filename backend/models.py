from dataclasses import dataclass
from enum import Enum

class ProcessState(Enum):
    READY = "READY"
    RUNNING = "RUNNING" 
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"
    ACCESSED = "ACCESSED"

@dataclass
class Process:
    pid: str
    burst_time: int
    arrival_time: int
    priority: int
    remaining_time: int = None
    start_time: int = None
    completion_time: int = None
    waiting_time: int = 0
    turnaround_time: int = 0
    state: ProcessState = ProcessState.READY
    
    def __post_init__(self):
        if self.remaining_time is None:
            self.remaining_time = self.burst_time

@dataclass
class Resource:
    name: str
    counter: int
    max_counter: int
    
    def __post_init__(self):
        self.max_counter = self.counter

@dataclass
class Action:
    pid: str
    action_type: str  # READ or WRITE
    resource: str
    cycle: int