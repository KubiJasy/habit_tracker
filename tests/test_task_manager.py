import pytest
from datetime import datetime, timedelta
from src.tasks import Task


def test_create_task(task_manager, mock_storage):
    mock_storage.load_tasks_for_habit.return_value = []
    expected_task = Task(habit_id=1, expected_completion_by=datetime.now())
    mock_storage.save_task.return_value = expected_task

    created_task = task_manager.create_task(1, "daily")

    assert created_task.habit_id == 1
    assert created_task.expected_completion_by is not None
    mock_storage.save_task.assert_called_once()
    mock_storage.load_tasks_for_habit.assert_called_once_with(1)
    assert created_task == expected_task


def test_create_task_existing_habit(task_manager, mock_storage):
    existing_task = Task(habit_id=1, expected_completion_by=datetime.now())
    mock_storage.load_tasks_for_habit.return_value = [existing_task]
    expected_new_task = Task(
        habit_id=1, expected_completion_by=datetime.now() + timedelta(days=1))
    mock_storage.save_task.return_value = expected_new_task

    created_task = task_manager.create_task(1, "daily")

    assert created_task.habit_id == 1
    assert created_task.expected_completion_by > existing_task.expected_completion_by
    mock_storage.save_task.assert_called_once()
    mock_storage.load_tasks_for_habit.assert_called_once_with(1)
    assert created_task == expected_new_task


def test_update_task(task_manager, mock_storage):
    task = Task(habit_id=1)
    task.id = 1  # Simulate a saved task with an ID
    task_manager.tasks = [task]

    task_manager.update_task(1, completed=True)

    assert task.completed
    mock_storage.save_task.assert_called_once_with(task)


def test_delete_task(task_manager, mock_storage):
    task = Task(habit_id=1)
    task.id = 1  # Simulate a saved task with an ID
    task_manager.tasks = [task]

    task_manager.delete_task(1)

    assert task not in task_manager.tasks
    mock_storage.session.delete.assert_called_once_with(task)
    mock_storage.session.commit.assert_called_once()
