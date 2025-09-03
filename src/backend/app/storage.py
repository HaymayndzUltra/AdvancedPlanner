from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from threading import RLock

from .models import Task, TaskCreate, TaskStatus, TaskUpdate


@dataclass
class InMemoryTaskStore:
    _tasks: dict[str, Task]
    _lock: RLock

    def __init__(self) -> None:
        self._tasks = {}
        self._lock = RLock()

    def _now(self) -> datetime:
        return datetime.now(tz=UTC)

    def list_tasks(self) -> Iterable[Task]:
        with self._lock:
            return list(self._tasks.values())

    def get_task(self, task_id: str) -> Task | None:
        with self._lock:
            return self._tasks.get(task_id)

    def create_task(self, task_id: str, create: TaskCreate) -> Task:
        now = self._now()
        task = Task(
            id=task_id,
            title=create.title,
            description=create.description,
            status=TaskStatus.todo,
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._tasks[task.id] = task
        return task

    def update_task(self, task_id: str, update: TaskUpdate) -> Task | None:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return None
            data = task.model_dump()
            if update.title is not None:
                data["title"] = update.title
            if update.description is not None:
                data["description"] = update.description
            if update.status is not None:
                data["status"] = update.status
            data["updated_at"] = self._now()
            new_task = Task(**data)
            self._tasks[task_id] = new_task
            return new_task

    def delete_task(self, task_id: str) -> bool:
        with self._lock:
            return self._tasks.pop(task_id, None) is not None


store = InMemoryTaskStore()

