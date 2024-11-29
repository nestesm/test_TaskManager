from typing import List, Optional

from task import Task, Priority, Status
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
        
    def delete_task_by_category(self, category: str) -> None:
        self.task = [task for task in self.tasks if task.category == category]
        self.data_handler.save(self.tasks)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)
    
    def get_tasks_by_category(self, category: str) -> List[Task]:
        return [task for task in self.tasks if task.category == category]
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        for key, value in kwargs:
            if key in ["title", "description", "category", "due_date"]:
                setattr(task, key, value)
            elif key == "priority" and value in Priority.list_values():
                task.priority = Priority(value)
            elif key == "status" and value in Status.list_values():
                task.status = Status(value)
        self.data_handler.save(self.tasks)
        return True
    
    def search_tasks(self, keyword: str = "", category: str = "", status: Optional[Status] = None ) -> List[Task]:
        return [
            task for task in self.tasks 
            if (keyword.upper() in task.description.upper()) or (keyword.upper() in task.description.upper())
            and (category.upper() == task.category.upper() if category else True)
            and (status == task.status if status else True)
        ]