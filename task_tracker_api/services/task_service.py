from typing import List, Optional
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from datetime import datetime

_tasks_db: List[TaskResponse] = []
_next_id: int = 1

def mask_email(email: str) -> str:
    """Маскирует email для защиты персональных данных"""
    if "@" in email:
        local, domain = email.split("@")
        return f"{local[:2]}***@{domain}"
    return email

def create_task(task_data: TaskCreate) -> TaskResponse:
    global _next_id
    new_task = TaskResponse(
        id=_next_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status=task_data.status,
        due_date=task_data.due_date,
        assigned_email=mask_email(task_data.assigned_email),  # ← Маскирование при создании
        created_at=datetime.now()
    )
    _tasks_db.append(new_task)
    _next_id += 1
    return new_task

def get_task_by_id(task_id: int) -> Optional[TaskResponse]:
    """Получение задачи по ID"""
    for task in _tasks_db:
        if task.id == task_id:
            return task
    return None

def get_all_tasks() -> List[TaskResponse]:
    """Получение списка всех задач (копия, чтобы не передавать ссылку на внутреннее хранилище)"""
    return _tasks_db.copy()

def update_task(task_id: int, task_data: TaskUpdate) -> Optional[TaskResponse]:
    """Частичное обновление задачи"""
    for i, task in enumerate(_tasks_db):
        if task.id == task_id:
            update_dict = task_data.model_dump(exclude_unset=True)
            # Если обновляем email — маскируем его
            if "assigned_email" in update_dict and update_dict["assigned_email"]:
                update_dict["assigned_email"] = mask_email(update_dict["assigned_email"])
            updated_task = task.model_copy(update={**update_dict, "updated_at": datetime.now()})
            _tasks_db[i] = updated_task
            return updated_task
    return None

def delete_task(task_id: int) -> bool:
    """Удаление задачи по ID"""
    global _tasks_db
    initial_len = len(_tasks_db)
    _tasks_db = [t for t in _tasks_db if t.id != task_id]
    return len(_tasks_db) < initial_len