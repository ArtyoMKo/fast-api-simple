import os
import json
import pytest
from typing import List, Dict, Optional

from model.model import Task, TaskList
from model.taskman import (
    read_tasks_from_file,
    data_to_json,
    get_tasks,
    create_task,
    delete_task,
    update_task,
)

# Set the test file path
TEST_FILE_PATH = "test_tasks.json"


@pytest.fixture
async def setup_test_data(tmpdir):
    test_file_path = tmpdir.join(TEST_FILE_PATH)
    test_data = [
        {"id": 1, "task": {"summary": "Task 1", "priority": 1}},
        {"id": 2, "task": {"summary": "Task 2", "priority": 2}},
    ]
    with open(str(test_file_path), "w") as file:
        json.dump(test_data, file)
    return str(test_file_path)


@pytest.mark.asyncio
class TestTaskman:
    @pytest.mark.asyncio
    async def test_read_tasks_from_file(self, setup_test_data):
        test_file_path = await setup_test_data
        tasks = await read_tasks_from_file(test_file_path)
        assert isinstance(tasks, list)
        assert all(isinstance(task, TaskList) for task in tasks)

    @pytest.mark.asyncio
    async def test_data_to_json(self, setup_test_data):
        test_file_path = await setup_test_data
        test_data = [
            {"id": 3, "task": {"summary": "Task 3", "priority": 3}},
            {"id": 4, "task": {"summary": "Task 4", "priority": 4}},
        ]
        await data_to_json(test_data, test_file_path)

        with open(test_file_path, "r") as file:
            data = json.load(file)
        assert data == test_data

    @pytest.mark.asyncio
    async def test_get_tasks_all(self, setup_test_data):
        test_file_path = await setup_test_data
        tasks = await get_tasks(filepath=test_file_path)
        assert isinstance(tasks, dict)
        assert all(isinstance(task_id, int) for task_id in tasks.keys())
        assert all(isinstance(task_data, dict) for task_data in tasks.values())
