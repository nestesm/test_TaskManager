from typing import Dict
from task_manager import TaskManager
from task import Status, Priority, Task

def input_task_data() -> Dict:
    """
        Запрашивает у пользователя данные для создания или изменения задачи.
        
        Returns:
            Dict: Словарь с данными задачи.
    """
    return {
            "title": input("Название: ").strip(),
            "description": input("Описание: ").strip(),
            "category": input("Категория: ").strip(),
            "due_date": input("Срок выполнения (ГГГГ-ММ-ДД): ").strip(),
            "priority": input(f"Приоритет ({Priority.values_as_string()}): ").strip(),
            "status": input(f"Статус ({Status.values_as_string()}): ").strip(),
        }

def main():
    """
        Основная функция программы.
        Осуществляет взаимодействие пользователя с менеджером задач.
    """
    manager = TaskManager() # Создаем экземпляр менеджера задач
    
    while True:
        try:
            print( # Вывод меню действий
                "\n Менеджер задач",
                "1. Просмотреть задачи",
                "2. Добавить задачу",
                "3. Изменить задачу",
                "4. Удалить задачу",
                "5. Поиск задач",
                "0. Выход",
                sep="\n"
                )
            action = input("Введите номер действия: ").strip()
            match action: # Обработка выбранного действия
                case "1": # Просмотр задач по категории (или всех задач)
                    category = input("Введите категорию (оставьте поле пустым, для просмотра всех задач): ").strip() 
                    print()
                    tasks = manager.search_tasks(category=category)
                    if tasks:
                        print("\n\n".join(str(task) for task in tasks))
                    else:
                        print("Нет задач для отображения.")
                case "2": # Добавление новой задачи
                    print("Введите данные для создания задачи")
                    task_data = input_task_data()
                    task = Task(**task_data) # Создаем задачу с помощью распаковки словаря
                    manager.add_task(task) # Добавляем задачу в менеджер
                    print("Задача добавлена!")
                case "3": # Изменение существующей задачи
                    task_id = int(input("Введите ID задачи: ").strip())
                    
                    task_data = input_task_data() # Ввод данных для обновления
                    filtered_data = {key: value for key, value in task_data.items() if value} # Исключаем пустые значения
                    if manager.update_task(task_id, **filtered_data): # Попытка обновить задачу
                        print("Задача обновлена!") 
                    else: print("Ошибка обновления!")
                case "4": # Удаление задачи
                    print(
                        "Выберите критерий для удаления:",
                        "1. ID", 
                        "2. Категория", 
                        sep="\n"
                    )
                    try:
                        action = int(input("Введите номер действия (1 или 2): ").strip())
                    except ValueError:
                        print("Некорректный ввод! Пожалуйста, введите число 1 или 2.")
                        continue
                    
                    if action == 1: # Удаление по ID
                        try:
                            task_id = int(input("Введите ID задачи: ").strip())
                            manager.delete_task_by_id(task_id)
                            print(f"Задача с ID {task_id} успешно удалена.")
                        except ValueError:
                            print("Некорректный ID! Ожидалось целое число.")
                    elif action == 2: # Удаление по категории
                        category = input("Введите категорию: ").strip()
                        manager.delete_task_by_category(category)
                        print(f"Задачи категории '{category}' успешно удалены.")
                    else: print("Некорректное действие!")
                   
                case "5": # Поиск задач
                    task_data = {
                        "keyword": input("Ключевое слово: ").strip(),
                        "category": input("Категория: ").strip(),
                        "status": None
                    }
                    status_input = input(f"Статус ({Status.values_as_string()}): ").strip() 
                    if status_input: # Обработка статуса задачи
                        try:
                            task_data["status"] = Status(status_input)  # Преобразуем строку в экземпляр Status
                        except ValueError:
                            print(f"Некорректный статус: {status_input}")
                            task_data["status"] = None  # Если статус неверный, продолжаем без фильтрации по статусу
                    print("\nЗадачи:")
                    results = manager.search_tasks(**task_data)
                    if results:
                        for task in results:
                            print(task)
                    else: print("Задач не найдено!")
                    
                case "0": # Завершение работы программы
                    print("Окончание работы.")
                    break
                case _: # Обработка некорректного выбора
                    print("Некорректное действие! Попробуйте снова.")
        except Exception as e: # Общая обработка ошибок
            print(f"Произошла ошибка: {e}")
                
if __name__ == "__main__":
    main()
    