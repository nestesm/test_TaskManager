from typing import List, Optional

from task import Task, Priority, Status
from data_handler import DataHandler

class TaskManager:
    """
        Класс для управления задачами. Реализует паттерн Singleton.
        Отвечает за добавление, удаление, обновление и поиск задач.
    """
    _instance = None  # Экземпляр для реализации паттерна Singleton
    
    def __new__(cls, *args, **kwargs):
        """
            Создает единственный экземпляр TaskManager. Если экземпляр уже существует,
            возвращает его.

            Args:
                cls: Класс, для которого вызывается метод.

            Returns:
                TaskManager: Экземпляр класса.
        """
        if not cls._instance: # Если экземпляр еще не создан
            cls._instance = super().__new__(cls) # Создаем новый экземпляр
        return cls._instance # Возвращаем единственный экземпляр
    
    def __init__(self, data_file: str = "data.json"):
        """
            Инициализация менеджера задач. 
            Загружает задачи из файла и инициализирует обработчик данных.
            
            Args:
                data_file (str): Путь к файлу с данными.
        """
        if not hasattr(self, "initialized"): # Проверка на уже выполненную инициализацию
            self.data_handler = DataHandler(data_file) # Инициализируем обработчик данных
            self.tasks = self.data_handler.load() # Загружаем задачи из файла
            self.initialized = True # Помечаем инициализацию как выполненную
            self._update_id_counter() # Обновляем счетчик ID для задач
            
    def _update_id_counter(self) -> None:
        """
            Обновляет счетчик ID на основе существующих задач
        """
        if self.tasks: # Если задачи существуют
            max_id = max(task._id for task in self.tasks) # Находим максимальный ID среди задач
            Task._id_counter = max_id # Обновляем счетчик ID
            
    def add_task(self, task: Task) -> None:
        """
            Добавляет задачу в список задач и сохраняет изменения в файле.
            
            Args:
                task (Task): Задача для добавления.
        """
        self.tasks.append(task) # Добавляем задачу в список
        self.data_handler.save(self.tasks) # Сохраняем изменения в файл
        
    def delete_task_by_id(self, task_id: int) -> None:
        """
            Удаляет задачу по ее ID.
            
            Args:
                task_id (int): ID задачи для удаления.
        """
        self.tasks = [task for task in self.tasks if task.id != task_id] # Выбираем задачи без указанного ID
        self.data_handler.save(self.tasks) # Сохраняем изменения в файл
        
    def delete_task_by_category(self, category: str) -> None:
        """
            Удаляет задачи по категории.
            
            Args:
                category (str): Категория задач для удаления.
        """
        self.tasks = [task for task in self.tasks if task.category != category] # Фильтруем задачи по категории
        self.data_handler.save(self.tasks) # Сохраняем изменения в файл
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
            Получает задачу по ID.
            
            Args:
                task_id (int): ID задачи для поиска.

            Returns:
                Optional[Task]: Задача с указанным ID или None, если задача не найдена.
        """
        return next((task for task in self.tasks if task.id == task_id), None)
    
    def get_tasks_by_category(self, category: str) -> List[Task]:
        """
            Получает список задач по категории.
            
            Args:
                category (str): Категория для поиска задач.

            Returns:
                List[Task]: Список задач, принадлежащих указанной категории.
        """
        return [task for task in self.tasks if task.category == category]
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """
            Обновляет данные задачи по ее ID.
            
            Args:
                task_id (int): ID задачи для обновления.
                **kwargs: Ключи и значения, которые будут обновлены.

            Returns:
                bool: True, если задача успешно обновлена, иначе False.
        """
        task = self.get_task(task_id)  # Получаем задачу по ID
        if not task: # Если задача не найдена, возвращаем False
            return False
        for key, value in kwargs.items(): # Обновляем данные задачи в зависимости от переданных ключей
            if key in ["title", "description", "category", "due_date"]: 
                setattr(task, key, value)
            elif key == "priority" and value in Priority.list_values():
                task.priority = Priority(value)
            elif key == "status" and value in Status.list_values():
                task.status = Status(value)
        self.data_handler.save(self.tasks) # Сохраняем изменения в файл
        return True
    
    def search_tasks(self, keyword: str = "", category: str = "", status: Optional[Status] = None) -> List[Task]:
        """
            Ищет задачи по ключевому слову, категории и статусу.

            Args:
                keyword (str): Ключевое слово для поиска в названии и описании задачи.
                category (str): Категория для фильтрации задач.
                status (Optional[Status]): Статус для фильтрации задач.

            Returns:
                List[Task]: Список задач, соответствующих фильтрам.
        """
        return [
            task for task in self.tasks
            if (
                (keyword.upper() in task.description.upper() or keyword.upper() in task.title.upper())  # Проверка по ключевому слову
                and (category.upper() == task.category.upper() if category else True)  # Проверка по категории
                and (status == task.status if status else True)  # Проверка по статусу
            )
        ]