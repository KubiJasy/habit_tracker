import pandas as pd
from src.db import session
from src.models import Habit, Task
from .generate_habit_tracker_dataset import generate_habit_tracker_dataset
from .validate_sample_habits import validate_habit_data
from .validate_sample_tasks import validate_task_entries_from_csv


def load_habits_from_csv(csv_file):
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        habit = Habit(
            id=row['id'],
            name=row['name'],
            periodicity=row['periodicity'],
            current_streak=row['current_streak'],
            longest_streak=row['longest_streak'],
            next_completion_date=pd.to_datetime(row['next_completion_date']),
            created_at=pd.to_datetime(row['created_at']),
            updated_at=pd.to_datetime(row['updated_at'])
        )
        session.add(habit)

    session.commit()
    session.close()
    print("Habits loaded successfully.")


def load_tasks_from_csv(csv_file):
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        task = Task(
            habit_id=row['habit_id'],
            completed=row['completed'],
            completed_on=pd.to_datetime(row['completed_on']) if pd.notnull(
                row['completed_on']) else None,
            expected_completion_by=pd.to_datetime(
                row['expected_completion_by']),
            created_at=pd.to_datetime(row['created_at']),
            updated_at=pd.to_datetime(row['updated_at'])
        )
        session.add(task)

    session.commit()
    session.close()
    print("Tasks loaded successfully.")


def load_data():
    # delete existing data if any
    session.query(Habit).delete()
    session.query(Task).delete()
    session.commit()
    session.close()

    # generating habit data
    generate_habit_tracker_dataset()

    # Validating that the generated dataset is consistent
    habits_valid, habits_validation_report = validate_habit_data(
        "sample_habits.csv")
    tasks_valid, tasks_validation_report = validate_task_entries_from_csv(
        "sample_tasks.csv", "sample_habits.csv")

    print(habits_validation_report, tasks_validation_report)

    # populating the database with generated data
    if habits_valid and tasks_valid:
        load_habits_from_csv("sample_habits.csv")
        load_tasks_from_csv("sample_tasks.csv")
    else:
        print("Please run the script again, invalid data generated!!")
        exit()
