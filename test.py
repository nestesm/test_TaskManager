import pytest
from task_manager import Task, TaskManager, Priority, Status

@pytest.fixture
def task_manager():
    """
        Фикстура для создания экземпляра TaskManager
    """
    return TaskManager()

@pytest.fixture
def sample_task():
    """
        Фикстура для создания задачи
    """
    return Task(
        title="Test Task",
        description="Test Description",
        category="Work",
        due_date="2024-12-15",
        priority=Priority.MEDIUM
    )


def test_add_task(task_manager, sample_task):
    """
        Тест на добавление задачи
    """
    task_manager.add_task(sample_task)
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Test Task"
    assert task_manager.tasks[0].description == "Test Description"


def test_delete_task_by_id(task_manager, sample_task):
    """
        Тест на удаление задачи по ID
    """
    task_manager.add_task(sample_task)
    task_manager.delete_task_by_id(sample_task.id)
    assert len(task_manager.tasks) == 0


def test_search_tasks(task_manager, sample_task):
    """
        Тест на поиск задачи по ключевому слову
    """
    task_manager.add_task(sample_task)
    results = task_manager.search_tasks(keyword="Test")
    assert len(results) == 1
    assert results[0].title == "Test Task"


def test_update_task_priority(task_manager, sample_task):
    """
        Тест на обновление приоритета задачи
    """
    task_manager.add_task(sample_task)
    task_manager.update_task(sample_task.id, priority=Priority.HIGH)
    updated_task = task_manager.get_task(sample_task.id)
    assert updated_task.priority == Priority.HIGH


def test_delete_task_by_category(task_manager, sample_task):
    """
        Тест на удаление задач по категории
    """
    task_manager.add_task(sample_task)
    task_manager.add_task(Task(
        title="Another Task",
        description="Another Description",
        category="Personal",
        due_date="2024-12-16",
        priority=Priority.LOW
    ))
    task_manager.delete_task_by_category("Work")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].category == "Personal"


def test_task_to_dict(sample_task):
    """
        Тест на преобразование задачи в словарь
    """
    task_dict = sample_task.to_dict()
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == "Test Description"
    assert task_dict["category"] == "Work"
    assert task_dict["due_date"] == "2024-12-15"
    assert task_dict["priority"] == "Средний"
    assert task_dict["status"] == "Не выполнена"


def test_task_from_dict():
    """
        Тест на создание задачи из словаря
    """
    task_data = {
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "category": "Work",
        "due_date": "2024-12-15",
        "priority": "Средний",
        "status": "Не выполнена"
    }
    task = Task.from_dict(task_data)
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.category == "Work"
    assert task.due_date == "2024-12-15"
    assert task.priority == Priority.MEDIUM
    assert task.status == Status.NOT_DONE
