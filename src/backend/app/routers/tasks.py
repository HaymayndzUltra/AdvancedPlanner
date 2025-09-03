
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..models import Task, TaskCreate, TaskUpdate
from ..storage import store

router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskListResponse(BaseModel):
    items: list[Task]


@router.get("/", response_model=TaskListResponse)
def list_tasks() -> TaskListResponse:
    return TaskListResponse(items=list(store.list_tasks()))


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    # Simple ID strategy: use title slug + count; replace in real DB
    base = payload.title.strip().lower().replace(" ", "-")
    suffix = 1
    candidate = base
    while store.get_task(candidate) is not None:
        suffix += 1
        candidate = f"{base}-{suffix}"
    return store.create_task(candidate, payload)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: str) -> Task:
    task = store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate) -> Task:
    task = store.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    deleted = store.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return None

