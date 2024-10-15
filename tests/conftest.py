import pytest
from datetime import datetime
from src.habits import Habit, HabitManager
from src.tasks import Task, TaskManager


@pytest.fixture
def mock_storage(mocker):
    return mocker.Mock()


@pytest.fixture
def sample_habit():
    habit = Habit("Exercise", "daily")
    habit.id = 1
    return habit


@pytest.fixture
def habit_manager(mock_storage):
    return HabitManager(mock_storage)


@pytest.fixture
def mock_task_manager(mocker):
    return mocker.patch('src.tasks.TaskManager')


@pytest.fixture
def mock_task(mocker):
    return mocker.Mock(
        expected_completion_by=datetime.now(),
        habit_id=1
    )


@pytest.fixture
def sample_task():
    return Task(habit_id=1)


@pytest.fixture
def task_manager(mock_storage):
    return TaskManager(mock_storage)


@pytest.fixture
def sample_datetime():
    return datetime(2023, 1, 1, 12, 0, 0)


@pytest.fixture
def mock_datetime(mocker):
    mock = mocker.patch('datetime.datetime', autospec=True)
    mock.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    return mock
