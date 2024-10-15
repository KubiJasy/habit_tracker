import pytest
from datetime import datetime, timedelta


def test_record_habit_completion(sample_task, mock_datetime):
    sample_task.record_habit_completion(1, datetime(2023, 1, 2), 5, 10)

    assert sample_task.habit_id == 1
    assert sample_task.completed
    assert sample_task.completed_on == mock_datetime.now()


def test_set_completed_on(sample_task):
    completion_date = datetime(2023, 1, 1)
    result = sample_task.set_completed_on(completion_date)
    assert result == completion_date
    assert sample_task.completed_on == completion_date


@pytest.mark.parametrize("periodicity, last_completion, expected", [
    ("daily", None, datetime.now().replace(
        hour=23, minute=59, second=59, microsecond=0)),
    ("daily", datetime.now(), (datetime.now() + timedelta(days=1)
                               ).replace(hour=23, minute=59, second=59, microsecond=0)),
    ("weekly", None, datetime.now().replace(
        hour=23, minute=59, second=59, microsecond=0)),
])
def test_calculate_expected_completion_by(sample_task, periodicity, last_completion, expected):
    result = sample_task.calculate_expected_completion_by(
        periodicity, last_completion)
    assert result.date() == expected.date()
    assert result.hour == 23
    assert result.minute == 59
    assert result.second == 59


def test_calculate_expected_completion_by_weekly(sample_task, sample_datetime, mock_datetime):
    last_completion = sample_datetime - timedelta(days=7)
    result = sample_task.calculate_expected_completion_by(
        "weekly", last_completion)

    expected = (sample_datetime + timedelta(days=7)
                ).replace(hour=23, minute=59, second=59, microsecond=0)
    assert result == expected


def test_calculate_expected_completion_by_invalid_periodicity(sample_task):
    with pytest.raises(ValueError, match="Unsupported periodicity"):
        sample_task.calculate_expected_completion_by("monthly")
