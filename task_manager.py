from typing import List

from task import Task
from data_handler import DataHandler

class TaskManager:
    _instance = None  # Singleton
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, data_file: str = "data.json"):
        if not hasattr(self, "initialized"):
            self.data_handler = DataHandler(data_file)
            self.tasks = self.data_handler.load()
            self.initialized = True
            
    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.data_handler.save(self.tasks)
        
    def delete_task_by_id(self, task_id: int) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.data_handler.save(self.tasks)