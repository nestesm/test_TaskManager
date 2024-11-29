from enum import Enum
from typing import Optional, Dict
from datetime import datetime


class EnumBase(Enum):
    @classmethod
    def list_values(cls):
        """Возвращает список всех значений Enum."""
        return [item.value for item in cls]

    @classmethod
    def list_names(cls):
        """Возвращает список всех имен Enum."""
        return [item.name for item in cls]
    
    def __str__(self):
        """Возвращает строковое представление значений перечисления через запятую."""
        return ", ".join(self.list_values())
    
class Priority(EnumBase):
    HIGH = 'Высокий'
    MEDIUM = 'Средний'
    LOW = 'Низкий'

class Status(EnumBase):
    DONE = 'Выполнена'
    NOT_DONE = 'Не выполнена'

class Task:
    _id_counter = 0 
    def __init__(self, title: str, description: str, category: str, due_date, priority: Priority, status: Status = Status.NOT_DONE):
        self._id: int = Task._generate_id() 
        self.title: str = title
        self.description: str = description
        self.category: str = category
        self._due_date = self.validate_data(due_date)   
        self.priority: str = priority
        self.status: str = status
        
    @classmethod
    def _generate_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter
        
    @staticmethod
    def validate_data(date_str: str) -> str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return 'Дата должна быть в формате YYYY-MM-DD'  
        
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, value: int) -> None:
        if self._id is not None:
            raise AttributeError("ID задачи уставновлено, изменение невозможно")
        if not isinstance(value, int) or value < 0:
            raise TypeError("Некорректное значение для ID задачи.")
        self._id = value 
        
    @property
    def due_date(self) -> str:
        return self._due_date
    
    @due_date.setter
    def due_date(self, value: str) -> None:
        self._due_date = self.validate_data(value)
        
    @property
    def priority(self) -> str:
        return self._priority
    
    @priority.setter
    def priority(self, value: str) -> None:
        pass
    
    @property
    def status(self) -> str:
        return self._status
        
    @status.setter
    def status(self, value: str) -> None:
        """
            Установка статуса задачи.
            
            Args:
                value (str): Новый статус книги. Можно указать строку 
                                      или объект BookStatus.

            Raises:
                ValueError: Если передано некорректное строковое значение.
                TypeError: Если тип аргумента не поддерживается.
        """
        if isinstance(value, str):
            try:
                value = Status(value)  # Преобразуем строку в объект BookStatus
            except ValueError:
                raise ValueError(f"Неверное значение для статуса книги. Допустимые значения: {str(Status)}") 
        if not isinstance(value, Status):
            raise ValueError(f"Неверное значение для статуса книги. Допустимые значения: {str(Status)}.")
        self._status = value

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        task = cls(
            id=data["id"], 
            title=data["title"], 
            description = data["description"],
            category = data["category"],
            due_date = data["due_date"], 
            priority = data["priority"], 
            status = data["status"]
        )
        task.id = data["id"]
        return task
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }
            
        