from typing import List
from fastapi import APIRouter, HTTPException, status, Request
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from services.task_service import create_task, get_task_by_id, update_task, delete_task, get_all_tasks
from dependencies import limiter  # ← импортируем отсюда, НЕ из main!

router = APIRouter(prefix="/api/tasks", tags=["Task Manager"])

@router.get("/", response_model=List[TaskResponse])
@limiter.limit("10/minute")
def list_tasks(request: Request):
    """Получение списка всех задач"""
    return get_all_tasks()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_new_task(request: Request, task: TaskCreate):
    """Создание новой задачи"""
    return create_task(task)

@router.get("/{task_id}", response_model=TaskResponse)
@limiter.limit("10/minute")
def read_task(request: Request, task_id: int):
    """Получение задачи по ID"""
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
@limiter.limit("10/minute")
def patch_task(request: Request, task_id: int, task_data: TaskUpdate):  # ← исправлено: task_ → task_data
    """Частичное обновление задачи"""
    updated = update_task(task_id, task_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return updated

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
def remove_task(request: Request, task_id: int):
    """Удаление задачи"""
    if not delete_task(task_id):
        raise HTTPException(status_code=404, detail="Задача не найдена")