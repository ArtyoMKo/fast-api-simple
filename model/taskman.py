"""
    This is our task handler. We could have built this inside the routes themselves
but the reason why they are split is because of top-down design paradigms where
one can replace the handler which currently handles JSON , to a handler that
handles either a Relational DB or a NoSQL DB without changing anything in the
routes.
    Or if we wanted to change the routes in future you don’t have to change anything
in task handler.
"""

from typing import List, Dict, Optional
import logging
import json

# from pydantic import parse_file_as

from model.model import Task, TaskList

FILE_PATH = "data/tasks.json"


async def read_tasks_from_file(file_path: str):
    data = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exception:
        logging.error(f"{exception}")
    tasks = [TaskList(**item) for item in data]
    return tasks


parse_file_as = read_tasks_from_file


async def data_to_json(data: List, filepath: str = FILE_PATH) -> bool:
    """
    Take data and write it in json file
    :param filepath: Path of json file
    :param data: List of data to be written
    :return: Boolean True or False
    """
    try:
        data = json.dumps(data)  # type: ignore
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(data)  # type: ignore
        return True
    except Exception as exception:  # pylint: disable=broad-except
        logging.error(f"{exception}")
        return False


async def get_tasks(task_id: Optional[int] = 0, filepath: str = FILE_PATH) -> Dict:
    """
    Get all tasks if no id provided, else get task by task id
    :param filepath: Path of json file
    :param task_id: Task id
    :return: Dict of Tasks
    """
    tasks = await parse_file_as(filepath)
    data = {task.id: task.model_dump() for task in tasks}
    response = data if task_id == 0 else data[task_id]
    return response


async def create_task(new_task: Task, filepath: str = FILE_PATH) -> int:
    """
    Create new task
    :param filepath: Path of json file
    :param new_task: Task parameters
    :return: Task id
    """
    tasks = await parse_file_as(filepath)
    if tasks:
        task_id = max(task.id for task in tasks) + 1
    else:
        task_id = 1
    tasks.append(TaskList(id=task_id, task=new_task))
    data = [task.model_dump() for task in tasks]
    await data_to_json(data)
    return task_id


async def delete_task(task_id: int, filepath: str = FILE_PATH) -> int:
    """
    Delete task
    :param filepath: Path of json file
    :param task_id: Task id
    :return: Task id
    """
    tasks = await read_tasks_from_file(filepath)
    tasks = [task for task in tasks if task.id != task_id]
    data = [task.model_dump() for task in tasks]
    await data_to_json(data)
    return task_id


async def update_task(task_id: int, new_task: Task, filepath: str = FILE_PATH) -> int:
    """
    Update task
    :param filepath: Path of json file
    :param task_id: Task id
    :param new_task: New task parameters
    :return: Task id
    """
    tasks = await read_tasks_from_file(filepath)
    data = [task.model_dump() for task in tasks]
    for task_dict in data:
        if task_dict["id"] == task_id:
            task_dict["task"] = new_task.model_dump()
    await data_to_json(data)
    return task_id
