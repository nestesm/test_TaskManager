import json
import csv
from pathlib import Path
from typing import List

from task import Task


class DataHandler:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

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