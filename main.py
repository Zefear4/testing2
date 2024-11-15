from typing import List, Optional
from pydantic import BaseModel, Field, validator
import json

from BaseTask import BaseTask


class Task(BaseTask, BaseModel):
    name: str
    description: str = ''
    due_date: Optional[str] = None
    completed: bool = False

    @validator('due_date')
    def validate_due_date(cls, v):
        if v is not None:
            import datetime
            try:
                datetime.datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('due_date должен быть в формате YYYY-MM-DD')
        return v

    def complete(self):
        self.completed = True

    def is_completed(self) -> bool:
        return self.completed

    def postpone(self, days: int):
        if self.due_date is not None:
            import datetime
            due = datetime.datetime.strptime(self.due_date, '%Y-%m-%d')
            new_due = due + datetime.timedelta(days=days)
            self.due_date = new_due.strftime('%Y-%m-%d')
        else:
            raise ValueError('У задачи не установлена дата выполнения')

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def remove_task(self, task_name: str):
        self.tasks = [task for task in self.tasks if task.name != task_name]

    @classmethod
    def from_task_names(cls, names: List[str]):
        manager = cls()
        for name in names:
            manager.add_task(Task(name=name))
        return manager

    def save_to_file(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([task.dict() for task in self.tasks], f, ensure_ascii=False, indent=4)

    @classmethod
    def load_from_file(cls, filename: str):
        manager = cls()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                for task_data in tasks_data:
                    task = Task(**task_data)
                    manager.add_task(task)
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        return manager
