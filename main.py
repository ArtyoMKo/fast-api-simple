from typing import Dict
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from model import taskman
from model.model import Task

app = FastAPI()
BASE_URL = "/api/tasks"


@app.get(f"{BASE_URL}")
async def get_tasks() -> Dict:
    """
    Get all tasks
    :return: Dict of tasks
    """
    return await taskman.get_tasks()


@app.get(BASE_URL + "/{task_id}")
async def get_task(task_id: int) -> Dict:
    """
    Get task by task id parameter
    :param task_id: Task id
    :return: Dict of task components
    """
    return await taskman.get_tasks(task_id)


@app.post(BASE_URL + "/create")
async def create_task(task: Task) -> Dict:
    """
    Create new task and return details
    :param task: Task parameters
    :return: Dict of tasks
    """
    task_id = await taskman.create_task(task)
    return await taskman.get_tasks(task_id)


@app.put(BASE_URL + "/{task_id}/update")
async def update_task(task_id: int, task: Task) -> Dict:
    """
    Updated existing tasks by task id
    :param task_id: Task id
    :param task: Existed task
    :return: Dict of updated task
    """
    await taskman.update_task(task_id, task)
    return await taskman.get_tasks(task_id)


@app.delete(BASE_URL + "/{task_id}/delete")
async def delete_task(task_id: int) -> Dict:
    """
    Delete existing task by task id
    :param task_id: Task id
    :return: Dict of message
    """
    task_id = await taskman.delete_task(task_id)
    response = {task_id: "Task successfully deleted"}
    return jsonable_encoder(response)
