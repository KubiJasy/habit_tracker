import csv
from datetime import datetime, timedelta
import random


def simulate_habit(start_date, end_date, periodicity):
    current_date = start_date
    current_streak = 0
    longest_streak = 0
    last_completion = None
    streak_history = []

    while current_date <= end_date:
        if periodicity == "daily" or (periodicity == "weekly" and current_date.weekday() == start_date.weekday()):
            if random.random() < 0.8:  # 80% chance of completing the habit
                current_streak += 1
                last_completion = current_date
            else:
                streak_history.append(current_streak)
                current_streak = 0
        current_date += timedelta(days=1)

    if current_streak > 0:
        streak_history.append(current_streak)

    longest_streak = max(streak_history) if streak_history else 0

    if last_completion and (end_date - last_completion).days < (7 if periodicity == "weekly" else 1):
        current_streak = streak_history[-1] if streak_history else 0
    else:
        current_streak = 0

    return current_streak, longest_streak


def next_weekly_occurrence(start_date, reference_date):
    """Find the next occurrence of the same weekday as start_date, after or on reference_date."""
    days_ahead = (start_date.weekday() - reference_date.weekday()) % 7
    if days_ahead == 0 and reference_date.time() > start_date.time():
        # If it's the same day but the time has passed, move to the next week
        days_ahead = 7
    return reference_date + timedelta(days=days_ahead)


def generate_habits_data(num_rows):
    habits = [
        ("Meditate", "daily"), ("Read a book", "daily"), ("Exercise", "daily"),
        ("Write in journal", "daily"), ("Learn a new language", "daily"),
        ("Practice instrument", "daily"), ("Cook healthy meals", "weekly"),
        ("Take vitamins", "daily"), ("Floss teeth", "daily"),
        ("Call a friend", "weekly"), ("Save money", "daily"),
        ("Practice gratitude", "daily"), ("Drink water", "daily"),
        ("Stretch", "daily"), ("Clean the house", "weekly"),
        ("Go for a walk", "daily"), ("Practice coding", "daily"),
        ("Get 8 hours of sleep", "daily")
    ]

    start_date = datetime(2024, 8, 1)
    # Current date in the scenario
    # Todo: Make sure to update to current datetime when submitting the work
    # ! Adjust current time conf when necessary
    # this is to ensure that whenever the code is run, daily tasks will be just due for checking off and weekly tasks will be current as well
    end_date = datetime.now().replace(hour=23, minute=59, second=59,
                                      microsecond=0) - timedelta(days=1)
    print(end_date)

    data = []

    for index in range(num_rows):
        name, periodicity = random.choice(habits)
        habits.remove((name, periodicity))  # Ensure uniqueness

        created_at = start_date + \
            timedelta(seconds=random.randint(
                0, int((end_date - start_date).total_seconds())))

        current_streak, longest_streak = simulate_habit(
            created_at, end_date, periodicity)

        if periodicity == "daily":
            next_completion_date = end_date + timedelta(days=1)
        else:  # weekly
            next_completion_date = next_weekly_occurrence(created_at, end_date)

        data.append({
            "id": index + 1,
            "name": name,
            "periodicity": periodicity,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "next_completion_date": next_completion_date,
            "created_at": created_at,
            "updated_at": created_at
        })

    return data


def save_habits_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["id", "name", "periodicity", "current_streak",
                      "longest_streak", "next_completion_date", "created_at", "updated_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            row_copy = row.copy()
            for key in ['next_completion_date', 'created_at', 'updated_at']:
                row_copy[key] = row_copy[key].strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(row_copy)
