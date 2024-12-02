from enum import Enum
from typing import Optional, Dict, List, Any
from datetime import datetime


class EnumBase(Enum):
    """
        Базовый класс для перечислений, содержащий методы для работы с перечислениями.
    """
    @classmethod
    def list_values(cls) -> List[Any]:
        """
            Возвращает список всех значений Enum.

            Returns:
                List[Any]: Список значений перечисления.
        """
        return [item.value for item in cls]
    
    @classmethod
    def values_as_string(cls) -> str:
        """
            Возвращает строковое представление значений перечисления через запятую.

            Returns:
                str: Строка, содержащая все значения перечисления, разделенные запятой.
        """
        return ", ".join(cls.list_values())
    
class Priority(EnumBase):
    """
        Перечисление для приоритетов задач.
    """
    HIGH = 'Высокий'
    MEDIUM = 'Средний'
    LOW = 'Низкий'

class Status(EnumBase):
    """
        Перечисление для статусов задач.
    """
    DONE = 'Выполнена'
    NOT_DONE = 'Не выполнена'

class Task:
    """
        Класс для представления задачи с аттрибутами и методами для манипуляций с задачами.
    """
    _id_counter = 0  # Статическая переменная для автоматической генерации ID задач
    def __init__(self, title: str, description: str, category: str, due_date, priority: Priority, status: Status = Status.NOT_DONE):
        """
            Инициализация задачи с необходимыми аттрибутами.

            Args:
                title (str): Название задачи.
                description (str): Описание задачи.
                category (str): Категория задачи.
                due_date (str): Срок выполнения задачи в формате YYYY-MM-DD.
                priority (Priority): Приоритет задачи.
                status (Status): Статус задачи (по умолчанию - "Не выполнена").
        """
        self._id: int = Task._generate_id() # Генерация уникального ID задачи
        self.title: str = title
        self.description: str = description
        self.category: str = category
        self._due_date: datetime = self.validate_data(due_date)  # Валидация даты
        self.priority: str = priority
        self.status: str = status
    
    @classmethod
    def _generate_id(cls) -> int:
        """
            Генерирует уникальный ID для задачи.

            Returns:
                int: Уникальный ID задачи.
        """
        cls._id_counter += 1
        return cls._id_counter
        
    @staticmethod
    def validate_data(date_str: str) -> datetime:
        """
            Валидация строки с датой, проверка на формат YYYY-MM-DD.

            Args:
                date_str (str): Строка с датой для валидации.

            Returns:
                datetime: Объект даты, если дата корректна.

            Raises:
                ValueError: Если строка не соответствует формату.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")

        except ValueError:
            raise "Дата должна быть в формате YYYY-MM-DD"  
            
    @property
    def id(self) -> Optional[int]:
        """
            Геттер для получения ID задачи.

            Returns:
                Optional[int]: ID задачи.
        """
        return self._id
    
    @id.setter
    def id(self, value: int) -> None:
        """
            Сеттер для установки ID задачи. Не допускает изменение ID после его установки.

            Args:
                value (int): Новый ID задачи.

            Raises:
                AttributeError: Если ID уже был установлен.
                TypeError: Если ID некорректного типа.
        """
        if self._id is not None:
            raise AttributeError("ID задачи уставновлено, изменение невозможно")
        if not isinstance(value, int) or value < 0:
            raise TypeError("Некорректное значение для ID задачи.")
        self._id = value 
        
    @property
    def due_date(self) -> str:
        """
            Геттер для получения строки с датой в формате YYYY-MM-DD.

            Returns:
                str: Дата в строковом формате.
        """
        return self._due_date.strftime("%Y-%m-%d")
    
    @due_date.setter
    def due_date(self, value: str) -> None:
        """
            Сеттер для установки даты выполнения задачи. Выполняет валидацию даты.

            Args:
                value (str): Новая дата задачи в формате YYYY-MM-DD.
        """
        self._due_date = self.validate_data(value)
        
    @property
    def priority(self) -> str:
        """
            Геттер для получения приоритета задачи.

            Returns:
                str: Приоритет задачи.
        """
        return self._priority
    
    @priority.setter
    def priority(self, value: str) -> None:
        """
            Сеттер для установки приоритета задачи.

            Args:
                value (str): Новый приоритет задачи.

            Raises:
                ValueError: Если передано некорректное строковое значение.
                TypeError: Если тип аргумента не поддерживается.
        """
        if isinstance(value, str):
            try:
                value = Priority(value)   # Преобразуем строку в объект Priority
            except ValueError:
                raise ValueError(f"Неверное значение для приоритета задачи. Допустимые значения: {Priority.values_as_string()}") 
        if not isinstance(value, Priority):
            raise ValueError(f"Неверное значение для приоритета задачи. Допустимые значения: {Priority.values_as_string()}.")
        self._priority = value
    
    @property
    def status(self) -> str:
        """
            Геттер для получения статуса задачи.

            Returns:
                str: Статус задачи.
        """

        return self._status
        
    @status.setter
    def status(self, value: str) -> None:
        """
            Установка статуса задачи.
            
            Args:
                value (str): Новый статус задачи. 

            Raises:
                ValueError: Если передано некорректное строковое значение.
                TypeError: Если тип аргумента не поддерживается.
        """
        if isinstance(value, str):
            try:
                value = Status(value)  # Преобразуем строку в объект Status
            except ValueError:
                raise ValueError(f"Неверное значение для статуса задачи. Допустимые значения: {Status.values_as_string()}") 
        if not isinstance(value, Status):
            raise ValueError(f"Неверное значение для статуса задачи. Допустимые значения: {Status.values_as_string()}.")
        self._status = value

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """
            Создает задачу из словаря данных.

            Args:
                data (Dict): Данные задачи.

            Returns:
                Task: Созданная задача.
        """
        task = cls(
            title=data["title"], 
            description = data["description"],
            category = data["category"],
            due_date = data["due_date"], 
            priority = data["priority"], 
            status = data["status"]
        )
        task._id = data["id"] # Устанавливаем ID задачи
        return task
        
    def to_dict(self) -> dict:
        """
            Преобразует задачу в словарь.

            Returns:
                dict: Словарь, содержащий аттрибуты задачи.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority.value,
            "status": self.status.value
        }
        
    def __str__(self) -> str:
        """
            Строковое представление задачи.

            Returns:
                str: Представление задачи в строковом формате.
        """
        return (
            f"Задача ID: {self.id}\n"
            f"Название: {self.title or 'Не указано'}\n"
            f"Описание: {self.description or 'Не указано'}\n"
            f"Категория: {self.category or 'Не указано'}\n"
            f"Срок выполнения: {self.due_date or 'Не задан'}\n"
            f"Приоритет: {getattr(self.priority, 'value', 'Не указан')}\n"
            f"Статус: {getattr(self.status, 'value', 'Не указан')}"
        )
            
        