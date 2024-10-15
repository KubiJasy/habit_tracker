from datetime import datetime
from src.analytics import (
    list_habits,
    list_habits_periodicity,
    longest_streak_from_habits,
    longest_streak_for_given_habit
)
from src.habits import Habit


def test_list_habits(mocker, mock_storage):
    mock_storage.load_habits.return_value = [
        Habit("Exercise", "daily"),
        Habit("Read", "weekly")
    ]
    mocker.patch('src.analytics.StorageComponent', return_value=mock_storage)

    result = list_habits()

    assert len(result) == 2
    assert result[0].name == "Exercise"
    assert result[1].name == "Read"


def test_list_habits_periodicity(mocker, mock_storage):
    mock_storage.load_habits.return_value = [Habit("Exercise", "daily")]
    mocker.patch('src.analytics.StorageComponent', return_value=mock_storage)

    result = list_habits_periodicity("daily")

    assert len(result) == 1
    assert result[0].name == "Exercise"
    assert result[0].periodicity == "daily"


def test_longest_streak_from_habits(mocker, mock_storage):
    habit1 = Habit("Exercise", "daily", longest_streak=5)
    habit2 = Habit("Read", "weekly", longest_streak=10)
    mock_storage.load_habits.return_value = [habit1, habit2]
    mocker.patch('src.analytics.StorageComponent', return_value=mock_storage)

    result = longest_streak_from_habits()

    assert result == "The habit with the longest streak is 'Read' with a streak of 10."


def test_longest_streak_for_given_habit(mocker, mock_storage):
    habit = Habit("Exercise", "daily", longest_streak=15)
    mock_storage.load_habits.return_value = [habit]
    mocker.patch('src.analytics.StorageComponent', return_value=mock_storage)

    result = longest_streak_for_given_habit("Exercise")

    assert result == "The longest streak for habit 'Exercise' is 15."
