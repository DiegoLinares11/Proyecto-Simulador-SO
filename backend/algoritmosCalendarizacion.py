class SchedulingAlgorithm:
    @staticmethod
    def fifo(processes):
        return sorted(processes, key=lambda x: x['arrival_time'])
    
    @staticmethod
    def sjf(processes):
        
        return None
    @staticmethod
    def srt(processes):
        return None
    
    @staticmethod
    def round_robin(processes, quantum):
        return None
    @staticmethod
    def priority_scheduling(processes):
        return sorted(processes, key=lambda x: (x['priority'], x['arrival_time']))
    
    