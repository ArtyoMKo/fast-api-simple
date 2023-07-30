from typing import NewType
from pydantic import BaseModel

ID = NewType("id", int)  # type: ignore


class Task(BaseModel):
    """
    Definition of components of all tasks
    """

    summary: str
    priority: int


class TaskList(BaseModel):
    """
    Definition of the TaskList - task ids
    """

    id: ID
    task: Task
