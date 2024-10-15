import pytest
from datetime import datetime, timedelta
from src.habits import Habit


def test_get_streak(sample_habit):
    assert sample_habit.get_streak() == 0
    sample_habit.current_streak = 5
    assert sample_habit.get_streak() == 5


@pytest.mark.parametrize("periodicity", [
    ("daily"),
    ("weekly"),
])
def test_calculate_next_completion_new_habit(sample_habit, periodicity):
    sample_habit.periodicity = periodicity
    sample_habit.next_completion_date = None
    now = datetime.now()
    expected_date = now.replace(hour=23, minute=59, second=59, microsecond=0)

    assert sample_habit.calculate_next_completion().date() == expected_date.date()

#  TODO COME BACK TO


@pytest.mark.parametrize("periodicity,date,expected_date", [
    ("daily", datetime(2024, 10, 15, 23, 59, 59),
     datetime(2024, 10, 16, 23, 59, 59)),
    ("weekly",  datetime(2024, 10, 15, 23, 59, 59),
     datetime(2024, 10, 22, 23, 59, 59)),
    ("weekly",  datetime(2024, 10, 8, 23, 59, 59),
     datetime(2024, 10, 22, 23, 59, 59)),
    ("weekly",  datetime(2024, 10, 10, 23, 59, 59),
     datetime(2024, 10, 24, 23, 59, 59))
])
def test_calculate_next_completion_default(sample_habit, periodicity, date, expected_date):
    sample_habit.periodicity = periodicity
    sample_habit.next_completion_date = date

    assert sample_habit.calculate_next_completion().date() == expected_date.date()


def test_calculate_next_completion_invalid_periodicity(sample_habit):
    sample_habit.periodicity = "invalid"
    with pytest.raises(ValueError, match="Unsupported periodicity"):
        sample_habit.calculate_next_completion()


def test_reset_streak(sample_habit):
    sample_habit.current_streak = 5
    sample_habit.reset_streak()
    assert sample_habit.current_streak == 0
    assert sample_habit.next_completion_date is not None


def test_is_due(sample_habit):
    sample_habit.next_completion_date = datetime.now() - timedelta(days=1)
    assert sample_habit.is_due() is True

    sample_habit.next_completion_date = datetime.now() + timedelta(days=1)
    assert sample_habit.is_due() is False
