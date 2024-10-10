from .generate_habits import generate_habits_data, save_habits_to_csv
from .generate_tasks import generate_task_data
import csv


def generate_habit_tracker_dataset():
    # Generating sample habits data
    num_rows = 15
    habits_data = generate_habits_data(num_rows)
    save_habits_to_csv(habits_data, "sample_habits.csv")
    print(
        f"Generated {len(habits_data)} rows of habit data.")

    # Generating sample tasks data for each habit
    # Read habit data from a CSV file
    with open("sample_habits.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        habit_data = list(reader)

    # Remove header row
    habit_data = habit_data[1:]  # Assuming the first row is the header

    tasks = generate_task_data(habit_data)

    # Write task data to a CSV file
    with open("sample_tasks.csv", "w", newline="") as csvfile:
        fieldnames = ["habit_id", "completed", "completed_on",
                      "expected_completion_by", "created_at", "updated_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)

    print(f"Generated {len(tasks)} rows of task data.")
