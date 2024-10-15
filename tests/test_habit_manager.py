import pytest
from src.habits import Habit  # Replace 'your_module' with the actual module name


def test_create_habit(habit_manager, mock_storage):
    mock_storage.save_habit.return_value = Habit("Exercise", "daily")
    habit = habit_manager.create_habit("Exercise", "daily")
    habit.id = 1

    assert habit.name == "Exercise"
    assert habit.periodicity == "daily"
    assert habit.id == 1
    mock_storage.save_habit.assert_called_once()


def test_update_habit(habit_manager, mock_storage):
    habit = Habit("Exercise", "daily")
    habit.id = 1
    habit_manager.habits = [habit]

    habit_manager.update_habit(1, name="New Exercise", periodicity="weekly")

    assert habit.name == "New Exercise"
    assert habit.periodicity == "weekly"
    mock_storage.save_habit.assert_called_once_with(habit)


def test_delete_habit(habit_manager, mock_storage):
    habit = Habit("Exercise", "daily")
    habit.id = 1
    habit_manager.habits = [habit]

    habit_manager.delete_habit(1)

    assert len(habit_manager.habits) == 0
    mock_storage.session.delete.assert_called_once_with(habit)
    mock_storage.session.commit.assert_called_once()


def test_mark_habit_completed(habit_manager, mock_storage, mock_task):
    habit = Habit("Exercise", "daily")
    habit.id = 1
    habit_manager.habits = [habit]

    mock_storage.load_tasks_for_habit.return_value = [mock_task]

    result = habit_manager.mark_habit_completed(1)

    assert result == "Habit marked as completed😊!"
    mock_storage.save_task.assert_called()
    mock_storage.save_habit.assert_called_once()


def test_clear_habits(habit_manager, mock_storage):
    habit_manager.habits = [
        Habit("Exercise", "daily"), Habit("Read", "weekly")]

    habit_manager.clear_habits()

    assert len(habit_manager.habits) == 0
    mock_storage.session.query.assert_called_once()
    mock_storage.session.query().delete.assert_called_once()
    mock_storage.session.commit.assert_called_once()
