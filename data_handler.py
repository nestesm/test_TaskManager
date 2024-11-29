import json
import csv
from pathlib import Path
from typing import List, Callable
from functools import wraps

from task import Task

def handle_extension(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.extension not in [".json", ".csv"]:
            raise ValueError("Неподдерживаемое расширение файла.")
        return method(self, *args, **kwargs)
    return wrapper
class DataHandler:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.extension = self.file_path.suffix
        
    def save(self, tasks: List[Task])

    def save_to_json(self, tasks: List[Task]) -> None:
        data = [task.to_dict() for task in tasks]
        with self.file_path.open("w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    def load_from_json(self) -> List[Task]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл {self.file_path} не найден.")
        with self.file_path.open("r") as file:
            data = json.load(file)
        return [Task.from_dict(task) for task in data]
    
    def save_to_csv(self, tasks: List[Task]) -> None:
        with self.file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=tasks[0].to_dict().keys() if tasks else [])
            writer.writeheader()
            writer.writerows(task.to_dict() for task in tasks)
    
    def load_from_csv(self) -> List[Task]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл {self.file_path} не найден.")
        with self.file_path.open("r", encoding="utf-8") as file:
            rows = csv.DictReader(file)
            return [Task.from_dict(row) for row in rows]
        
    @handle_extension
    def save(self, tasks: List[Task]) -> None:
        if self.extension == ".json":
            self.save_to_json(tasks)
        elif self.extension == ".csv":
            self.save_to_csv(tasks)
            
    @handle_extension
    def load(self) -> List[Task]:
        if self.extension == ".json":
            return self.load_from_json()
        elif self.extension == ".csv":
            return self.load_from_csv()
        return []
            