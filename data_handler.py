import json
import csv
from pathlib import Path
from typing import List, Callable
from functools import wraps

from task import Task

def handle_extension(method: Callable) -> Callable:
    """
    Декоратор для проверки расширения файла перед выполнением метода.
    Поддерживаются только файлы с расширениями .json и .csv.
    
    Args:
        method (Callable): Метод, который будет обернут декоратором.
        
    Returns:
        Callable: Обработанный метод.
    """
    @wraps(method) # Сохраняем оригинальное имя метода и его документацию
    def wrapper(self, *args, **kwargs):
        if self.extension not in [".json", ".csv"]: # Проверяем, что расширение файла поддерживаемое
            raise ValueError("Неподдерживаемое расширение файла.")
        return method(self, *args, **kwargs) # Вызываем оригинальный метод
    return wrapper
class DataHandler:
    """
        Класс для обработки данных, сохранения и загрузки их из файлов.
        Поддерживает форматы JSON и CSV.
    """
    
    def __init__(self, file_path: str):
        """
            Инициализация DataHandler с путем к файлу.
            
            Args:
                file_path (str): Путь к файлу, в котором будут сохраняться или из которого будут загружаться данные.
        """
        self.file_path = Path(file_path) # Преобразуем строку в объект Path для удобства работы с файлом
        self.extension = self.file_path.suffix # Определяем расширение файла

    def save_to_json(self, tasks: List[Task]) -> None:
        """
            Сохраняет список задач в файл формата JSON.
            
            Args:
                tasks (List[Task]): Список задач для сохранения.
        """
        data = [task.to_dict() for task in tasks] # Преобразуем каждую задачу в словарь
        with self.file_path.open("w") as file: # Открываем файл для записи
            json.dump(data, file, indent=4, ensure_ascii=False) # Сохраняем данные в JSON формате
    
    def load_from_json(self) -> List[Task]:
        """
            Загружает список задач из файла формата JSON.
            
            Returns:
                List[Task]: Список задач, загруженных из файла.
            
            Raises:
                FileNotFoundError: Если файл не существует.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл {self.file_path} не найден.") # Если файл не найден, выбрасываем исключение
        with self.file_path.open("r") as file:
            data = json.load(file) # Загружаем данные из файла
        return [Task.from_dict(task) for task in data] # Преобразуем данные в объекты Task
    
    def save_to_csv(self, tasks: List[Task]) -> None:
        """
            Сохраняет список задач в файл формата CSV.
            
            Args:
                tasks (List[Task]): Список задач для сохранения.
        """
        with self.file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=tasks[0].to_dict().keys() if tasks else [])
            writer.writeheader() # Пишем заголовки для столбцов
            writer.writerows(task.to_dict() for task in tasks) # Записываем данные задач
    
    def load_from_csv(self) -> List[Task]:
        """
            Загружает список задач из файла формата CSV.
            
            Returns:
                List[Task]: Список задач, загруженных из файла.
            
            Raises:
                FileNotFoundError: Если файл не существует.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл {self.file_path} не найден.") # Если файл не найден, выбрасываем исключение
        with self.file_path.open("r", encoding="utf-8") as file:
            rows = csv.DictReader(file) # Читаем строки из CSV
            return [Task.from_dict(row) for row in rows] # Преобразуем строки в объекты Task
        
    @handle_extension
    def save(self, tasks: List[Task]) -> None:
        """
            Сохраняет задачи в файл в зависимости от расширения файла.
            
            Args:
                tasks (List[Task]): Список задач для сохранения.
        """
        if self.extension == ".json":
            self.save_to_json(tasks) # Сохраняем в формате JSON
        elif self.extension == ".csv":
            self.save_to_csv(tasks) # Сохраняем в формате CSV
            
    @handle_extension
    def load(self) -> List[Task]:
        """
            Загружает задачи из файла в зависимости от расширения файла.
            
            Returns:
                List[Task]: Список задач, загруженных из файла.
        """
        if self.extension == ".json":
            return self.load_from_json() # Загружаем из JSON
        elif self.extension == ".csv":
            return self.load_from_csv() # Загружаем из CSV
        return [] # Если расширение не поддерживается, возвращаем пустой список
            